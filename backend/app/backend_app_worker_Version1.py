from celery import Celery
import os
import time
import cv2
import numpy as np
from sqlalchemy.orm import Session
from .config import settings
from .db import SessionLocal
from .models import models
from .services import alert_engine
from .ml.inference import InferenceModel
from .utils import events

celery_app = Celery("worker", broker=settings.RABBITMQ_URL, backend=settings.REDIS_URL)

# Inference model singleton
inference = InferenceModel(settings.MODEL_DIR)


@celery_app.task(bind=True, acks_late=True, autoretry_for=(Exception,), retry_backoff=True, max_retries=3)
def process_video(self, job_id: int, source: str):
    """
    Extract frames from video source, run inference, and evaluate alerts.
    """
    db: Session = SessionLocal()
    job = db.query(models.Job).get(job_id)
    job.status = "processing"
    db.commit()

    cap = cv2.VideoCapture(source)
    if not cap.isOpened():
        job.status = "failed"
        db.commit()
        return {"error": "cannot_open_source"}

    frame_count = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame_count += 1
        if frame_count % 5 != 0:
            continue
        events.increment_metric("processed_frames")
        detections = inference.predict(frame)
        # Evaluate rules and push alerts
        alert_engine.evaluate_detections(db, job_id=job_id, camera_id=job.camera_id or 0, detections=detections)
        time.sleep(0.01)
    job.status = "done"
    db.commit()
    cap.release()
    events.increment_metric("ingested_jobs")
    return {"status": "done", "processed_frames": frame_count}