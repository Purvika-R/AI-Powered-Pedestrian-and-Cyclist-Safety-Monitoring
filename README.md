````markdown
# AI-Powered Pedestrian and Cyclist Safety Monitoring — Backend

This repository contains a production-feasible backend for the "AI-Powered Pedestrian and Cyclist Safety Monitoring" system (see `/mnt/data/AI-Powered-Pedestrian-and-Cyclist-Safety-Monitoring.pptx` for the project PPTX used as authoritative spec).

The backend is implemented with:
- Python 3.11+
- FastAPI + Uvicorn
- TensorFlow (training & inference)
- OpenCV for video handling
- PostgreSQL (SQLAlchemy + Alembic)
- Redis for caching & pub/sub
- RabbitMQ + Celery for background tasks
- Docker + docker-compose for local dev
- pytest for tests
- GitHub Actions CI example

Features:
- Video ingestion (`POST /ingest/video`) — upload or provide camera URL to create processing job
- Celery pipeline that extracts frames, runs inference, and produces alerts
- Rule-based alerting engine with persistence and pub/sub
- Dashboard APIs for summaries and camera details
- Model training on synthetic data and an inference wrapper that loads the trained model
- JWT authentication
- Prometheus-friendly metrics endpoint (`GET /metrics`)
- WebSocket endpoint `/ws/alerts` for live alerts (extra credit)
- Simple sample dataset generator and training script

Notes:
- The PPTX slides were used to inform functional requirements — section names and phrasing from the PPTX are referenced throughout the README where appropriate (e.g., "Real-time Inference", "Risk Detection Rules", "Dashboard & Alerts").
- All secrets are read from environment variables; see `.env.example`.

Quick start (local demo)
1. Copy `.env.example` to `.env` and adjust values if needed.
2. Build images:
   docker-compose build
3. Start services:
   docker-compose up -d
4. Run migrations and seed an admin user:
   docker-compose exec backend bash -c "alembic upgrade head && python -m app.utils.seed_db"
   (or see "Run migrations and seed" below)
5. Train a demo model with sample data:
   docker-compose exec backend bash -c "bash scripts/run_train.sh"
6. Ingest a sample video (or use RTSP URL):
   curl -X POST "http://localhost:8000/ingest/video" -H "Authorization: Bearer <token>" -F "file=@tests/samples/sample_video.mp4"
   Or:
   curl -X POST "http://localhost:8000/ingest/video" -H "Authorization: Bearer <token>" -H "Content-Type: application/json" -d '{"rtsp_url":"tests/samples/sample_video.mp4"}'
7. Subscribe to live alerts:
   - WebSocket: ws://localhost:8000/ws/alerts
   - Redis pub/sub channel: `alerts`

API summary
- POST /auth/token — get JWT token (seeded admin user)
- POST /ingest/video — upload file or provide camera URL; returns job id
- GET /job/{id} — job status
- POST /alerts — push manual alert
- GET /alerts — query alerts (filters: camera_id, severity, from_ts, to_ts)
- GET /dashboard/summary — aggregated metrics (protected)
- GET /camera/{id}/summary — camera-specific summary (protected)
- GET /metrics — JSON metrics (ingested_jobs, processed_frames, alerts_count)

Repository layout (key files)
- backend/
  - app/main.py
  - app/config.py
  - app/db.py
  - app/auth.py
  - app/models/
  - app/schemas/
  - app/api/ (routers)
  - app/services/
  - app/worker.py
  - app/ml/
  - app/utils/
  - migrations/
  - tests/
  - docker/Dockerfile
  - docker/docker-compose.yml
  - scripts/run_train.sh, run_infer.sh, generate_sample_data.py
  - .env.example
  - ci/ (GitHub Actions example)

Run migrations and seed user
- After bringing up containers:
  docker-compose exec backend bash -c "alembic upgrade head && python -m app.utils.seed_db"
- Default admin user is created from environment variables:
  - ADMIN_USERNAME
  - ADMIN_PASSWORD

Testing
- Run unit & integration tests:
  docker-compose exec backend bash -c "pytest -q"

Deployment notes
- Build and push `backend` image to your registry.
- Use managed PostgreSQL, Redis, and RabbitMQ in production.
- Set environment variables (DB URL, Redis URL, RabbitMQ URL, JWT secret).
- Consider using Gunicorn + Uvicorn workers and enable TLS/SSL at load balancer.

References to PPTX (authoritative sections used)
- "Real-time Inference" — implemented in `app/ml/inference.py`
- "Risk Detection Rules" — implemented in `app/services/alert_engine.py`
- "Dashboard & Alerts" — implemented in `app/api/dashboard.py` and `app/api/alerts.py`

For details and examples, read the rest of this README and open the code.
