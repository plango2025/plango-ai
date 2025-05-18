# TourAPI - detailIntro1 (소개정보조회)중 문화시설(contentTypeId=14) 응답 스키마

from typing import Any
from .base import IntroBase


class CultureIntro(IntroBase):
    accomcountculture: Any | None = None            # 수용인원
    chkbabycarriageculture: Any | None = None       # 유모차 대여정보
    chkcreditcardculture: Any | None = None         # 신용카드 가능여부
    chkpetculture: Any | None = None                # 애완동물 동반 가능여부
    discountinfo:  Any | None = None                 # 할인정보
    infocenterculture:  Any | None = None            # 문의 및 안내
    parkingculture:  Any | None = None               # 주차시설
    parkingfee:  Any | None = None                   # 주차요금
    restdateculture:  Any | None = None              # 쉬는날
    usefee:  Any | None = None                        # 이용요금
    usetimeculture:  Any | None = None               # 이용시간
    scale:  Any | None = None                         # 규모
    spendtime:  Any | None = None                     # 관람 소요시간

