from fastapi import APIRouter, HTTPException
from app.db import orders_col
from app.models.order import Order
from app.models.event import ConversationEvent
from app.services.event_logger import log_event

router = APIRouter()

@router.post("/orders")
async def create_order(order: Order):
    existing = await orders_col.find_one({"id": order.id})
    if existing:
        raise HTTPException(status_code=400, detail="Order already exists")
    
    await orders_col.insert_one(order.dict())

    await log_event(
        ConversationEvent(
            conversation_id=order.id,
            event_type="ORDER_CREATED",
            payload={
                "order_id": order.id,
                "status": order.status,
                "items": [item.dict() for item in order.items]
            }
        )
    )

    return order


@router.get("/orders/{order_id}")
async def get_order(order_id: str):
    order = await orders_col.find_one({"id": order_id})
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    order["_id"] = str(order["_id"])
    return order
