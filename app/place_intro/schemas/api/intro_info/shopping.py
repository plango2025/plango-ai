# TourAPI - detailIntro1 (소개정보조회)중 쇼핑(contentTypeId=38) 응답 스키마

from typing import Any
from .base import IntroBase


class ShoppingIntro(IntroBase):
    chkbabycarriageshopping: Any | None = None  # 유모차 대여 정보
    chkcreditcardshopping: Any | None = None    # 신용카드 가능 정보
    chkpetshopping: Any | None = None           # 애완동물 동반 가능 정보
    culturecenter: Any | None = None            # 문화센터 바로가기
    fairday: Any | None = None                  # 장서는 날
    infocentershopping: Any | None = None       # 문의 및 안내
    opendateshopping: Any | None = None         # 개장일
    opentime: Any | None = None                 # 영업시간
    parkingshopping: Any | None = None          # 주차시설
    restdateshopping: Any | None = None         # 쉬는 날
    restroom: Any | None = None                 # 화장실 설명
    saleitem: Any | None = None                 # 판매 품목
    saleitemcost: Any | None = None             # 판매 품목별 가격
    scaleshopping: Any | None = None            # 규모
    shopguide: Any | None = None                # 매장 안내


