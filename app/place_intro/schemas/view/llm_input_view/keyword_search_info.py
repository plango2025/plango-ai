# TourAPI - searchKeyword1 (키워드검색조회)응답 중 필요한 필드만 골라 담은 스키마

from typing import Any
from pydantic import BaseModel


class KeywordSearchItem(BaseModel):
    # 관광지 기본 정보
    addr1: Any | None = None                   # 주소
    addr2: Any | None = None                   # 상세주소
    areacode: Any | None = None               # 지역코드
    sigungucode: Any | None = None            # 시군구코드
    contentid: int                         # 콘텐츠 ID (필수)
    contenttypeid: int                     # 콘텐츠 타입 ID (필수)
    title: str                             # 콘텐츠 제목 (필수)

    # 분류 코드
    cat1: Any | None = None                    # 대분류
    cat2: Any | None = None                    # 중분류
    cat3: Any | None = None                    # 소분류

    # 좌표 정보
    mapx: Any | None = None                  # 경도 (X)
    mapy: Any | None = None                  # 위도 (Y)
    mlevel: Any | None = None                 # 지도레벨

    # 이미지
    firstimage: Any | None = None              # 대표이미지 원본
    firstimage2: Any | None = None             # 대표이미지 썸네일

    # 날짜
    createdtime: str                       # 최초 등록일 (필수)
    modifiedtime: str                      # 수정일 (필수)

    # 기타
    tel: Any | None = None                     # 전화번호
    booktour: Any | None = None              # 교과서 여행지 여부
    cpyrhtDivCd: Any | None = None            # 저작권 유형



