import uuid

from app.schedule.repositories.schedule_repository import ScheduleRepository
from app.schedule.models.schedule_document import ScheduleDocument
from app.schedule.schemas.schedule_create_request import ScheduleCreateRequest
from app.schedule.schemas.schedule_create_response import ScheduleCreateResponse
from app.schedule.schemas.schedule_feedback_request import ScheduleFeedbackRequest
from app.schedule.services.schedule_ai_service import ScheduleAIService

from app.schedule.repositories.schedule_repository import schedule_repository
from app.schedule.services.schedule_ai_service import schedule_ai_service

from fastapi import HTTPException
from typing import List, Optional


class ScheduleService:
    def __init__(
        self,
        schedule_repository: ScheduleRepository,
        schedule_ai_service: ScheduleAIService,
    ):
        self.schedule_repository = schedule_repository
        self.schedule_ai_service = schedule_ai_service

    async def create_schedule(self, schedule_request: ScheduleCreateRequest) -> ScheduleCreateResponse :
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

        schedule_response = ScheduleCreateResponse(
            schedule_id=schedule_id,
            schedule=schedule
        )
        
        # 일정 응답 반환        
        return schedule_response

    async def pin_places(self, schedule_id: str, places: List[str], user_id: Optional[str]) -> None:
        """
        고정 장소를 추가합니다.
        """

        # 문서 조회
        document = self.schedule_repository.find_by_id(schedule_id)
        if not document:
            raise HTTPException(status_code=404, detail="존재하지 않는 일정입니다.")

        # 다른 사람의 일정에 접근한 경우 예외 처리
        if document.owner and document.owner != user_id:
            raise HTTPException(status_code=403, detail="다른 사용자의 일정에는 접근할 수 없습니다.")

        # document에 고정 장소 추가
        success = self.schedule_repository.add_pinned_places(schedule_id, places)

        # 성공 여부 확인
        if not success:
            raise HTTPException(status_code=404, detail=f"존재하지 않는 일정입니다.")

    async def ban_places(self, schedule_id: str, places: List[str], user_id: Optional[str]) -> None:
        """
        제외 장소를 추가합니다.
        """

        # 문서 조회
        document = self.schedule_repository.find_by_id(schedule_id)
        if not document:
            raise HTTPException(status_code=404, detail="존재하지 않는 일정입니다.")

        # 다른 사람의 일정에 접근한 경우 예외 처리
        if document.owner and document.owner != user_id:
            raise HTTPException(status_code=403, detail="다른 사용자의 일정에는 접근할 수 없습니다.")

        # document에 제외 장소 추가
        success = self.schedule_repository.add_banned_places(schedule_id, places)

        # 성공 여부 확인
        if not success:
            raise HTTPException(status_code=404, detail=f"존재하지 않는 일정입니다.")

    async def keep_schedule(self, schedule_id: str, user_id: str) -> None:
        """
        일정을 보관합니다.
        """

        # 유효성 검사
        if not schedule_id:
            raise HTTPException(status_code=400, detail="schedule_id를 입력해주세요.")
        if not user_id:
            raise HTTPException(status_code=400, detail="user_id를 입력해주세요.")

        # 문서 조회
        document = self.schedule_repository.find_by_id(schedule_id)
        if not document:
            raise HTTPException(status_code=404, detail="존재하지 않는 일정입니다.")

        # 이미 보관된 일정인 경우 바로 나가기
        if document.owner == user_id and not document.expires_at:
            return

        # 다른 사람의 일정에 접근한 경우 예외 처리
        if document.owner and document.owner != user_id:
            raise HTTPException(status_code=403, detail="다른 사용자의 일정에는 접근할 수 없습니다.")

        # 소유자 설정
        owner_update_success = self.schedule_repository.set_owner(schedule_id, user_id)

        # 만료 제거
        ttl_removal_success = self.schedule_repository.remove_ttl(schedule_id)

        # 디버깅 용 출력
        document = self.schedule_repository.find_by_id(schedule_id)

        # 실패 시 에러 처리
        if not owner_update_success or not ttl_removal_success:
            raise HTTPException(status_code=500, detail="일정 보관 처리 중 오류가 발생했습니다.")
    
    async def apply_feedback(self, schedule_id: str, request: ScheduleFeedbackRequest) -> ScheduleCreateResponse:
        """
        AI를 이용하여 일정에 피드백을 적용합니다.
        """

        # 입력값 유효성 검사
        if not schedule_id:
            raise HTTPException(status_code=400, detail="schedule_id를 입력해주세요.")
        if not request.feedback:
            raise HTTPException(status_code=400, detail="feedback 내용을 입력해주세요.")

        # 문서 조회
        document = self.schedule_repository.find_by_id(schedule_id)
        if not document:
            raise HTTPException(status_code=404, detail="존재하지 않는 일정입니다.")

        # 다른 사람의 일정에 접근한 경우 예외 처리
        if document.owner and document.owner != request.user_id:
            raise HTTPException(status_code=403, detail="다른 사용자의 일정에는 접근할 수 없습니다.")

        # AI 일정 피드백
        new_schedule = await self.schedule_ai_service.update_schedule_with_feedback(
            parameters=document.parameters,
            schedule=document.schedule,
            pinned_places=document.pinned_places,
            banned_places=document.banned_places,
            new_feedback=request.feedback,
            feedback_history=document.feedback_history
        )

        # 새로운 일정 저장
        self.schedule_repository.update_schedule(
            schedule_id=schedule_id,
            new_schedule=new_schedule
        )

        # 피드백 내역 추가
        self.schedule_repository.add_feedback(
            schedule_id=schedule_id,
            feedback=request.feedback
        )

        # 수정된 일정 반환
        return ScheduleCreateResponse(
            schedule_id=schedule_id,
            schedule=new_schedule
        )

    async def recreate_schedule(self, schedule_id: str, user_id: Optional[str]) -> ScheduleCreateResponse:
        """
        기존 일정 설정 정보를 바탕으로 새로운 일정을 생성합니다.
        """

        # 입력값 유효성 검사
        if not schedule_id:
            raise HTTPException(status_code=400, detail="schedule_id를 입력해주세요.")

        # 문서 조회
        document = self.schedule_repository.find_by_id(schedule_id)
        if not document:
            raise HTTPException(status_code=404, detail="존재하지 않는 일정입니다.")
        
        # 다른 사람의 일정에 접근한 경우 예외 처리
        if document.owner and document.owner != user_id:
            raise HTTPException(status_code=403, detail="다른 사용자의 일정에는 접근할 수 없습니다.")
        
        # AI 일정 재생성
        new_schedule = await self.schedule_ai_service.regenerate_schedule(
            parameters=document.parameters,
            pinned_places=document.pinned_places,
            banned_places=document.banned_places,
            feedback_history=document.feedback_history
        )

        # 새로운 일정 저장
        self.schedule_repository.update_schedule(
            schedule_id=schedule_id,
            new_schedule=new_schedule
        )

        # 재생성된 일정 반환
        return ScheduleCreateResponse(
            schedule_id=schedule_id,
            schedule=new_schedule
        )



# 전역 인스턴스 (싱글턴처럼 사용)
schedule_service = ScheduleService(
    schedule_repository=schedule_repository,
    schedule_ai_service=schedule_ai_service,
)
