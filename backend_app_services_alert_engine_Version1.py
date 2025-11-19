from typing import List, Dict, Any
from ..services.alerts import push_alert
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
    persons = [d for d in detections if d["class"] == "person" and d["score"] > 0.4]
    bikes = [d for d in detections if d["class"] == "bicycle" and d["score"] > 0.4]
    vehicles = [d for d in detections if d["class"] == "vehicle" and d["score"] > 0.4]

    alerts = []
    for p in persons:
        for v in vehicles:
            dist = euclidean(bbox_center(p["bbox"]), bbox_center(v["bbox"]))
            if dist < 80:
                alert = {"camera_id": camera_id, "severity": "high", "type": "near_miss", "payload": {"person": p, "vehicle": v, "distance": dist, "job_id": job_id}}
                alerts.append(alert)
                push_alert(db, alert_in=type("X", (), alert))
    for b in bikes:
        for v in vehicles:
            dist = euclidean(bbox_center(b["bbox"]), bbox_center(v["bbox"]))
            if dist < 100:
                alert = {"camera_id": camera_id, "severity": "medium", "type": "bike_vehicle_close", "payload": {"bike": b, "vehicle": v, "distance": dist, "job_id": job_id}}
                alerts.append(alert)
                push_alert(db, alert_in=type("X", (), alert))
    return alerts