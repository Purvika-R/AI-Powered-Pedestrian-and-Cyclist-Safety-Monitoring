from typing import List, Dict, Any
# use absolute import so Pylance can resolve it reliably
from backend.app.services.backend_app_services_alerts_Version1 import push_alert
from sqlalchemy.orm import Session
import math


def bbox_center(bbox):
    x, y, w, h = bbox
    return (x + w / 2, y + h / 2)


def euclidean(a, b):
    return math.hypot(a[0] - b[0], a[1] - b[1])


def evaluate_detections(db: Session, job_id: int, camera_id: int, detections: List[Dict[str, Any]]):
    """
    Simple rule-based engine:
    - If pedestrian and vehicle center distance < threshold => near-miss (severity=high)
    - If cyclist and vehicle close => medium
    - If pedestrian crossing (detected alone in roadway area) => low
    """
    persons = [d for d in detections if d.get("class") == "person" and d.get("score", 0) > 0.4]
    bikes = [d for d in detections if d.get("class") == "bicycle" and d.get("score", 0) > 0.4]
    vehicles = [d for d in detections if d.get("class") in ("car", "truck", "bus", "motorcycle") and d.get("score", 0) > 0.4]

    alerts = []
    for p in persons:
        for v in vehicles:
            dist = euclidean(bbox_center(p["bbox"]), bbox_center(v["bbox"]))
            if dist < 80:
                alert = {
                    "camera_id": camera_id,
                    "severity": "high",
                    "type": "near_miss",
                    "payload": {"person": p, "vehicle": v, "distance": dist, "job_id": job_id},
                }
                alerts.append(alert)
                class A: pass
                ai = A()
                ai.camera_id = alert["camera_id"]
                ai.severity = alert["severity"]
                ai.type = alert["type"]
                ai.payload = alert["payload"]
                push_alert(db, ai)
    for b in bikes:
        for v in vehicles:
            dist = euclidean(bbox_center(b["bbox"]), bbox_center(v["bbox"]))
            if dist < 100:
                alert = {
                    "camera_id": camera_id,
                    "severity": "medium",
                    "type": "bike_vehicle_close",
                    "payload": {"bike": b, "vehicle": v, "distance": dist, "job_id": job_id},
                }
                alerts.append(alert)
                class A: pass
                ai = A()
                ai.camera_id = alert["camera_id"]
                ai.severity = alert["severity"]
                ai.type = alert["type"]
                ai.payload = alert["payload"]
                push_alert(db, ai)
    return alerts