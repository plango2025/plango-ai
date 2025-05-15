import uuid

from app.repositories.schedule_repository import ScheduleRepository
from app.models.schedule_document import ScheduleDocument
from app.schemas.schedule_request import ScheduleRequest
from app.schemas.schedule_response import ScheduleResponse
from app.services.schedule_ai_service import ScheduleAIService

from app.repositories.schedule_repository import schedule_repository
from app.services.schedule_ai_service import schedule_ai_service

from fastapi import HTTPException
from typing import List


class ScheduleService:
    def __init__(
        self,
        schedule_repository: ScheduleRepository,
        schedule_ai_service: ScheduleAIService,
    ):
        self.schedule_repository = schedule_repository
        self.schedule_ai_service = schedule_ai_service

    async def create_schedule(self, schedule_request: ScheduleRequest) -> ScheduleResponse :
        """
        AI를 통해 여행 일정을 생성하고, MongoDB에 저장합니다.
        TTL은 24시간으로 설정됩니다.
        """

        # AI를 통해 일정 생성
        schedule = await self.schedule_ai_service.generate_schedule(schedule_request)

        # 일정 ID 생성
        schedule_id = uuid.uuid4().hex

        # ScheduleDocument 생성
        document = ScheduleDocument(
            schedule_id=schedule_id,
            parameters=schedule_request,
            schedule=schedule
        )

        # MongoDB에 저장
        self.schedule_repository.save(document)

        schedule_response = ScheduleResponse(
            schedule_id=schedule_id,
            schedule=schedule
        )
        
        # 일정 응답 반환        
        return schedule_response

    async def pin_places(self, schedule_id: str, places: List[str]) -> None:
        """
        고정 장소를 추가합니다.
        """

        # document에 고정 장소 추가
        success = self.schedule_repository.add_pinned_places(schedule_id, places)

        # 성공 여부 확인
        if not success:
            raise HTTPException(status_code=404, detail=f"Schedule '{schedule_id}' not found.")

    async def ban_places(self, schedule_id: str, places: List[str]) -> None:
        """
        제외 장소를 추가합니다.
        """

        # document에 제외 장소 추가
        success = self.schedule_repository.add_banned_places(schedule_id, places)

        # 성공 여부 확인
        if not success:
            raise HTTPException(status_code=404, detail=f"Schedule '{schedule_id}' not found.")


# 전역 인스턴스 (싱글턴처럼 사용)
schedule_service = ScheduleService(
    schedule_repository=schedule_repository,
    schedule_ai_service=schedule_ai_service,
)
