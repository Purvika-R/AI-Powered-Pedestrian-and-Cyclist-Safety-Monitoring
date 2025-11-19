from sqlalchemy.orm import Session
from ..models import models
from ..schemas.schemas import AlertIn
import json
import redis
from ..config import settings

r = redis.from_url(settings.REDIS_URL, decode_responses=True)


def push_alert(db: Session, alert_in: AlertIn):
    alert = models.Alert(
        camera_id=alert_in.camera_id,
        severity=alert_in.severity,
        type=alert_in.type,
        payload=alert_in.payload,
    )
    db.add(alert)
    db.commit()
    db.refresh(alert)
    # publish to redis channel
    r.publish("alerts", json.dumps({"id": alert.id, "type": alert.type, "severity": alert.severity, "payload": alert.payload}))
    return alert