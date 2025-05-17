from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from api.v1 import tour  # api/v1/tour.py의 router 불러오기

app = FastAPI(
    title="Plango API",
    description="LLM 기반 여행지 설명 API",
    version="1.0.0"
)

# CORS 설정 (필요 시 도메인 제한 가능)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 개발 시에는 "*" / 배포 시에는 특정 도메인으로 제한
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 라우터 등록
app.include_router(tour.router, prefix="/v1", tags=["Tour"])

# 루트 엔드포인트 (헬스체크)
@app.get("/")
async def root():
    return {"message": "Plango API is running"}


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
