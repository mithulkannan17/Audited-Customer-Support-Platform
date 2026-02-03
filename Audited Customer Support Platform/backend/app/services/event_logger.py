from app.db import events_col 
from app.models.event import ConversationEvent

async def log_event(event: ConversationEvent):
    await events_col.insert_one(event.dict())