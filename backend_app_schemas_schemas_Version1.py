from pydantic import BaseModel
from typing import Optional, List, Any
from datetime import datetime


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    username: Optional[str] = None


class UserCreate(BaseModel):
    username: str
    password: str


class CameraOut(BaseModel):
    id: int
    name: Optional[str]
    location: Optional[str]
    rtsp_url: Optional[str]

    class Config:
        orm_mode = True


class JobOut(BaseModel):
    id: int
    camera_id: Optional[int]
    source: str
    status: str
    created_at: datetime

    class Config:
        orm_mode = True


class AlertIn(BaseModel):
    camera_id: Optional[int]
    severity: str
    type: str
    payload: Any


class AlertOut(BaseModel):
    id: int
    camera_id: Optional[int]
    severity: str
    type: str
    payload: Any
    created_at: datetime

    class Config:
        orm_mode = True