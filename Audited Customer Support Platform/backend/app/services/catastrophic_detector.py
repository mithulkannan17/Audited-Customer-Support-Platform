from app.db import events_col

async def detect_catastrophic_failure(conversation_id: str) -> bool:

    irr_event = await events_col.find_one({
        "conversation_id": conversation_id,
        "event_type": "IRR_ESTIMATED"
    })

    false_positive = await events_col.find_one({
        "conversation_id": conversation_id,
        "event_type": "FALSE_POSITIVE_DETECTED"
    })

    if not irr_event:
        return False
    
    irr = irr_event["payload"].get("irr", 0)

    return irr > 0.7 and false_positive is not None