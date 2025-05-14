import uuid

from app.repositories.schedule_repository import ScheduleRepository
from app.models.schedule_document import ScheduleDocument
from app.schemas.schedule_request import ScheduleRequest
from app.schemas.schedule_response import ScheduleResponse
from app.services.schedule_ai_service import ScheduleAIService

from app.repositories.schedule_repository import schedule_repository
from app.services.schedule_ai_service import schedule_ai_service


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
        print(document)

        # MongoDB에 저장
        self.schedule_repository.save(document)

        print("schedule type:", type(schedule))

        schedule_response = ScheduleResponse(
            schedule_id=schedule_id,
            schedule=schedule
        )
        print(schedule_response)
        
        # 일정 응답 반환        
        return schedule_response

# 전역 인스턴스 (싱글턴처럼 사용)
schedule_service = ScheduleService(
    schedule_repository=schedule_repository,
    schedule_ai_service=schedule_ai_service,
)
