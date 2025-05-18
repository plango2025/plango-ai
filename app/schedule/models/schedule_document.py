from pydantic import BaseModel, Field
from typing import List
from datetime import datetime, timedelta, timezone

from app.schedule.schemas.schedule import Schedule
from app.schedule.schemas.schedule_create_request import ScheduleCreateRequest

from typing import Optional


class ScheduleDocument(BaseModel):
    # 일정 ID
    schedule_id: str

    # 소유자 ID
    owner: Optional[str] = None

    # 요청 파라미터
    parameters: ScheduleCreateRequest

    # 생성된 일정
    schedule: Schedule

    # 고정 장소 이름 리스트
    pinned_places: List[str] = Field(default_factory=list)

    # 제외 장소 이름 리스트
    banned_places: List[str] = Field(default_factory=list)

    # 유저 피드백 내역
    feedback_history: List[str] = Field(default_factory=list)

    # 생성일
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    # 만료일 (기본값: 24시간 뒤)
    expires_at: Optional[datetime] = Field(default_factory=lambda: datetime.now(timezone.utc) + timedelta(hours=24))
