from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    OPENAI_API_KEY: str
    PLANGO_AI_ACCESS_KEY: str
    TOURAPI_SERVICE_KEY: str

    class Config:
        env_file = ".env"

settings = Settings()
