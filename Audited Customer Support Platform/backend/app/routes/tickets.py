from fastapi import APIRouter
from app.db import tickets_col
from app.models.ticket import SupportTicket
from app.models.event import ConversationEvent
from app.services.event_logger import log_event

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


