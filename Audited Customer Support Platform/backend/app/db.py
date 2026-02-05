from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv


load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

if not MONGO_URI:
    raise ValueError("No MONGO_URI found in environment variables")

client = AsyncIOMotorClient(MONGO_URI)
db = client["ai_support_platform"]

products_col = db["products"]
orders_col = db["orders"]
tickets_col = db["tickets"]
events_col = db["conversation_events"]


async def init_indexes():
    await events_col.create_index("conversation_id")
    await events_col.create_index([("conversation_id", 1), ("created_at", 1)])
    await events_col.create_index("event_type")