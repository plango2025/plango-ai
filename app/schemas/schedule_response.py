from pydantic import BaseModel
from typing import List, Optional


class ScheduleItem(BaseModel):
    order: Optional[int]            # 순서
    name: Optional[str]             # 장소 이름
    description: Optional[str]      # 장소 설명
    image: Optional[str]            # 이미지 URL
    latitude: Optional[float]       # 위도
    longitude: Optional[float]      # 경도


class DaySchedule(BaseModel):
    day: Optional[int]              # 날짜
    schedules: List[ScheduleItem]   # 일정 목록


class ScheduleResponse(BaseModel):  
    title: Optional[str]            # 여행 제목
    days: List[DaySchedule]         # 여행 일정 목록
