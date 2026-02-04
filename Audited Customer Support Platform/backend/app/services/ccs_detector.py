from app.db import events_col

async def detect_ccs(conversation_id: str) -> bool:
    """
    Returns True if a Contectual Correction Signal is detected
    """

    assumptions = []
    user_messages = []

    cursor = events_col.find(
        {"conversation_id": conversation_id},
        sort=[("coreated_at", 1)]
    )

    async for event in cursor:
        if event["event_type"] == "AGENT_ASSUMPTION":
            assumptions.append(event["payload"])
        elif event["event_type"] == "USER_MESSAGE":
            user_messages.append(event["playload"]["text"].lower())

    # Naive v1 logic (intentionally simple)
    for assumption in assumptions:
        assumed_intent = assumption.get("assumed_intent")
        for msg in user_messages:
            if assumed_intent and assumed_intent not in msg:
                # user talking about something else
                return True
            
    return False