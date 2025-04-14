from pydantic import BaseModel, HttpUrl
from typing import List


class ScheduleItem(BaseModel):
    order: int
    name: str
    description: str
    image: HttpUrl


class DaySchedule(BaseModel):
    day: int
    schedules: List[ScheduleItem]


class ScheduleResponse(BaseModel):
    title: str
    days: List[DaySchedule]
