from sqlalchemy.orm import Session
from typing import Any
import json
import redis
# use absolute import so Pylance can resolve it reliably
from backend.app.config import settings

# Redis client (decode_responses so published payloads are str)
r = redis.from_url(settings.REDIS_URL, decode_responses=True)


def push_alert(db: Session, alert_in: Any):
    """
    Persist an alert to DB and publish to a Redis 'alerts' channel.
    alert_in expected to have attributes: camera_id, severity, type, payload
    """
    # lazy import to avoid circular imports
    from backend.app.models import models as models_module

    alert = models_module.Alert(
        camera_id=getattr(alert_in, "camera_id", None),
        severity=getattr(alert_in, "severity", "low"),
        type=getattr(alert_in, "type", "unknown"),
        payload=getattr(alert_in, "payload", None),
    )
    db.add(alert)
    db.commit()
    db.refresh(alert)

    # publish to redis channel
    try:
        r.publish("alerts", json.dumps({
            "id": alert.id,
            "type": alert.type,
            "severity": alert.severity,
            "payload": alert.payload
        }))
    except Exception:
        # fail gracefully if redis not available during development
        pass

    return alert