"""Calendar management functionality for ChronoLock."""

from __future__ import annotations

import json
import os
from dataclasses import dataclass
from datetime import datetime, timedelta
from getpass import getpass
from pathlib import Path

from dateutil import parser, tz
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/calendar"]
DEFAULT_TOKEN_PATH = Path.home() / ".config" / "chronolock" / "google_calendar_token.json"


@dataclass
class MeetingRequest:
    summary: str
    starts_at: datetime
    duration_minutes: int

    @property
    def ends_at(self) -> datetime:
        return self.starts_at + timedelta(minutes=self.duration_minutes)


def load_client_config() -> dict:
    """Load Google OAuth client secrets from environment or user input."""
    json_env = os.environ.get("CHRONOLOCK_GOOGLE_CLIENT_SECRETS_JSON")
    if json_env:
        return json.loads(json_env)

    path_env = os.environ.get("CHRONOLOCK_GOOGLE_CLIENT_SECRETS_PATH")
    if path_env:
        return json.loads(Path(path_env).read_text())

    raw = getpass(
        "Paste OAuth client secrets JSON (input hidden). "
        "Set CHRONOLOCK_GOOGLE_CLIENT_SECRETS_JSON to skip: "
    ).strip()
    if not raw:
        raise RuntimeError("No OAuth client secrets provided.")
    return json.loads(raw)


def load_credentials(token_path: Path) -> Credentials:
    """Load or create Google Calendar credentials."""
    credentials = None
    if token_path.exists():
        try:
            credentials = Credentials.from_authorized_user_file(token_path, SCOPES)
        except ValueError as e:
            # Token file exists but is invalid - likely a client secrets file, not a token
            print(f"Warning: Token file exists but is invalid: {e}")
            print("This may be a client secrets file instead of an authorized token.")
            print("Proceeding with OAuth flow to generate a proper token...")
            credentials = None

    if credentials and credentials.expired and credentials.refresh_token:
        credentials.refresh(Request())
        token_path.write_text(credentials.to_json())
        return credentials

    if credentials and credentials.valid:
        return credentials

    config = load_client_config()
    flow = InstalledAppFlow.from_client_config(config, SCOPES)
    credentials = flow.run_local_server(port=0)
    token_path.parent.mkdir(parents=True, exist_ok=True)
    token_path.write_text(credentials.to_json())
    return credentials


def prompt_meeting_request() -> MeetingRequest:
    """Prompt user for meeting details."""
    tomorrow = datetime.now(tz=tz.tzlocal()) + timedelta(days=1)
    summary = input("Meeting name: ").strip()
    if not summary:
        raise RuntimeError("Meeting name is required.")

    starts_at_raw = input(f"When should the meeting start? (e.g. {tomorrow.strftime('%Y-%m-%d %H:%M')}) ").strip()
    if not starts_at_raw:
        raise RuntimeError("Start time is required.")

    starts_at = parser.parse(starts_at_raw)
    if starts_at.tzinfo is None:
        starts_at = starts_at.replace(tzinfo=tz.tzlocal())

    duration_raw = input("How long in minutes? ").strip()
    if not duration_raw.isdigit():
        raise RuntimeError("Duration must be an integer number of minutes.")

    return MeetingRequest(
        summary=summary,
        starts_at=starts_at,
        duration_minutes=int(duration_raw),
    )


def list_upcoming_events(service) -> None:
    """List upcoming events on the primary calendar."""
    now = datetime.now(tz=tz.tzlocal()).isoformat()
    events = (
        service.events()
        .list(
            calendarId="primary",
            timeMin=now,
            maxResults=5,
            singleEvents=True,
            orderBy="startTime",
        )
        .execute()
    )
    items = events.get("items", [])
    if not items:
        print("No upcoming events found.")
        return

    print("Upcoming events:")
    for event in items:
        start = event.get("start", {}).get("dateTime", event.get("start", {}).get("date"))
        summary = event.get("summary", "(no title)")
        print(f"- {start}: {summary}")


def create_event(service, meeting: MeetingRequest) -> dict:
    """Create a new event on the primary calendar."""
    body = {
        "summary": meeting.summary,
        "start": {"dateTime": meeting.starts_at.isoformat()},
        "end": {"dateTime": meeting.ends_at.isoformat()},
    }
    return service.events().insert(calendarId="primary", body=body).execute()


def delete_event(service, event_id: str) -> None:
    """Delete an event from the primary calendar."""
    service.events().delete(calendarId="primary", eventId=event_id).execute()