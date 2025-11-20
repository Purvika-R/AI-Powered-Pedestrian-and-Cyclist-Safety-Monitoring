from sqlalchemy import Column, Integer, String, DateTime, JSON, ForeignKey, func, Boolean, Text
from sqlalchemy.orm import relationship
from datetime import datetime

from ..db import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(64), unique=True, nullable=False)
    password_hash = Column(String(256), nullable=False)
    is_admin = Column(Boolean, default=False)


class Camera(Base):
    __tablename__ = "cameras"
    id = Column(Integer, primary_key=True)
    name = Column(String(128))
    location = Column(String(256))
    rtsp_url = Column(String(512))


class Job(Base):
    __tablename__ = "jobs"
    id = Column(Integer, primary_key=True)
    camera_id = Column(Integer, ForeignKey("cameras.id"), nullable=True)
    source = Column(String(512))  # path or url
    status = Column(String(32), default="pending")
    created_at = Column(DateTime, server_default=func.now())


class Alert(Base):
    __tablename__ = "alerts"
    id = Column(Integer, primary_key=True)
    camera_id = Column(Integer, ForeignKey("cameras.id"), nullable=True)
    job_id = Column(Integer, ForeignKey("jobs.id"), nullable=True)
    severity = Column(String(32), default="low")
    type = Column(String(64))
    payload = Column(JSON)
    created_at = Column(DateTime, server_default=func.now())


class ModelVersion(Base):
    __tablename__ = "model_versions"
    id = Column(Integer, primary_key=True)
    version = Column(String(64))
    path = Column(String(512))
    created_at = Column(DateTime, server_default=func.now())