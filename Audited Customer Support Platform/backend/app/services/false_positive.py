from app.db import events_col
from datetime import timedelta

async def detect_false_positive(conversation_id: str) -> bool:
    events = []
    async for e in events_col.find(
        {"conversation_id": conversation_id},
        sort=[("created_at", 1)]
    ):
        events.append(e)

    # Rule 1: CCS exists
    if any(e["event_type"] == "CCS_DETECTED" for e in events):
        return True
    
    # Rule 2: Closed without confirmation
    has_confirmation = any(
        e["event_type"] == "AGENT_MESSAGE" and 
        "anything else" in e["payload"].get("text", "").lower()
        for e in events
    )

    return not has_confirmation

