import cv2
import tkinter as tk
from PIL import Image, ImageTk
from detector import ObjectDetector
from utils import draw_box, log_detection
from alert import speak_alert
import time  # for interval timing

detector = ObjectDetector()

# Variables for detection interval
last_detection = 0
DETECTION_DELAY = 1.5 # seconds

# Store the last detections to keep showing boxes until next detection
current_detections = []

def update_frame():
    global last_detection, current_detections
    ret, frame = cap.read()
    if not ret:
        return

    current_time = time.time()

    # Run detection every DETECTION_DELAY seconds
    if current_time - last_detection > DETECTION_DELAY:
        current_detections = detector.detect(frame)
        last_detection = current_time
        # Trigger alerts for dangerous objects
        for obj in current_detections:
            if obj["danger"]:
                speak_alert(f"Warning! {obj['label']} detected")
            log_detection(obj["label"], obj["confidence"], obj["danger"])

    # Draw boxes from last detections
    for obj in current_detections:
        x1, y1, x2, y2 = obj["bbox"]
        draw_box(frame, x1, y1, x2, y2, obj["label"], obj["confidence"], obj["danger"])

    img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    imgtk = ImageTk.PhotoImage(img)
    lbl.imgtk = imgtk
    lbl.configure(image=imgtk)
    lbl.after(10, update_frame)

cap = cv2.VideoCapture(0)
root = tk.Tk()
root.title("Smart Object Detection & Danger Alert System")
lbl = tk.Label(root)
lbl.pack()

update_frame()
root.mainloop()

cap.release()
cv2.destroyAllWindows()
