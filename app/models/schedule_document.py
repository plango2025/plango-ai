from pydantic import BaseModel, Field
from typing import List
from datetime import datetime, timedelta, timezone

from app.schemas.schedule import Schedule
from app.schemas.schedule_request import ScheduleRequest


class ScheduleDocument(BaseModel):
    schedule_id: str                                # 일정 ID
    parameters: ScheduleRequest                     # 요청 파라미터
    schedule: Schedule                              # 일정
    pinned_places: List[str] = Field(default_factory=list)      # 고정 장소 이름 리스트
    banned_places: List[str] = Field(default_factory=list)      # 제외 장소 이름 리스트
    feedback_history: List[str] = Field(default_factory=list)   # 유저 피드백 내역
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))    # 생성일
    # created_at 필드가 24시간 후에 만료되도록 설정
    expires_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc) + timedelta(hours=24))  # 만료일
    