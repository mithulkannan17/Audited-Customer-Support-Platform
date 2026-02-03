from motor.motor_asyncio import AsyncIOMotorClient
import os

MONGO_URI = os.getenv("mongodb+srv://mithulkannan5_db_user:Mithulkannan@new.5vp1oyk.mongodb.net/?appName=New")

client = AsyncIOMotorClient(MONGO_URI)
db = client["ai_support_platform"]

products_col = db["products"]
orders_col = db["orders"]
tickets_col = db["tickets"]
events_col = db["conversation_events"]