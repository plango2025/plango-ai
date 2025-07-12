from pydantic import BaseModel

class ScheduleThumbnail(BaseModel):
    schedule_id: str
    created_at: str
    title: str
    thumbnail_url: str
    destination: str
    duration: str

    class Config:
        orm_mode = True
        json_encoders = {
            str: lambda v: v.isoformat() if hasattr(v, 'isoformat') else v,
        }