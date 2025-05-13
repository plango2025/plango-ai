from typing import Optional
from pydantic import BaseModel

class TourKeywordSearchResponse(BaseModel):
    """
    TourAPI - searchKeyword1 (키워드검색조회) 응답 항목 스키마
    """

    # 관광지 기본 정보
    addr1: Optional[str] = None         # 주소
    addr2: Optional[str] = None         # 상세주소
    areacode: Optional[int] = None      # 지역코드
    sigungucode: Optional[int] = None   # 시군구코드
    contentid: Optional[int] = None     # 콘텐츠 ID (필수)
    contenttypeid: Optional[int] = None # 콘텐츠 타입 ID (필수)
    title: Optional[str] = None         # 콘텐츠 제목 (필수)

    # 분류 코드
    cat1: Optional[str] = None          # 대분류
    cat2: Optional[str] = None          # 중분류
    cat3: Optional[str] = None          # 소분류

    # 좌표 정보
    mapx: Optional[str] = None        # 경도 (X)
    mapy: Optional[str] = None        # 위도 (Y)
    mlevel: Optional[str] = None        # 지도레벨

    # 이미지
    firstimage: Optional[str] = None    # 대표이미지 원본
    firstimage2: Optional[str] = None   # 대표이미지 썸네일

    # 날짜
    createdtime: Optional[str] = None   # 최초 등록일 (필수)
    modifiedtime: Optional[str] = None  # 수정일 (필수)

    # 기타
    tel: Optional[str] = None           # 전화번호
    booktour: Optional[str] = None      # 교과서 여행지 여부
    cpyrhtDivCd: Optional[str] = None   # 저작권 유형