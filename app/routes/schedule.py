from fastapi import APIRouter
from app.schemas.schedule_request import ScheduleRequest
from app.schemas.schedule_response import ScheduleResponse
from app.services.schedule_ai_service import generate_schedule

router = APIRouter(prefix="/api/schedules")

@router.post("/ai", response_model=ScheduleResponse, status_code=200)
async def create_ai_schedule(request: ScheduleRequest):
    return await generate_schedule(request)