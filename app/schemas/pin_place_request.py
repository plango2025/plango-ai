from pydantic import BaseModel
from typing import List

class PinPlaceRequest(BaseModel):
    places: List[str]
