# TourAPI - detailIntro1 (소개정보조회)중 음식점(contentTypeId=39) 응답 스키마

from typing import Any
from .base import IntroBase


class FoodIntro(IntroBase):
    chkcreditcardfood: Any | None = None     # 신용카드 가능 정보
    discountinfofood: Any | None = None      # 할인정보
    firstmenu: Any | None = None             # 대표메뉴
    infocenterfood: Any | None = None        # 문의 및 안내
    kidsfacility: Any | None = None          # 어린이 놀이방 여부
    opendatefood: Any | None = None          # 개업일
    opentimefood: Any | None = None          # 영업시간
    packing: Any | None = None               # 포장 가능
    parkingfood: Any | None = None           # 주차시설
    reservationfood: Any | None = None       # 예약안내
    restdatefood: Any | None = None          # 쉬는 날
    scalefood: Any | None = None             # 규모
    seat: Any | None = None                  # 좌석수
    smoking: Any | None = None               # 금연/흡연 여부
    treatmenu: Any | None = None             # 취급 메뉴
    lcnsno: Any | None = None                # 인허가번호

