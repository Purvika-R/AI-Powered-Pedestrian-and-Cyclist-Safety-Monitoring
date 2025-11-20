import threading
import redis
import json
import asyncio
from ..config import settings

r = redis.from_url(settings.REDIS_URL, decode_responses=True)

_metrics = {"ingested_jobs": 0, "processed_frames": 0, "alerts_count": 0}
__current_model = {"version": None, "path": None}


def publish_alert(msg: dict):
    r.publish("alerts", json.dumps(msg))
    _metrics["alerts_count"] += 1


def increment_metric(k: str, n: int = 1):
    _metrics[k] = _metrics.get(k, 0) + n


def metrics():
    return _metrics


def set_model_info(version, path):
    __current_model["version"] = version
    __current_model["path"] = path


def current_model_info():
    return __current_model


# Websocket bridge: simple thread that reads redis pubsub and yields messages via an async generator
_subscribers = []


def start_redis_listener():
    thread = threading.Thread(target=_redis_listener_thread, daemon=True)
    thread.start()


def _redis_listener_thread():
    pub = r.pubsub()
    pub.subscribe("alerts")
    for msg in pub.listen():
        if msg and msg.get("type") == "message":
            data = json.loads(msg.get("data"))
            for q in list(_subscribers):
                try:
                    q.put_nowait(data)
                except asyncio.QueueFull:
                    pass


async def websocket_subscribe():
    q = asyncio.Queue(maxsize=100)
    _subscribers.append(q)
    try:
        while True:
            item = await q.get()
            yield item
    finally:
        _subscribers.remove(q)