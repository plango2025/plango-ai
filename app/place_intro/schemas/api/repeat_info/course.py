# TourAPI - detailInfo1 (반복정보조회) 중 contentTypeId = 25 (여행코스) 응답 스키마

from typing import Any
from .base import RepeatInfoBase


class RepeatCourseItem(RepeatInfoBase):
    subcontentid: Any | None = None         # 하위 콘텐츠 ID
    subdetailalt: Any | None = None         # 코스 이미지 설명
    subdetailimg: Any | None = None         # 코스 이미지
    subdetailoverview: Any | None = None    # 코스 개요
    subname: Any | None = None              # 코스명
    subnum: Any | None = None                # 반복 일련번호


