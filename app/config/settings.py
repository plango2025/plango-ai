from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    # 기본 설정
    APP_NAME : str = "Plango"
    DEBUG : bool = True # FastAPI 실행 시 디버깅 정보 출력

    # 외부 통신 설정
    TIMEOUT: int = 30  # 외부 API 호출시 타임아웃 시간

    # TourAPI 설정
    TOURAPI_BASE_URL: str = "http://apis.data.go.kr/B551011"

    # env 파일 환경 변수
    OPENAI_API_KEY: str = Field(..., env="OPENAI_API_KEY")
    PLANGO_AI_ACCESS_KEY: str = Field(..., env="PLANGO_AI_ACCESS_KEY")
    TOURAPI_KEY: str = Field(..., env="TOURAPI_KEY")
    MONGO_URI: str = Field(..., env="MONGO_URI")
    MONGO_DB_NAME: str = Field(..., env="MONGO_DB_NAME")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8" # UTF-8로 인코딩된 파일을 읽게 설정.

settings = Settings()