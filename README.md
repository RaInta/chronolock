# ChronoLock

Lock in time. Unlock expertise on an expert's calendar.

ChronoLock is a lightweight service for **locking, selling, and releasing time** on a personal calendar.

It enables individuals to advertise availability, accept payment via **x402**, and automatically convert paid bookings into confirmed calendar events. This is with Google Calendar initially, but designed to be calendar-agnostic.

Your time is valuable. So value it! ChronoLock treats time as an ownable resource:
- Availability is discoverable
- Access is managed
- Payment is atomic
- Booking is frictionless

No marketplaces, no intermediaries, and **no subscriptions**.  
Instead, paid access to attention, expertise, or presence at a fair market rate.

## Core ideas

- **Time as a resource**: availability is published, not negotiated. OK, maybe it can be negotiated
- **Payment-gated access**: slots unlock only after escrow deposit. Payment is only made once the calendar event has occurred
- **Hold and confirm semantics**: temporary locks prevent double-booking
- **Minimal trust surface**: calendars remain the source of truth
- **Composable by design**: works with agents, MCP tools, and automation

ChronoLock is intended as infrastructure, not a platform.

## Why ChronoLock exists

Time is the scarcest resource in modern knowledge work, yet it’s still exchanged informally, inefficiently, and without clear boundaries.

ChronoLock exists to make **access to time explicit and valued fairly**.

It lets people publish availability, set a price for their attention, and rely on a formal agreement to enforce fairness, commitment, and respect. Payment becomes the signal of intent.

ChronoLock is about making the meetings **deliberate and accountable**.

## Demo: advertise availability + tiers

This repo includes a small FastAPI demo that publishes availability and the tiered offerings
outlined in `ILLUSTRATION.md`. It does **not** integrate with Google Calendar yet; instead it
returns sample availability and a placeholder x402 payment request to show the shape of the
workflow.

### Run the demo

```bash
uvicorn chronolock.app:app --reload --port 8000
```

### Key endpoints

```bash
# List tiers (Bronze/Silver/Gold)
curl http://localhost:8000/tiers

# List advertised availability slots
curl http://localhost:8000/availability

# Place a hold for a tier + slot (returns x402-style payment info)
curl -X POST http://localhost:8000/holds \
  -H "Content-Type: application/json" \
  -d '{"tier_id":"silver","slot_id":"slot-1"}'

# Confirm a hold (simulates payment confirmation -> booked event)
curl -X POST http://localhost:8000/holds/<hold_id>/confirm
```

## Demo: Google Calendar booking (read + write)

This interactive script uses the Google Calendar API with read/write scope to list upcoming
events, create a meeting, and optionally delete it at the end. Credentials are supplied via
environment variables or a hidden prompt.

### Prerequisites

1. Create an OAuth client in the Google Cloud console (Desktop app).
2. Download the client secrets JSON.

### Run the demo

```bash
export CHRONOLOCK_GOOGLE_CLIENT_SECRETS_PATH="/path/to/client_secret.json"
python -m chronolock.demos.google_calendar_demo
```

You can also supply the JSON directly (hidden input):

```bash
export CHRONOLOCK_GOOGLE_CLIENT_SECRETS_JSON='{"installed":{...}}'
python -m chronolock.demos.google_calendar_demo
```

The script will prompt for:
- Meeting name
- Start time (e.g. `2025-01-31 14:00`)
- Duration in minutes

It will create the event and ask if you want to delete it before exiting.
