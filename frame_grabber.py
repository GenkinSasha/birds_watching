import cv2
import time

# RTSP Stream URL
rtsp_url = "rtsp://10.0.0.6:10554/udp/av0_0"

# Open video stream
cap = cv2.VideoCapture(rtsp_url)

if not cap.isOpened():
    print("Error: Could not open RTSP stream")
    exit()

frame_count = 0

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break

    frame_count += 1
    filename = f"frame_{frame_count:04d}.jpg"
    cv2.imwrite(filename, frame)  # Save frame as image
    print(f"Saved: {filename}")

    time.sleep(1)  # Wait for 1 second before capturing next frame

cap.release()
cv2.destroyAllWindows()
