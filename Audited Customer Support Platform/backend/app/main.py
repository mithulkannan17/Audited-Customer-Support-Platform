from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from app.routes import products, tickets, orders, chat, agents, analytics
from dotenv import load_dotenv
from app.db import init_indexes


load_dotenv()
app = FastAPI(title="AI Audited Support Platform")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    await init_indexes()
    print("AI Audit support Platform")

app.include_router(products.router, prefix="/api/v1")
app.include_router(tickets.router, prefix="/api/v1")
app.include_router(orders.router, prefix="/api/v1")
app.include_router(agents.router, prefix="/api/v1")
app.include_router(analytics.router, prefix="/api/v1")
app.include_router(chat.router)