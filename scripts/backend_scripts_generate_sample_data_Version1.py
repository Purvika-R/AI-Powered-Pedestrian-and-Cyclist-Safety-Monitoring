from app.ml.generate_sample_data import generate_dataset
import numpy as np
import os
X,y = generate_dataset(10)
os.makedirs("tests/samples", exist_ok=True)
import cv2
for i,img in enumerate((X*255).astype('uint8')):
    cv2.imwrite(f"tests/samples/img_{i}.png", img)
print("Saved sample images in tests/samples")