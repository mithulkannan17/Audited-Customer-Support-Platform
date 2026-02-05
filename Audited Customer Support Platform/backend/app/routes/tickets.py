from fastapi import APIRouter, HTTPException
from app.db import tickets_col
from app.models.ticket import SupportTicket
from app.models.event import ConversationEvent
from app.services.event_logger import log_event
from app.services.quality_engine import run_quality_checks

router = APIRouter()

AGENT_ID = "agent_v1"


@router.post("/tickets")
async def create_ticket(ticket: SupportTicket):
    await tickets_col.insert_one(ticket.dict())

    await log_event(
        ConversationEvent(
            conversation_id=ticket.id,
            event_type="TICKET_CREATED",
            payload={"order_id": ticket.order_id}
        )
    )

    return ticket


@router.post("/tickets/{ticket_id}/close")
async def close_ticket(ticket_id: str):

    result = await tickets_col.update_one(
        {"id": ticket_id},
        {"$set": {"status": "PROVISIONALLY_RESOLVED"}}
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Ticket not found")

    await log_event(
        ConversationEvent(
            conversation_id=ticket_id,
            event_type="TICKET_PROVISIONALLY_RESOLVED",
            payload={"agent_id": AGENT_ID}
        )
    )

    await run_quality_checks(ticket_id)

    return {"status": "provisionally_resolved"}


@router.post("/tickets/{ticket_id}/reopen")
async def reopen_ticket(ticket_id: str):

    result = await tickets_col.update_one(
        {"id": ticket_id},
        {"$set": {"status": "REOPENED"}}
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Ticket not found")

    await log_event(
        ConversationEvent(
            conversation_id=ticket_id,
            event_type="TICKET_REOPENED",
            payload={"agent_id": AGENT_ID}
        )
    )

    return {"status": "reopened"}
