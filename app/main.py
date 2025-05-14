from fastapi import FastAPI
from contextlib import asynccontextmanager
from pymongo import errors
import logging as logger

from app.routes import schedule
from app.middleware.api_key_middleware import verify_api_key_middleware
from app.db.mongo import db

# lifespan 이벤트 등록
@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        # MongoDB 연결 확인
        db.command("ping")
        logger.info("MongoDB 연결 성공")
    except errors.PyMongoError as e:
        # MongoDB 연결 실패 시 서버 중지
        logger.critical(f"MongoDB 연결 실패: {str(e)}")
        raise RuntimeError("MongoDB 연결에 실패했습니다.")

    yield  # 서버 실행

# FastAPI 인스턴스 생성
app = FastAPI(lifespan=lifespan)

# 미들웨어 등록
app.middleware("http")(verify_api_key_middleware)

# 라우터 등록
app.include_router(schedule.router)
