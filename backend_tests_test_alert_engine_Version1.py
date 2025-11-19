from app.services.alert_engine import evaluate_detections
from app.models import models
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import tempfile
import os

def test_alert_rule_simple():
    # in-memory sqlite
    engine = create_engine("sqlite:///:memory:")
    models.Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    db = Session()
    # create dummy job & camera
    cam = models.Camera(name="c", rtsp_url="x")
    db.add(cam)
    db.commit()
    job_id = 1
    detections = [
        {"bbox":[10,10,20,40],"class":"person","score":0.9},
        {"bbox":[15,15,30,30],"class":"vehicle","score":0.9}
    ]
    alerts = evaluate_detections(db, job_id, cam.id, detections)
    assert len(alerts) >= 1