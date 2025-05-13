from fastapi import Request, HTTPException
from app.config import settings


ALLOWED_PATH_PREFIXES = ["/docs", "/openapi.json"]

async def verify_api_key_middleware(request: Request, call_next):
    """
    FastAPI 전역 미들웨어로, 모든 HTTP 요청에 대해 API 키를 검사합니다.

    - 헤더에 'X-PLANGO-AI-ACCESS-KEY'가 포함되어 있는지 확인합니다.
    - 키가 누락되었거나 유효하지 않으면 403 Forbidden 에러를 발생시킵니다.
    - 단, Swagger 문서(/docs), OpenAPI 스펙(/openapi.json) 등의 경로는 예외 처리하여 인증 없이 접근할 수 있도록 허용합니다.

    이 미들웨어는 서버 간 내부 통신 보호 또는 외부 요청 제한용으로 사용됩니다.
    """

    path = request.url.path

    # 특정 경로에 대해서는 API 키 검증을 건너뜁니다.
    if any(path.startswith(p) for p in ALLOWED_PATH_PREFIXES):
        return await call_next(request)

    # API 키가 요청 헤더에 포함되어 있는지 확인합니다.
    header_key = request.headers.get("X-PLANGO-AI-ACCESS-KEY")
    if header_key != settings.PLANGO_AI_ACCESS_KEY:
        raise HTTPException(status_code=403, detail="접근이 거부되었습니다. API 키가 잘못되었거나 전달되지 않았습니다.")

    return await call_next(request)
