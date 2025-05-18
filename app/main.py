from fastapi import FastAPI

from app.schedule.routes import schedule
from app.middleware.api_key_middleware import verify_api_key_middleware

from app.place_intro.routers.v1 import tour  # api/v1/tour.py의 router 불러오기

# FastAPI 인스턴스 생성
app = FastAPI(
    title="Plango API",
    description="LLM 기반 여행지 설명 API",
    version="1.0.0"
)

# 미들웨어 등록
app.middleware("http")(verify_api_key_middleware)

# 라우터 등록
app.include_router(schedule.router)
app.include_router(tour.router, prefix="/v1", tags=["Tour"])