# TourAPI - detailInfo1 (반복정보조회) 응답에서 공통적으로 사용되는 필드를 정의한 스키마

from pydantic import BaseModel


class RepeatInfoBase(BaseModel):
    contentid: int           # 콘텐츠 ID
    contenttypeid: int       # 콘텐츠 타입 ID
