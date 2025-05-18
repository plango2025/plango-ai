# TourAPI - detailIntro1 (소개정보조회)중 행사/공연/축제(contentTypeId=15) 응답 스키마

from typing import Any
from .base import IntroBase


class FestivalIntro(IntroBase):
    agelimit: Any | None = None                 # 관람 가능 연령
    bookingplace:  Any | None = None             # 예매처
    discountinfofestival:  Any | None = None     # 할인 정보
    eventenddate:  Any | None = None             # 행사 종료일
    eventhomepage:  Any | None = None            # 행사 홈페이지
    eventplace:  Any | None = None               # 행사 장소
    eventstartdate:  Any | None = None           # 행사 시작일
    festivalgrade:  Any | None = None            # 축제 등급
    placeinfo:  Any | None = None                # 행사장 위치 안내
    playtime:  Any | None = None                 # 공연 시간
    program:  Any | None = None                  # 행사 프로그램
    spendtimefestival:  Any | None = None        # 관람 소요 시간
    sponsor1:  Any | None = None                 # 주최자 정보
    sponsor1tel:  Any | None = None              # 주최자 연락처
    sponsor2:  Any | None = None                 # 주관사 정보
    sponsor2tel:  Any | None = None              # 주관사 연락처
    subevent:  Any | None = None                 # 부대행사 내용
    usetimefestival:  Any | None = None          # 이용 요금

