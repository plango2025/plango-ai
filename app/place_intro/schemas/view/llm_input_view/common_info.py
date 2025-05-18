# TourAPI - detailCommon1 (공통정보조회) 응답 중 필요한 필드만 골라 담은 스키마

from typing import Any
from pydantic import BaseModel


class CommonInfoItem(BaseModel):
    # 기본 식별 정보
    contentid: int                          # 콘텐츠 ID
    contenttypeid: int                      # 콘텐츠 타입 ID
    title: str                              # 콘텐츠명
    
    # 날짜 정보
    createdtime: str                        # 최초 등록일
    modifiedtime: str                       # 수정일

    # 홈페이지 및 연락처
    homepage: Any | None = None                 # 홈페이지 주소 
    tel: Any | None = None                      # 전화번호
    telname: Any | None = None                  # 전화번호명

    # 분류 코드
    cat1: Any | None = None                     # 대분류
    cat2: Any | None = None                     # 중분류
    cat3: Any | None = None                     # 소분류

    # 위치 정보
    areacode: Any | None = None                # 지역 코드
    sigungucode: Any | None = None             # 시군구 코드
    addr1: Any | None = None                    # 주소
    addr2: Any | None = None                    # 상세 주소
    zipcode: Any | None = None                  # 우편번호
    mapx: Any | None = None                   # 경도
    mapy: Any | None = None                   # 위도
    mlevel: Any | None = None                  # 지도 레벨

    # 이미지
    firstimage: Any | None = None               # 원본 이미지 URL
    firstimage2: Any | None = None              # 썸네일 이미지 URL

    # 기타
    overview: Any | None = None                 # 콘텐츠 개요
    booktour: Any | None = None                # 교과서 여행지 여부 (1: 있음, 0: 없음)
    cpyrhtDivCd: Any | None = None              # 저작권 유형



