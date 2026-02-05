from app.models.event import ConversationEvent
from app.services.event_logger import log_event
from app.services.ccs_detector import detect_ccs
from app.services.false_positive import detect_false_positive

async def run_quality_checks(conversation_id: str):
    ccs_detected = await detect_ccs(conversation_id)

    if ccs_detected:
        await log_event(
            ConversationEvent(
                conversation_id=conversation_id,
                event_type="CCS_DETECTED",
                payload={"severity": "high"}
            )
        )

    false_positive = await detect_false_positive(conversation_id)

    if false_positive:
        await log_event(
            ConversationEvent(
                conversation_id=conversation_id,
                event_type="FALSE_POSITIVE_DETECTED",
                payload={"reason": "unconfirmed_or_corrected"}
            )
        )