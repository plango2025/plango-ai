from pymongo.collection import Collection
from pymongo import ASCENDING
from app.db.mongo import db
from app.schedule.models.schedule_document import ScheduleDocument
from app.schedule.schemas.schedule import Schedule
from typing import Optional

class ScheduleRepository:
    def __init__(self):
        self.collection: Collection = db["schedules"]

        # TTL 인덱스 생성 (created_at 기준)
        self.collection.create_index(
            [("expires_at", ASCENDING)],
            expireAfterSeconds=0,
            name="ttl_expires_at"
        )

    # 새 문서 저장
    def save(self, document: ScheduleDocument) -> None:
        self.collection.insert_one(document.model_dump())

    # 일정 ID로 조회
    def find_by_id(self, schedule_id: str) -> Optional[ScheduleDocument]:
        doc = self.collection.find_one({"schedule_id": schedule_id})
        return ScheduleDocument(**doc) if doc else None

    # 일정 ID로 삭제
    def delete_by_id(self, schedule_id: str) -> bool:
        result = self.collection.delete_one({"schedule_id": schedule_id})
        return result.deleted_count == 1

    # TTL 없애기 (expires_at 필드 제거 = 삭제 대상에서 제외)
    def remove_ttl(self, schedule_id: str) -> bool:
        result = self.collection.update_one(
            {"schedule_id": schedule_id},
            {"$set": {"expires_at": None}}
        )
        return result.modified_count == 1

    # 일정 소유자 설정
    def set_owner(self, schedule_id: str, user_id: str) -> bool:
        result = self.collection.update_one(
            {"schedule_id": schedule_id},
            {"$set": {"owner": user_id}}
        )
        return result.modified_count == 1
    
    # 일정 설정
    def update_schedule(self, schedule_id: str, new_schedule: Schedule) -> bool:
        result = self.collection.update_one(
            {"schedule_id": schedule_id},
            {"$set": {"schedule": new_schedule.model_dump()}}
        )
        return result.modified_count == 1

    
    # pinned_places에 장소 추가
    def add_pinned_places(self, schedule_id: str, place_names: list[str]) -> bool:
        result = self.collection.update_one(
            {"schedule_id": schedule_id},
            {"$addToSet": {"pinned_places": {"$each": place_names}}}
        )
        return result.matched_count == 1

    # banned_places에 장소 추가
    def add_banned_places(self, schedule_id: str, place_names: list[str]) -> bool:
        result = self.collection.update_one(
            {"schedule_id": schedule_id},
            {"$addToSet": {"banned_places": {"$each": place_names}}}
        )
        return result.matched_count == 1

    # 피드백 내역 추가
    def add_feedback(self, schedule_id: str, feedback: str) -> bool:
        result = self.collection.update_one(
            {"schedule_id": schedule_id},
            {"$push": {"feedback_history": feedback}}
        )
        return result.modified_count == 1



schedule_repository = ScheduleRepository()