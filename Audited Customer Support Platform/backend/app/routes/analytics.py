from fastapi import APIRouter, Depends
from app.services.agent_leaderboard import (
    generate_leaderboard,
    failure_breakdown,
    governance_summary,
)
from app.security.dependencies import require_role
from app.security.roles import Role
from app.db import events_col

router = APIRouter()


@router.get("/analytics/leaderboard")
async def leaderboard(
    role=Depends(require_role(Role.ADMIN, Role.QA))
):
    return await generate_leaderboard()


@router.get("/analytics/agents/{agent_id}/failures")
async def agent_failures(
    agent_id: str,
    role=Depends(require_role(Role.ADMIN, Role.QA))
):
    return await failure_breakdown(agent_id)


@router.get("/analytics/governance-summary")
async def summary(
    role=Depends(require_role(Role.ADMIN, Role.QA))
):
    return await governance_summary()


@router.get("/analytics/risk-trends")
async def risk_trends(
    role=Depends(require_role(Role.ADMIN, Role.QA))
):
    pipeline = [
        {
            "$match": {
                "event_type": {
                    "$in": [
                        "CATASTROPHIC_FAILURE",
                        "FALSE_POSITIVE_DETECTED",
                        "TICKET_REOPENED",
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
                            "date": "$created_at",
                        }
                    },
                    "type": "$event_type",
                },
                "count": {"$sum": 1},
            }
        },
        {"$sort": {"_id.day": 1}},
    ]

    results = []
    async for r in events_col.aggregate(pipeline):
        results.append(
            {
                "day": r["_id"]["day"],
                "event_type": r["_id"]["type"],
                "count": r["count"],
            }
        )

    return results
