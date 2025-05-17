# 환경 설정값을 중앙에서 관리하기 위한 파일
# .env 환경변수 파일과 연동되어, 설정값을 안전하고 효율적으로 다룰 수 있도록 한다.

from pydantic_settings import BaseSettings
from pydantic import Field
from functools import lru_cache


class Settings(BaseSettings):
    # 기본 설정
    app_name: str = "Plango"
    debug: bool = True # FastAPI 실행 시 디버깅 정보 출력

    # TourAPI 설정
    tourapi_key: str = Field(..., env="TOURAPI_KEY") # .env 파일에 정의된 TOURAPI_KEY 값을 로드. 해당 키는 반드시 있어야 되며 없으면 에러 발생.
    tourapi_base_url: str = "http://apis.data.go.kr/B551011"

    # 외부 통신 설정
    timeout: int = 30  # 외부 API 호출시 타임아웃 시간

    class Config:
        env_file = ".env" # .env 파일에서 값을 로드하도록 지정
        env_file_encoding = "utf-8" # UTF-8로 인코딩된 파일을 읽게 설정.

# 매번 Settings()를 새로 만들면 비효율적이므로, lru_cache()로 1회 생성 후 재사용
# 다른 모듈에서 get_settings()를 호출하면 캐시된 동일한 설정 인스턴스를 받게 된다.
@lru_cache()
def get_settings():
    return Settings()
