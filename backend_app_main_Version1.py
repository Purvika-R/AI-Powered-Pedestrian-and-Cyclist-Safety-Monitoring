from fastapi import FastAPI, Depends, WebSocket
from fastapi.middleware.cors import CORSMiddleware

from .config import settings
from .api import health, ingest, alerts, dashboard, auth as auth_router, models as models_api
from .utils import events

app = FastAPI(title="AI-Pedestrian-Cyclist Safety Monitoring Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, prefix="/health")
app.include_router(auth_router.router, prefix="/auth")
app.include_router(ingest.router, prefix="/ingest")
app.include_router(alerts.router, prefix="/alerts")
app.include_router(dashboard.router, prefix="/dashboard")
app.include_router(models_api.router, prefix="/models")


@app.on_event("startup")
async def startup_event():
    # initialize pubsub listener (bridge alerts to websocket)
    events.start_redis_listener()


@app.get("/metrics")
async def metrics():
    return events.metrics()


@app.websocket("/ws/alerts")
async def websocket_alerts(ws: WebSocket):
    await ws.accept()
    async for msg in events.websocket_subscribe():
        await ws.send_json(msg)