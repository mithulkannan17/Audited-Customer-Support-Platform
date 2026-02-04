from app.models.event import ConversationEvent
from app.services.event_logger import log_event
from app.services.ccs_detector import detect_ccs

async def run_quality_checks(converstion_id: str):
    ccs_detected = await detect_ccs(converstion_id)

    if ccs_detected:
        await log_event(
            ConversationEvent(
                converstion_id=converstion_id,
                event_type="CCS_DETECTED",
                payload={"severity": "high"}
            )
        )