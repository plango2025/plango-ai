from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    # 기본 설정
    app_name: str = "Plango"
    debug: bool = True # FastAPI 실행 시 디버깅 정보 출력

    # 외부 통신 설정
    timeout: int = 30  # 외부 API 호출시 타임아웃 시간

    # TourAPI 설정
    TOURAPI_BASE_URL: str = "http://apis.data.go.kr/B551011"

    # env 파일 환경 변수
    OPENAI_API_KEY: str
    PLANGO_AI_ACCESS_KEY: str
    TOURAPI_KEY: str
    MONGO_URI: str
    MONGO_DB_NAME: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8" # UTF-8로 인코딩된 파일을 읽게 설정.


''''
# 매번 Settings()를 새로 만들면 비효율적이므로, lru_cache()로 1회 생성 후 재사용
# 다른 모듈에서 get_settings()를 호출하면 캐시된 동일한 설정 인스턴스를 받게 된다.
@lru_cache()
def get_settings():
    return Settings()
'''

settings = Settings()