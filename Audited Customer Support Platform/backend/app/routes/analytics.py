from fastapi import APIRouter
from app.services.agent_leaderboard import generate_leaderboard
from app.services.agent_leaderboard import failure_breakdown
from app.services.agent_leaderboard import governance_summary


router = APIRouter()

@router.get("/analytics/leaderboard")
async def leaderboard():
    return await generate_leaderboard()

@router.get("/analytics/agents/{agent_id}/failures")
async def agent_failures(agent_id: str):
    return await failure_breakdown(agent_id)

@router.get("/analytics/governance-summary")
async def summary():
    return await governance_summary()

@router.get("/analytics/risk-trends")
async def risk_trends():
    from app.db import events_col

    pipeline = [
        {
            "$match": {
                "event_type": {
                    "$in": [
                        "CATASTROPHIC_FAILURE",
                        "FALSE_POSITIVE_DETECTED",
                        "TICKET_REOPENED"
                    ]
                }
            }
        },
        {
            "$group": {
                "_id": {
                    "day": {
                        "$dateToString": {
                            "format": "%Y-%m-%d",
                            "date": "$create_at"
                        }
                    },
                    "type": "$event_type"
                },
                "count": {"$sum": 1}
            }
        },
        {
            "$sort": {"_id.day": 1}
        }
    ]

    results = []
    async for r in events_col.aggregate(pipeline):
        results.append({
            "day": r["_id"]["day"],
            "event_type": r["id"]["type"],
            "count": r["count"]
        })

    return results