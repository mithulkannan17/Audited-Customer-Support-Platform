from fastapi import FastAPI
from app.routes import products, tickets, orders, chat
from dotenv import load_dotenv

load_dotenv()
app = FastAPI(title="AI Audited Support Platform")

app.include_router(products.router)
app.include_router(tickets.router)
app.include_router(orders.router)
app.include_router(chat.router)