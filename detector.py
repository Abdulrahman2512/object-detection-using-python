import cv2
from ultralytics import YOLO

class ObjectDetector:
    def __init__(self):
        self.model = YOLO("yolov8n.pt")
        self.danger_items = ["knife", "scissors", "pistol", "gun", "fire", "axe"]

    def detect(self, frame):
        results = self.model(frame)
        detections = []
        for result in results:
            for box in result.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                class_id = int(box.cls[0])
                conf = float(box.conf[0])
                label = self.model.names[class_id]
                is_danger = label in self.danger_items
                detections.append({"label": label,"confidence": conf,"bbox": (x1, y1, x2, y2),"danger": is_danger})
        return detections
