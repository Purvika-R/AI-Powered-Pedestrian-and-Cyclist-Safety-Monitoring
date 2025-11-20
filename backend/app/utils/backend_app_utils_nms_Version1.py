from typing import List, Dict
def iou(a,b):
    x1,y1,w1,h1 = a
    x2,y2,w2,h2 = b
    ax1, ay1, ax2, ay2 = x1, y1, x1+w1, y1+h1
    bx1, by1, bx2, by2 = x2, y2, x2+w2, y2+h2
    inter_x1 = max(ax1, bx1)
    inter_y1 = max(ay1, by1)
    inter_x2 = min(ax2, bx2)
    inter_y2 = min(ay2, by2)
    inter_w = max(0, inter_x2 - inter_x1)
    inter_h = max(0, inter_y2 - inter_y1)
    inter_area = inter_w * inter_h
    area_a = w1 * h1
    area_b = w2 * h2
    union = area_a + area_b - inter_area
    if union == 0:
        return 0
    return inter_area / union

def nms(detections: List[Dict], iou_threshold=0.5):
    detections = sorted(detections, key=lambda x: x["score"], reverse=True)
    keep = []
    for d in detections:
        skip = False
        for k in keep:
            if iou(d["bbox"], k["bbox"]) > iou_threshold and d["class"] == k["class"]:
                skip = True
                break
        if not skip:
            keep.append(d)
    return keep