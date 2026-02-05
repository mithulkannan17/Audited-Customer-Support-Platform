from app.models.event import ConversationEvent
from app.services.event_logger import log_event
from app.services.ccs_detector import detect_ccs
from app.services.false_positive import detect_false_positive
from app.services.irr_detector import calculate_irr
from app.db import events_col


async def event_exists(conversation_id: str, event_type: str) -> bool:
    return await events_col.find_one({
        "conversation_id": conversation_id,
        "event_type": event_type
    }) is not None


async def run_quality_checks(conversation_id: str):
    print("QUALITY ENGINE RUNNING FOR:", conversation_id)
    # CCS 
    if not await event_exists(conversation_id, "CCS_DETECTED"):
        ccs_detected = await detect_ccs(conversation_id)

        if ccs_detected:
            await log_event(
                ConversationEvent(
                    conversation_id=conversation_id,
                    event_type="CCS_DETECTED",
                    payload={"severity": "high"}
                )
            )

    # FALSE POSITIVE 
    if not await event_exists(conversation_id, "FALSE_POSITIVE_DETECTED"):
        false_positive = await detect_false_positive(conversation_id)

        if false_positive:
            await log_event(
                ConversationEvent(
                    conversation_id=conversation_id,
                    event_type="FALSE_POSITIVE_DETECTED",
                    payload={"reason": "unconfirmed_or_corrected"}
                )
            )
    else:
        false_positive = True  # If already detected earlier

    # IRR 
    if not await event_exists(conversation_id, "IRR_ESTIMATED"):
        irr = await calculate_irr(conversation_id)

        await log_event(
            ConversationEvent(
                conversation_id=conversation_id,
                event_type="IRR_ESTIMATED",
                payload={"irr": irr}
            )
        )
    else:
        irr = 0.0  # fallback, safe

    # TRAINING EXCLUSION 
    if (false_positive or irr > 0.5) and not await event_exists(
        conversation_id, "EXCLUDE_FROM_TRAINING"
    ):
        await log_event(
            ConversationEvent(
                conversation_id=conversation_id,
                event_type="EXCLUDE_FROM_TRAINING",
                payload={"reason": "risk_detected"}
            )
        )
