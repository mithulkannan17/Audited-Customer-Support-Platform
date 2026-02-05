from app.db import events_col

async def calculate_irr(conversation_id: str) -> float:
    reopen_count  = await events_col.count_documents({
        "conversation_id": conversation_id,
        "event_type": "TICKET_REOPENED"
    })

    # v0 heuristic 
    if reopen_count == 0:
        return 0.1
    if reopen_count == 1:
        return 0.6
    return 0.9

