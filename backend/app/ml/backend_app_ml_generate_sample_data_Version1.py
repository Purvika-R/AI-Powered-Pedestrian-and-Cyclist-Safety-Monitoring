import numpy as np
import cv2
import os

def make_image(size=(128,128)):
    img = np.zeros((size[0], size[1], 3), dtype=np.uint8) + 255
    objects = []
    # random person = red rectangle
    x = np.random.randint(10, 90)
    y = np.random.randint(10, 90)
    w = np.random.randint(10, 20)
    h = np.random.randint(15, 30)
    cv2.rectangle(img, (x,y), (x+w, y+h), (0,0,255), -1)
    objects.append(("person", x, y, w, h))
    # maybe bike
    if np.random.rand() > 0.6:
        x = np.random.randint(10, 100)
        y = np.random.randint(10, 100)
        w = np.random.randint(8, 18)
        h = np.random.randint(8, 18)
        cv2.circle(img, (x,y), 8, (0,255,0), -1)
        objects.append(("bicycle", x, y, w, h))
    # maybe vehicle
    if np.random.rand() > 0.7:
        x = np.random.randint(10, 80)
        y = np.random.randint(10, 80)
        w = np.random.randint(20, 40)
        h = np.random.randint(10, 20)
        cv2.rectangle(img, (x,y), (x+w, y+h), (255,0,0), -1)
        objects.append(("vehicle", x, y, w, h))
    return img, objects

def generate_dataset(n=100):
    X = []
    Y = []
    K=5
    for i in range(n):
        img, objs = make_image()
        img = cv2.resize(img, (128,128))
        X.append(img.astype("float32")/255.0)
        # build y: K rows of [x,y,w,h,p1,p2,p3] normalized
        rows = []
        for j in range(K):
            if j < len(objs):
                cls,mapx,mapy,w,h = objs[j][0], objs[j][1], objs[j][2], objs[j][3], objs[j][4]
                x = mapx/128.0
                y = mapy/128.0
                w = w/128.0
                h = h/128.0
                p = [0.0,0.0,0.0]
                if cls=="person": p[0]=1.0
                if cls=="bicycle": p[1]=1.0
                if cls=="vehicle": p[2]=1.0
            else:
                x=y=w=h=0.0
                p=[0.0,0.0,0.0]
            rows.extend([x,y,w,h]+p)
        Y.append(rows)
    return np.array(X), np.array(Y)