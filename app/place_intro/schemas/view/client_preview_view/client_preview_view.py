# searchKeyword1 API의 일부 내용을 프론트에 빠르게 전달하는 요약 스키마

from pydantic import BaseModel

# keyword_search_info
from .keyword_search_info import KeywordSearchItem

class clientPreviewView(BaseModel):
    contentid: int
    contenttypeid: int

    keyword_search_info: KeywordSearchItem
    


