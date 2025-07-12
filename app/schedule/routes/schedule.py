from fastapi import APIRouter, Body, Query

from app.schedule.schemas.schedule_create_request import ScheduleCreateRequest
from app.schedule.schemas.schedule_create_response import ScheduleCreateResponse
from app.schedule.schemas.pin_place_request import PinPlaceRequest
from app.schedule.schemas.ban_place_request import BanPlaceRequest
from app.schedule.schemas.schedule_feedback_request import ScheduleFeedbackRequest
from app.schedule.schemas.schedule_read_response import ScheduleReadResponse
from app.schedule.schemas.schedule_thumbnail_list import ScheduleThumbnailList

from app.schedule.services.schedule_service import schedule_service

from typing import Optional


router = APIRouter(prefix="/api/schedules")


@router.post("", response_model=ScheduleCreateResponse, status_code=200)
async def create_ai_schedule(request: ScheduleCreateRequest):
    return await schedule_service.create_schedule(request)


@router.patch("/{schedule_id}/places/pin", status_code=204)
async def pin_places(schedule_id: str, request: PinPlaceRequest):
    await schedule_service.pin_places(schedule_id, request.places, request.user_id)


@router.patch("/{schedule_id}/places/ban", status_code=204)
async def ban_places(schedule_id: str, request: BanPlaceRequest):
    await schedule_service.ban_places(schedule_id, request.places, request.user_id)


@router.patch("/{schedule_id}/keep", status_code=204)
async def keep_schedule(schedule_id: str, user_id: str = Body(..., embed=True)):
    await schedule_service.keep_schedule(schedule_id, user_id)


@router.patch("/{schedule_id}/feedback", response_model=ScheduleCreateResponse, status_code=200)
async def give_schedule_feedback(schedule_id: str, request: ScheduleFeedbackRequest):
    return await schedule_service.apply_feedback(schedule_id, request)


@router.patch("/{schedule_id}/recreate", response_model=ScheduleCreateResponse, status_code=200)
async def recreate_schedule(schedule_id: str, user_id: Optional[str] = Body(None, embed=True)):
    return await schedule_service.recreate_schedule(schedule_id, user_id)

@router.get("/{schedule_id}", response_model=ScheduleReadResponse, status_code=200)
async def read_schedule(schedule_id: str):
    return await schedule_service.get_schedule(schedule_id)

@router.get("", response_model=ScheduleThumbnailList, status_code=200)
async def read_schedules(user_id: Optional[str] = Query(None, description="유저 ID")):
    return ScheduleThumbnailList(data=await schedule_service.get_schedules_by_user_id(user_id))