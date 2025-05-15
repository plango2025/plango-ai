from fastapi import APIRouter

from app.schemas.schedule_request import ScheduleRequest
from app.schemas.schedule_response import ScheduleResponse
from app.schemas.pin_place_request import PinPlaceRequest
from app.schemas.ban_place_request import BanPlaceRequest

from app.services.schedule_service import schedule_service

router = APIRouter(prefix="/api/schedules")


@router.post("/ai", response_model=ScheduleResponse, status_code=200)
async def create_ai_schedule(request: ScheduleRequest):
    return await schedule_service.create_schedule(request)


@router.post("/{schedule_id}/places/pin", status_code=204)
async def pin_places(schedule_id: str, request: PinPlaceRequest):
    await schedule_service.pin_places(schedule_id, request.places)


@router.post("/{schedule_id}/places/ban", status_code=204)
async def ban_places(schedule_id: str, request: BanPlaceRequest):
    await schedule_service.ban_places(schedule_id, request.places)