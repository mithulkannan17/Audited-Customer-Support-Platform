from fastapi import APIRouter
from app.services.agent_scoring import calculate_agent_score

router = APIRouter()

@router.get("/agents/{agent_id}/score")
async def get_agent_score(agent_id: str):
    return await calculate_agent_score(agent_id)