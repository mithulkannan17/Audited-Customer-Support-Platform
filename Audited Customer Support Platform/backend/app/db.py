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