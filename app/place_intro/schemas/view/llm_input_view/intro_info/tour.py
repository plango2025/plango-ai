# TourAPI - detailIntro1 (소개정보조회)중 관광지(contentTypeId=12)응답 중 필요한 필드만 골라 담은 스키마

from typing import Any
from .base import IntroBase


class TourIntro(IntroBase):
    accomcount: Any | None = None              # 수용인원
    chkbabycarriage: Any | None = None          # 유모차 대여정보
    chkcreditcard: Any | None = None            # 신용카드 가능여부
    chkpet: Any | None = None                   # 애완동물 동반 가능여부
    expagerange: Any | None = None              # 체험가능 연령
    expguide: Any | None = None                 # 체험 안내
    heritage1: Any | None = None                # 세계문화유산 여부
    heritage2: Any | None = None                # 세계자연유산 여부
    heritage3: Any | None = None                # 세계기록유산 여부
    infocenter: Any | None = None               # 문의 및 안내
    opendate: Any | None = None                 # 개장일
    parking: Any | None = None                  # 주차시설
    restdate: Any | None = None                 # 쉬는날
    useseason: Any | None = None                # 이용시기
    usetime: Any | None = None                  # 이용시간


