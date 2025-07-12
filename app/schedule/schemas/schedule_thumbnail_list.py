from pydantic import BaseModel
from app.schedule.schemas.schedule_thumbnail import ScheduleThumbnail
from typing import List

class ScheduleThumbnailList(BaseModel):
    data: List[ScheduleThumbnail]