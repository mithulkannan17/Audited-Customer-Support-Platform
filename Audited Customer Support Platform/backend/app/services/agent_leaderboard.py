from app.db import events_col
from app.services.agent_scoring import calculate_agent_score

async def get_all_agents():

    agent_ids = await events_col.distinct(
    "payload.agent_id",
    {"payload.agent_id": {"$exists": True}}
)


    # Remove None or empty values
    return [a for a in agent_ids if a]

async def generate_leaderboard():

    agents = await get_all_agents()

    leaderboard = []

    for agent in agents:
        score = await calculate_agent_score(agent)
        leaderboard.append(score)

    leaderboard.sort(key=lambda x: x["score"], reverse=True)

    return leaderboard

async def failure_breakdown(agent_id: str):

    pipeline = [
        {"$match": {"payload.agent_id": agent_id}},
        {"$group": {
            "_id": "$event_type",
            "count": {"$sum": 1}
        }}
    ]

    results = []
    async for r in events_col.aggregate(pipeline):
        results.append({
            "event_type": r["_id"],
            "count": r["count"]
        })

    return results

async def governance_summary():

    catastrophic = await events_col.count_documents({
        "event_type": "CATASTROPHIC_FAILURE"
    })

    recoveries = await events_col.count_documents({
        "event_type": "RECOVERY_SUCCESS"
    })

    exclusions = await events_col.count_documents({
        "event_type": "EXCLUDE_FROM_TRAINING"
    })

    return{
        "catastrophic_failures": catastrophic,
        "recoveries": recoveries,
        "training_exclusions": exclusions
    }