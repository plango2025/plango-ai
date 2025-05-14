from pymongo.collection import Collection
from pymongo import ASCENDING
from app.db.mongo import db
from app.models.schedule_document import ScheduleDocument
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
            {"$unset": {"expires_at": ""}}
        )
        return result.modified_count == 1


    # pick 장소 추가
    def add_picked_place(self, schedule_id: str, place_name: str) -> bool:
        result = self.collection.update_one(
            {"schedule_id": schedule_id},
            {"$addToSet": {"picked_places": place_name}}  # 중복 방지
        )
        return result.modified_count == 1

    # ban 장소 추가
    def add_banned_place(self, schedule_id: str, place_name: str) -> bool:
        result = self.collection.update_one(
            {"schedule_id": schedule_id},
            {"$addToSet": {"banned_places": place_name}}  # 중복 방지
        )
        return result.modified_count == 1

    # 피드백 내역 추가
    def add_feedback(self, schedule_id: str, feedback: str) -> bool:
        result = self.collection.update_one(
            {"schedule_id": schedule_id},
            {"$push": {"feedback_history": feedback}}
        )
        return result.modified_count == 1

schedule_repository = ScheduleRepository()