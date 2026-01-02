from __future__ import annotations

import os
from pathlib import Path

from googleapiclient.discovery import build

from chronolock.calendar_management import (
    DEFAULT_TOKEN_PATH,
    MeetingRequest,
    create_event,
    delete_event,
    list_upcoming_events,
    load_credentials,
    prompt_meeting_request,
)


def _load_credentials(token_path: Path):
    """Backward compatibility wrapper for load_credentials."""
    return load_credentials(token_path)


def _prompt_meeting_request() -> MeetingRequest:
    """Backward compatibility wrapper for prompt_meeting_request."""
    return prompt_meeting_request()


def _list_upcoming_events(service) -> None:
    """Backward compatibility wrapper for list_upcoming_events."""
    return list_upcoming_events(service)


def _create_event(service, meeting: MeetingRequest) -> dict:
    """Backward compatibility wrapper for create_event."""
    return create_event(service, meeting)


def _delete_event(service, event_id: str) -> None:
    """Backward compatibility wrapper for delete_event."""
    return delete_event(service, event_id)


def run_demo() -> None:
    token_path = Path(os.environ.get("CHRONOLOCK_GOOGLE_TOKEN_PATH", DEFAULT_TOKEN_PATH))
    credentials = _load_credentials(token_path)

    service = build("calendar", "v3", credentials=credentials)
    _list_upcoming_events(service)

    meeting = _prompt_meeting_request()
    event = _create_event(service, meeting)
    print("Created meeting:")
    print(f"- ID: {event.get('id')}")
    print(f"- Summary: {event.get('summary')}")
    print(f"- Starts: {event.get('start', {}).get('dateTime')}")
    print(f"- Ends: {event.get('end', {}).get('dateTime')}")

    delete_choice = input("Delete the demo meeting now? (y/N) ").strip().lower()
    if delete_choice == "y":
        _delete_event(service, event["id"])
        print("Deleted the demo meeting.")
    else:
        print("Left the meeting on your calendar.")


if __name__ == "__main__":
    run_demo()
