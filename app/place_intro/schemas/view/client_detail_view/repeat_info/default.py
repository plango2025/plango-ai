# TourAPI - detailInfo1 (반복정보조회) 중 숙박, 여행코스를 제외한 타입 응답 중 필요한 필드만 골라 담은 스키마  

from typing import Any
from .base import RepeatInfoBase


class RepeatInfoItem(RepeatInfoBase):
    fldgubun: Any | None = None     # 일련번호 구분
    infoname: Any | None = None     # 제목
    infotext: Any | None = None     # 내용
    serialnum: Any | None = None   # 반복 일련번호



