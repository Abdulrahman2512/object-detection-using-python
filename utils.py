import cv2
import pandas as pd
from datetime import datetime

def draw_box(frame, x1, y1, x2, y2, label, conf, danger=False):
    color = (0, 0, 255) if danger else (0, 255, 0)
    cv2.rectangle(frame, (x1, y1), (x2, y2), color, 3)
    cv2.putText(frame, f"{label} {conf:.2f}", (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)

def log_detection(label, confidence, danger):
    df = pd.DataFrame([[datetime.now(), label, confidence, danger]],
                      columns=["Time", "Object", "Confidence", "Danger"])
    df.to_csv("logs/detections.csv", mode='a', header=False, index=False)
