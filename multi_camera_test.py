import cv2

num_cameras = 2  # Adjust the number based on your setup

# Open all cameras
caps = [cv2.VideoCapture(i) for i in range(num_cameras)]

while True:
    frames = [cap.read()[1] for cap in caps]

    # Display frames
    for i, frame in enumerate(frames):
        cv2.imshow(f"Camera {i}", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release all cameras
for cap in caps:
    cap.release()
cv2.destroyAllWindows()
