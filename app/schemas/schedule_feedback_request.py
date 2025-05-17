from pydantic import BaseModel
from typing import Optional

class ScheduleFeedbackRequest(BaseModel):
    feedback: str           # 피드백 내용
    user_id: Optional[str] = None       # 사용자 ID (선택적)
