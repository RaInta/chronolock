from __future__ import annotations

from datetime import UTC, datetime, timedelta
from typing import Literal
from uuid import uuid4

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(title="ChronoLock Demo", version="0.1.0")


class Tier(BaseModel):
    id: Literal["bronze", "silver", "gold"]
    name: str
    price_usd: int
    duration_minutes: int
    summary: str
    constraints: list[str]


class AvailabilitySlot(BaseModel):
    id: str
    starts_at: datetime
    ends_at: datetime
    status: Literal["open", "held", "booked"] = "open"


class HoldRequest(BaseModel):
    tier_id: Literal["bronze", "silver", "gold"]
    slot_id: str


class HoldResponse(BaseModel):
    hold_id: str
    tier: Tier
    slot: AvailabilitySlot
    payment: dict[str, str]


class ConfirmResponse(BaseModel):
    hold_id: str
    status: Literal["confirmed"]
    calendar_event: dict[str, str]


TIERS: dict[str, Tier] = {
    "bronze": Tier(
        id="bronze",
        name="Rubber Duck",
        price_usd=25,
        duration_minutes=10,
        summary="Quick clarification or sanity check.",
        constraints=["No prep", "No follow-ups", "No screen-share"],
    ),
    "silver": Tier(
        id="silver",
        name="Working Session",
        price_usd=120,
        duration_minutes=30,
        summary="Active problem-solving with direct answers.",
        constraints=["Limited prep", "One concrete outcome expected"],
    ),
    "gold": Tier(
        id="gold",
        name="Deep Consult",
        price_usd=400,
        duration_minutes=60,
        summary="Strategic advice with full attention.",
        constraints=["Review materials in advance", "May include follow-up notes"],
    ),
}

_base_start = datetime.now(tz=UTC).replace(minute=0, second=0, microsecond=0)
SLOTS: dict[str, AvailabilitySlot] = {
    f"slot-{index}": AvailabilitySlot(
        id=f"slot-{index}",
        starts_at=_base_start + timedelta(days=1, hours=index),
        ends_at=_base_start + timedelta(days=1, hours=index + 1),
    )
    for index in range(3)
}
HOLDS: dict[str, HoldResponse] = {}


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/tiers", response_model=list[Tier])
def list_tiers() -> list[Tier]:
    return list(TIERS.values())


@app.get("/availability", response_model=list[AvailabilitySlot])
def list_availability() -> list[AvailabilitySlot]:
    return list(SLOTS.values())


@app.post("/holds", response_model=HoldResponse)
def create_hold(request: HoldRequest) -> HoldResponse:
    tier = TIERS.get(request.tier_id)
    if not tier:
        raise HTTPException(status_code=404, detail="Tier not found.")
    slot = SLOTS.get(request.slot_id)
    if not slot:
        raise HTTPException(status_code=404, detail="Slot not found.")
    if slot.status != "open":
        raise HTTPException(status_code=409, detail="Slot is not available.")

    slot.status = "held"
    hold_id = uuid4().hex
    payment = {
        "protocol": "x402",
        "amount_usd": str(tier.price_usd),
        "asset": "USDC",
        "address": "0xDEMOADDRESS",
        "expires_at": (datetime.now(tz=UTC) + timedelta(minutes=15)).isoformat(),
    }
    hold = HoldResponse(hold_id=hold_id, tier=tier, slot=slot, payment=payment)
    HOLDS[hold_id] = hold
    return hold


@app.post("/holds/{hold_id}/confirm", response_model=ConfirmResponse)
def confirm_hold(hold_id: str) -> ConfirmResponse:
    hold = HOLDS.get(hold_id)
    if not hold:
        raise HTTPException(status_code=404, detail="Hold not found.")
    slot = SLOTS[hold.slot.id]
    slot.status = "booked"
    return ConfirmResponse(
        hold_id=hold_id,
        status="confirmed",
        calendar_event={
            "provider": "google",
            "event_id": f"demo-{hold_id}",
            "starts_at": slot.starts_at.isoformat(),
            "ends_at": slot.ends_at.isoformat(),
        },
    )
