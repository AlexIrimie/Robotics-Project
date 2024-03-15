import cv2

num_cameras = 4  # Adjust the number based on your setup

for i in range(num_cameras):
    cap = cv2.VideoCapture(i)
    if not cap.isOpened():
        print(f"Camera {i} not found!")
    else:
        print(f"Camera {i} is ready.")
        cap.release()
