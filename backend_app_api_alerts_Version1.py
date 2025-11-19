from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from ..db import get_db
from ..models import models
from ..schemas.schemas import AlertIn, AlertOut
from ..services.alerts import push_alert

router = APIRouter()


@router.post("/", response_model=AlertOut)
def create_alert(alert: AlertIn, db: Session = Depends(get_db)):
    return push_alert(db, alert)


@router.get("/", response_model=List[AlertOut])
def list_alerts(camera_id: Optional[int] = Query(None), severity: Optional[str] = Query(None), from_ts: Optional[datetime] = Query(None), to_ts: Optional[datetime] = Query(None), limit: int = 50, db: Session = Depends(get_db)):
    q = db.query(models.Alert)
    if camera_id:
        q = q.filter(models.Alert.camera_id == camera_id)
    if severity:
        q = q.filter(models.Alert.severity == severity)
    if from_ts:
        q = q.filter(models.Alert.created_at >= from_ts)
    if to_ts:
        q = q.filter(models.Alert.created_at <= to_ts)
    alerts = q.order_by(models.Alert.created_at.desc()).limit(limit).all()
    return alerts