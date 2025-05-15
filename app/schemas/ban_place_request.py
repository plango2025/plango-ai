from pydantic import BaseModel
from typing import List, Optional

class BanPlaceRequest(BaseModel):
    places: List[str]
    user_id: Optional[str] = None
