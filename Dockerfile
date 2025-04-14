# Python 3.10 기반 이미지 사용
FROM python:3.10-slim

# 작업 디렉토리 설정
WORKDIR /app

# 의존성 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 소스 복사
COPY . .

# FastAPI 실행 (필요에 따라 변경 가능)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
