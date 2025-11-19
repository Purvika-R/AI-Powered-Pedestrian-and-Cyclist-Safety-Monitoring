import pytest
import numpy as np
from app.ml.generate_sample_data import generate_dataset
from app.ml.train import train
from app.ml.inference import InferenceModel
import os

def test_train_and_infer(tmp_path):
    model_dir = str(tmp_path / "models")
    # run small train
    from app.ml.train import train as t
    out = t(output_dir=model_dir)
    assert os.path.exists(out)
    inf = InferenceModel(model_dir)
    samples, _ = generate_dataset(2)
    # convert to bgr uint8 frames
    frame = (samples[0]*255).astype('uint8')
    dets = inf.predict(frame)
    assert isinstance(dets, list)