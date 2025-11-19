from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
import os
import uuid
from sqlalchemy.orm import Session

from ..db import get_db
from ..models import models as models_m

router = APIRouter()


@router.post("/upload")
def upload_model(file: UploadFile = File(...), db: Session = Depends(get_db)):
    os.makedirs("models", exist_ok=True)
    fname = f"models/{uuid.uuid4().hex}_{file.filename}"
    with open(fname, "wb") as f:
        f.write(file.file.read())
    new = models_m.ModelVersion(version=str(uuid.uuid4().hex)[:8], path=fname)
    db.add(new)
    db.commit()
    db.refresh(new)
    return {"id": new.id, "path": new.path}