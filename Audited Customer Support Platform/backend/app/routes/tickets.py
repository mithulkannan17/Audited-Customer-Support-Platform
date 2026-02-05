from fastapi import APIRouter
from app.db import tickets_col
from app.models.ticket import SupportTicket
from app.models.event import ConversationEvent
from app.services.event_logger import log_event
from app.services.quality_engine import run_quality_checks


router = APIRouter()

@router.post("/tickets")
async def create_ticket(ticket: SupportTicket):
    await tickets_col.insert_one(ticket.dict())

    await log_event(
        ConversationEvent(
            Conversation_id=ticket.id,
            event_type="TICKET_CREATED",
            payload={"order_id": ticket.order_id}
        )
    )

    return ticket

@router.post("/tickets/{ticket_id}/close")
async def close_ticket(ticket_id: str):
    await tickets_col.update_one(
        {"id": ticket_id},
        {"$set": {"status": "PROVISIONALLY_RESOLVED"}}
    )

    await log_event(
        ConversationEvent(
            Conversation_id=ticket_id,
            event_type="TICKET_PROVISIONALLY_RESOLVED",
            payload={}
        )
    )

    # Run quality intelligence AFTER closure
    await run_quality_checks(ticket_id)

    return {"status": "provisionally_resolved"}


@router.post("/tickets/{ticket_id}reopen")
async def reopen_ticket(ticket_id: str):
    await tickets_col.update_one(
        {"id": ticket_id},
        {"$set": {"status": "REOPENED"}}
    )

    await log_event(
        ConversationEvent(
            Conversation_id=ticket_id,
            event_type="TICKET_REOPENED",
            payload={}
        )
    )

    return {"status": "reopened"}
