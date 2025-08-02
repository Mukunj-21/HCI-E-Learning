import cv2
import os
import numpy as np
from ultralytics import YOLO

# Load YOLOv8 for face detection
yolo_model = YOLO("yolov8n-face.pt")

# Create directories for storing frames and cropped faces
os.makedirs("extracted_frames_yolo", exist_ok=True)
os.makedirs("cropped_faces_yolo", exist_ok=True)

# Open video file
video_path = "Dataset/IMG_6032.MOV"
cap = cv2.VideoCapture(video_path)

# Frame extraction interval
frame_interval = 240
frame_number = 0

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame_number += 1
    
    # Process every 'frame_interval'-th frame
    if frame_number % frame_interval == 0:
        # Rotate frame upside down
        # rotated_frame = cv2.rotate(frame, cv2.ROTATE_180)
        rotated_frame = frame
        
        frame_path = f"extracted_frames_yolo/frame_{frame_number}.jpg"
        cv2.imwrite(frame_path, rotated_frame)

        # Detect faces using YOLOv8
        results = yolo_model(rotated_frame, verbose=False)
        faces = results[0].boxes.xyxy.cpu().numpy()
        confidences = results[0].boxes.conf.cpu().numpy()  # Confidence scores

        face_id = 0
        for box, conf in zip(faces, confidences):
            if conf < 0.8:
                continue  # Skip faces with visibility below 70%

            x1, y1, x2, y2 = map(int, box)
            face_crop = rotated_frame[y1:y2, x1:x2]

            if face_crop.size == 0:
                continue  # Skip empty faces

            face_id += 1
            face_path = f"cropped_faces_yolo/frame_{frame_number}face{face_id}.jpg"
            cv2.imwrite(face_path, face_crop)

cap.release()
print("Frame extraction and face cropping completed.")