import cv2
import numpy as np

def resize_and_normalize(img, size=(128,128)):
    im = cv2.resize(img, size)
    return (im.astype("float32")/255.0)