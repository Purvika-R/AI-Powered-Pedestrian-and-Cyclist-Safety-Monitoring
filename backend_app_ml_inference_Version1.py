import tensorflow as tf
import numpy as np
import os
from typing import List, Dict
from ..utils.opencv import resize_and_normalize
from ..utils.nms import nms

class InferenceModel:
    """
    Loads a tiny TF model which outputs a fixed number of boxes (K) with
    format [x, y, w, h, p_person, p_bicycle, p_vehicle]
    Coordinates normalized [0,1]
    """
    def __init__(self, model_dir: str):
        self.model_path = self.find_latest_model(model_dir)
        self.model = None
        if self.model_path:
            self.model = tf.keras.models.load_model(self.model_path)
        else:
            # if no model, create a dummy that returns empty list
            self.model = None

    def find_latest_model(self, model_dir):
        if not os.path.exists(model_dir):
            os.makedirs(model_dir, exist_ok=True)
            return None
        files = [os.path.join(model_dir, f) for f in os.listdir(model_dir) if os.path.isdir(os.path.join(model_dir, f))]
        if not files:
            return None
        latest = max(files, key=os.path.getmtime)
        return latest

    def predict(self, frame) -> List[Dict]:
        if self.model is None:
            return []
        img = resize_and_normalize(frame, (128, 128))
        inp = np.expand_dims(img, axis=0)
        raw = self.model.predict(inp, verbose=0)[0]  # shape (K, 7) flattened?
        K = raw.shape[0] // 7 if raw.ndim==1 else raw.shape[0]
        if raw.ndim==1:
            raw = raw.reshape((K,7))
        detections = []
        for row in raw:
            x, y, w, h = row[:4].tolist()
            scores = row[4:]
            cls_idx = int(np.argmax(scores))
            cls_map = {0: "person", 1: "bicycle", 2: "vehicle"}
            score = float(scores[cls_idx])
            bbox = [int(x*frame.shape[1]), int(y*frame.shape[0]), int(w*frame.shape[1]), int(h*frame.shape[0])]
            detections.append({"bbox": bbox, "class": cls_map.get(cls_idx, "unknown"), "score": score})
        # basic NMS
        detections = nms(detections, iou_threshold=0.3)
        return detections