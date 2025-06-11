from app.schedule.schemas.schedule import Schedule
from typing import List, Optional
from pydantic import BaseModel
from app.schedule.schemas.schedule_create_request import Place

class ScheduleParameters(BaseModel):
    required_places: Optional[List[Place]]
    destination: Optional[str]
    duration: Optional[int]
    companion: Optional[str]
    style: Optional[str]
    schedule_count: Optional[int]
    budget: Optional[int]
    extra: Optional[str]

class ScheduleReadResponse(BaseModel):
    schedule_id: str  # 일정 ID
    schedule: Schedule  # 여행 일정
    parameters: ScheduleParameters  # 여행 일정 생성에 사용된 파라미터들