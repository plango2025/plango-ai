from pydantic import BaseModel
from typing import Optional
from app.schedule.schemas.schedule import Schedule

class ScheduleCreateResponse(BaseModel):  
    schedule_id: Optional[str]      # 일정 ID
    schedule : Schedule             # 여행 일정
