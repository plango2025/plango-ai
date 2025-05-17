# TourAPI - detailIntro1 (소개정보조회)중 숙박(contentTypeId=32)응답 중 필요한 필드만 골라 담은 스키마

from typing import Any
from .base import IntroBase


class LodgingIntro(IntroBase):
    accomcountlodging: Any | None = None             # 수용 가능 인원
    benikia: Any | None = None                        # 베니키아 여부
    checkintime: Any | None = None                    # 입실 시간
    checkouttime: Any | None = None                   # 퇴실 시간
    chkcooking: Any | None = None                     # 객실 내 취사 여부
    foodplace: Any | None = None                      # 식음료장
    goodstay: Any | None = None                       # 굿스테이 여부
    hanok: Any | None = None                          # 한옥 여부
    infocenterlodging: Any | None = None              # 문의 및 안내
    parkinglodging: Any | None = None                 # 주차 시설
    pickup: Any | None = None                         # 픽업 서비스
    roomcount: Any | None = None                     # 객실 수
    reservationlodging: Any | None = None             # 예약 안내
    reservationurl: Any | None = None                 # 예약 안내 홈페이지
    roomtype: Any | None = None                       # 객실 유형
    scalelodging: Any | None = None                   # 규모
    subfacility: Any | None = None                    # 부대시설 (기타)

    # 부대시설 상세
    barbecue: Any | None = None
    beauty: Any | None = None
    beverage: Any | None = None
    bicycle: Any | None = None
    campfire: Any | None = None
    fitness: Any | None = None
    karaoke: Any | None = None
    publicbath: Any | None = None
    publicpc: Any | None = None
    sauna: Any | None = None
    seminar: Any | None = None
    sports: Any | None = None

    refundregulation: Any | None = None               # 환불 규정


