from sqlalchemy.orm import Session
from ..models import models
from ..utils import events


def gather_summary(db: Session):
    cameras = db.query(models.Camera).count()
    recent_alerts = db.query(models.Alert).order_by(models.Alert.created_at.desc()).limit(10).all()
    model_health = {"loaded_model": events.current_model_info()}
    return {
        "active_cameras": cameras,
        "recent_alerts": [ {"id": a.id, "type": a.type, "severity": a.severity} for a in recent_alerts],
        "model_health": model_health,
        "metrics": events.metrics()
    }