import os
import cv2
import numpy as np


def _ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)


def run_demo(output_dir: str = "artifacts") -> str:
    _ensure_dir(output_dir)

    img = np.zeros((400, 400, 3), dtype=np.uint8)
    # Blue circle (ignored by detector), Red rectangle (detected)
    cv2.circle(img, (100, 300), 40, (255, 0, 0), -1)  # BGR
    cv2.rectangle(img, (100, 100), (300, 300), (0, 0, 255), -1)

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower1 = np.array([0, 120, 70])
    upper1 = np.array([10, 255, 255])
    lower2 = np.array([170, 120, 70])
    upper2 = np.array([180, 255, 255])
    mask = cv2.inRange(hsv, lower1, upper1) | cv2.inRange(hsv, lower2, upper2)

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    annotated = img.copy()
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        cv2.rectangle(annotated, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(annotated, "red", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2, cv2.LINE_AA)

    out_path = os.path.join(output_dir, "color_detection.png")
    cv2.imwrite(out_path, annotated)
    return out_path
