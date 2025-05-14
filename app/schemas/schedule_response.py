from pydantic import BaseModel
from typing import Optional
from app.schemas.schedule import Schedule

class ScheduleResponse(BaseModel):  
    schedule_id: Optional[str]      # 일정 ID
    schedule : Schedule             # 여행 일정
