from pydantic import BaseModel
from typing import List

class BanPlaceRequest(BaseModel):
    places: List[str]
