from pydantic import BaseModel, Field
from typing import List, Optional

class Place(BaseModel):
    name: str = Field(description="장소 이름")
    address: str = Field(description="장소 주소")


class ScheduleCreateRequest(BaseModel):
    required_places: Optional[List[Place]] = Field(description="필수 코스")
    destination: Optional[str] = Field(description="여행지")
    duration: Optional[str] = Field(description="여행 기간")
    companion: Optional[str] = Field(description="동행자")
    style: Optional[str] = Field(description="여행 스타일")
    schedule_count: Optional[int] = Field(description="(하루 당) 일정 개수")
    budget: Optional[int] = Field(description="예산 (만원 단위)")
    extra: Optional[str] = Field(description="기타 고려 사항")
