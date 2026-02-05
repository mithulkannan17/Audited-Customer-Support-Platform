from app.db import events_col

async def detect_recovery(conversation_id: str) -> bool:

    events = []
    async for e in events_col.find(
        {"conversation_id": conversation_id},
        sort=[("created_at", 1)]
    ):
        events.append(e["event_type"])

    if "CCS_DETECTED" in events and "TICKET_REOPENED" in events:
        if "TICKET_PROVISIONALLY_RESOLVED" in events:
            return True
        

    return False
