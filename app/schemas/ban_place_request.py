from pydantic import BaseModel
from typing import List, Optional

class BanPlaceRequest(BaseModel):
    places: List[str]       # 제외할 장소 리스트
    user_id: Optional[str] = None       # 사용자 ID (선택적)
