# TourAPI - detailIntro1 (소개정보조회)중 레포츠(contentTypeId=28) 응답 스키마

from typing import Any
from .base import IntroBase


class LeportsIntro(IntroBase):
    accomcountleports: Any | None = None             # 수용인원
    chkbabycarriageleports: Any | None = None        # 유모차 대여정보
    chkcreditcardleports: Any | None = None          # 신용카드 가능여부
    chkpetleports: Any | None = None                 # 애완동물 동반 가능여부
    expagerangeleports: Any | None = None            # 체험 가능 연령
    infocenterleports: Any | None = None             # 문의 및 안내
    openperiod: Any | None = None                    # 개장 기간
    parkingfeeleports: Any | None = None             # 주차 요금
    parkingleports: Any | None = None                # 주차 시설
    reservation: Any | None = None                   # 예약 안내
    restdateleports: Any | None = None               # 쉬는 날
    scaleleports: Any | None = None                  # 규모
    usefeeleports: Any | None = None                 # 입장료
    usetimeleports: Any | None = None                # 이용 시간


