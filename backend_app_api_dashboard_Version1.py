from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..db import get_db
from ..models import models
from ..schemas.schemas import CameraOut, AlertOut
from ..services.metrics import gather_summary

router = APIRouter()


@router.get("/summary")
def summary(db: Session = Depends(get_db)):
    return gather_summary(db)


@router.get("/camera/{camera_id}/summary")
def camera_summary(camera_id: int, limit: int = 20, db: Session = Depends(get_db)):
    camera = db.query(models.Camera).get(camera_id)
    if not camera:
        raise HTTPException(status_code=404, detail="camera not found")
    alerts = db.query(models.Alert).filter(models.Alert.camera_id == camera_id).order_by(models.Alert.created_at.desc()).limit(limit).all()
    return {"camera": CameraOut.from_orm(camera), "alerts": [AlertOut.from_orm(a) for a in alerts]}