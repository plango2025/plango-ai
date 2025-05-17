import requests

from fastapi import HTTPException
from pydantic import ValidationError
import logging as logger

from app.schedule.schemas.tour_keyword_search_response import TourKeywordSearchResponse

from app.config.settings import settings



def search_place_info(keyword: str) -> TourKeywordSearchResponse:
    """
    TourAPI 키워드 검색을 통해 장소의 썸네일 이미지와 좌표를 조회합니다.
    """

    # 요청 URL 및 인증키 설정
    url = f"http://apis.data.go.kr/B551011/KorService1/searchKeyword1?serviceKey={settings.TOURAPI_KEY}"

    # 요청 파라미터 구성
    params = {
        "MobileApp": "plango",     # 호출 앱 이름
        "MobileOS": "ETC",         # 운영체제 구분
        "numOfRows": 1,            # 결과 개수 (1개만 조회)
        "pageNo": 1,               # 페이지 번호
        "listYN": "Y",             # 목록 출력 여부
        "arrange": "A",            # 정렬 방식 (제목순)
        "keyword": keyword,        # 검색 키워드
        "_type": "json"            # 응답 포맷
    }

    # TourAPI GET 요청 전송
    response = requests.get(url, params=params)

    # 응답 상태 코드 확인 및 예외 처리
    if response.status_code != 200:
        logger.error(f"TourAPI 요청 실패: {response.status_code} - {response.text}")
        raise HTTPException(status_code=502, detail="TourAPI 서버 요청 실패")

    try:
        # JSON 응답 파싱 및 필요한 데이터 추출
        json_data = response.json()
        items = json_data["response"]["body"]["items"]

        # 검색 결과가 없을 경우, 빈 스키마 반환
        if not items or not items["item"]:
            return TourKeywordSearchResponse()  # 모든 필드는 기본값(None)으로 채워짐
        
        # 첫번째 검색 결과 항목을 선택
        place = items["item"][0]

        # 최종 응답 객체 반환
        return TourKeywordSearchResponse(**place)

    except (KeyError, IndexError, ValidationError) as e:
        # 응답 파싱 중 오류 발생 시 예외 처리
        logger.error(f"TourAPI 응답 파싱 오류: {str(e)}")
        raise HTTPException(status_code=500, detail=f"TourAPI 응답 파싱 실패: {str(e)}")
