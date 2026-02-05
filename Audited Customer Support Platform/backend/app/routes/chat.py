from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.services.event_logger import log_event
from app.models.event import ConversationEvent
from datetime import datetime

router = APIRouter()

@router.websocket("/ws/chat/{ticket_id}")
async def chat_socket(websocket: WebSocket, ticket_id: str):
    await websocket.accept()

    try:
        while True:
            user_message = await websocket.receive_text()

            # Log user message
            await log_event(
                ConversationEvent(
                    conversation_id=ticket_id,
                    event_type="USER_MESSAGE",
                    payload={"text": user_message}
                )
            )

            # Check for explicit escalation
            if user_message.lower() in ["human", "manager", "stop"]:
                await log_event(
                    ConversationEvent(
                        conversation_id=ticket_id,
                        event_type="EXPLICIT_ESCALATION",
                        payload={"trigger": user_message}
                    )
                )
                await websocket.send_text(
                    "I'm escalating this conversation to a human agent."
                )
                break

            # Mock agent logic (Intentionally Dumb)
            agent_reply = f"I understand your issue regarding: '{user_message}'. Let me check that for you."

            # Log agent assumption (even if trivial)

            await log_event(
                ConversationEvent(
                    conversation_id=ticket_id,
                    event_type="AGENT_CONFIDENCE",
                    payload={
                        "confidence": 0.42,
                        "basis": "low context"
                    }
                )
            )

            # agent assumption
            await log_event(
                ConversationEvent(
                    conversation_id=ticket_id,
                    event_type="AGENT_ASSUMPTION",
                    payload={
                        "assumed_intent": "order_delivery_issue",
                        "assumed_entity": "order",
                        "confidence_score": "heuristic"
                    }
                )
            )

            # Log agent messsage
            await log_event(
                ConversationEvent(
                    conversation_id=ticket_id,
                    event_type="AGENT_MESSAGE",
                    payload={"text": agent_reply}
                )
            )

            await websocket.send_text(agent_reply)

    except WebSocketDisconnect:
        await log_event(
            ConversationEvent(
                conversation_id=ticket_id,
                event_type="CONNECTION_CLOSED",
                payload={"timestamp": datetime.utcnow().isoformat()}
            )
        )