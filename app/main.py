from fastapi import FastAPI
from app.routes import schedule
from app.middleware.api_key_middleware import verify_api_key_middleware

app = FastAPI()
app.middleware("http")(verify_api_key_middleware)
app.include_router(schedule.router)
