from app.db import events_col

SUCCESS_WEIGHT = 10
CCS_PENALTY = 5
FALSE_CONFIDENCE_PENALTY  = 8
IRR_COST_WEIGHT = 12
RECOVERY_BONUS = 6
CATASTROPHIC_PENALTY = 40

async def calculate_agent_score(agent_id: str):

    cursor = events_col.find({
        "payload.agent_id": agent_id
    })

    successes = 0
    ccs_count = 0
    false_confidence = 0
    irr_prenalty = 0
    recovery = 0
    catastrophic = 0

    async for event in cursor:

        event_type = event["event_type"]
        payload = event.get("payload", {})

        if event_type ==  "TICKET_PROVISIONALLY_RESOLVED":
            successes += 1
            
        if event_type == "CCS_DETECTED":
            ccs_count += 1

        if event_type == "FALSE_POSITIVE_DETECTED":
            ccs_count += 1

        if event_type == "IRR_ESTIMATED":
            irr_prenalty += payload.get("irr", 0)

        if event_type == "RECOVERY_SUCCESS":
            recovery += 1

        if event_type == "CATASTROPHIC_FAILURE":
            catastrophic += 1

    score = (
        successes * SUCCESS_WEIGHT
        - ccs_count * CCS_PENALTY
        - false_confidence * FALSE_CONFIDENCE_PENALTY
        - irr_prenalty * IRR_COST_WEIGHT
        + recovery * RECOVERY_BONUS
        - catastrophic * CATASTROPHIC_PENALTY
    )

    return {
        "agent_id": agent_id,
        "score": round(score, 2),
        "successes": successes,
        "ccs": ccs_count,
        "false_confidence": false_confidence,
        "recovery": recovery,
        "catastrophic_failures": catastrophic
    }