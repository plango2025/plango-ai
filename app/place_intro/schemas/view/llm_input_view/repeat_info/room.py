# TourAPI - detailInfo1 (반복정보조회) 중 숙박(contentTypeId=32)응답 중 필요한 필드만 골라 담은 스키마 

from typing import Any
from .base import RepeatInfoBase


class LodgingRoomItem(RepeatInfoBase):
    roomcode: Any | None = None               # 객실코드
    roomtitle: Any | None = None              # 객실명칭
    roomsize1: Any | None = None              # 객실크기(평)
    roomcount: Any | None = None              # 객실수
    roombasecount: Any | None = None          # 기준인원
    roommaxcount: Any | None = None           # 최대인원
    roomoffseasonminfee1: Any | None = None   # 비수기주중최소
    roomoffseasonminfee2: Any | None = None   # 비수기주말최소
    roompeakseasonminfee1: Any | None = None  # 성수기주중최소
    roompeakseasonminfee2: Any | None = None  # 성수기주말최소
    roomintro: Any | None = None              # 객실소개
    roombathfacility: Any | None = None       # 목욕시설여부
    roombath: Any | None = None               # 욕조여부
    roomhometheater: Any | None = None        # 홈시어터여부
    roomaircondition: Any | None = None       # 에어컨여부
    roomtv: Any | None = None                 # TV 여부
    roompc: Any | None = None                 # PC 여부
    roomcable: Any | None = None              # 케이블설치여부
    roominternet: Any | None = None           # 인터넷여부
    roomrefrigerator: Any | None = None       # 냉장고여부
    roomtoiletries: Any | None = None         # 세면도구여부
    roomsofa: Any | None = None               # 소파여부
    roomcook: Any | None = None               # 취사용품여부
    roomtable: Any | None = None              # 테이블여부
    roomhairdryer: Any | None = None          # 드라이기여부
    roomsize2: Any | None = None              # 객실크기(평방미터)
    roomimg1: Any | None = None               # 객실사진1
    roomimg1alt: Any | None = None            # 객실사진1 설명
    cpyrhtDivCd1: Any | None = None           # 저작권 유형 1
    roomimg2: Any | None = None               # 객실사진2
    roomimg2alt: Any | None = None            # 객실사진2 설명
    cpyrhtDivCd2: Any | None = None           # 저작권 유형 2
    roomimg3: Any | None = None               # 객실사진3
    roomimg3alt: Any | None = None            # 객실사진3 설명
    cpyrhtDivCd3: Any | None = None           # 저작권 유형 3
    roomimg4: Any | None = None               # 객실사진4
    roomimg4alt: Any | None = None            # 객실사진4 설명
    cpyrhtDivCd4: Any | None = None           # 저작권 유형 4
    roomimg5: Any | None = None               # 객실사진5
    roomimg5alt: Any | None = None            # 객실사진5 설명
    cpyrhtDivCd5: Any | None = None           # 저작권 유형 5
