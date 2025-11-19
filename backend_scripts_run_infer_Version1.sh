#!/usr/bin/env bash
python -c "from app.ml.inference import InferenceModel; m=InferenceModel('/app/models'); print('Loaded', m.model_path)"