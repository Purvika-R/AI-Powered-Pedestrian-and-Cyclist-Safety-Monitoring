from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from fastapi import BackgroundTasks
from sqlalchemy.orm import Session
import os
import uuid
from typing import Optional

from ..db import get_db
from ..models import models
from ..schemas.schemas import JobOut
from ..worker import tasks

router = APIRouter()


@router.post("/video", response_model=JobOut)
async def ingest_video(file: Optional[UploadFile] = File(None), rtsp_url: Optional[str] = Form(None), camera_id: Optional[int] = Form(None), db: Session = Depends(get_db)):
    """
    POST /ingest/video
    Accepts: multipart file upload (video) OR rtsp_url in form-data
    Creates a Job and enqueues a processing task.
    """
    if not file and not rtsp_url:
        raise HTTPException(status_code=400, detail="Provide file upload or rtsp_url")

    source_path = ""
    if file:
        os.makedirs("storage/uploads", exist_ok=True)
        filename = f"storage/uploads/{uuid.uuid4().hex}_{file.filename}"
        with open(filename, "wb") as f:
            f.write(await file.read())
        source_path = filename
    else:
        source_path = rtsp_url

    job = models.Job(camera_id=camera_id, source=source_path, status="queued")
    db.add(job)
    db.commit()
    db.refresh(job)

    # enqueue celery task
    tasks.process_video.delay(job.id, source_path)

    return job