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