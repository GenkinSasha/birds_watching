import cv2
import numpy as np
import time

# RTSP Stream URL
rtsp_url = "rtsp://10.0.0.6:10554/udp/av0_0"

# Open video stream
cap = cv2.VideoCapture(rtsp_url)

if not cap.isOpened():
    print("Error: Could not open RTSP stream")
    exit()

# Read the first 3 frames
ret, frame1 = cap.read()
ret, frame2 = cap.read()
ret, frame3 = cap.read()
frame_count = 3

while True:
    if not ret:
        print("Failed to grab frame")
        break

    frame_count += 1

    # Define crop area (x, y, width, height)
    x, y, w, h = 0, 0, 1200, 500  	 # Cut road with moving cars off
    cropped_frame1 = frame1[y:y+h, x:x+w]  # Crop the frames
    cropped_frame2 = frame2[y:y+h, x:x+w]  # Crop the frames
    cropped_frame3 = frame3[y:y+h, x:x+w]  # Crop the frames


    # Convert frames to grayscale for better motion detection
    gray1 = cv2.cvtColor(cropped_frame1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(cropped_frame2, cv2.COLOR_BGR2GRAY)
    gray3 = cv2.cvtColor(cropped_frame3, cv2.COLOR_BGR2GRAY)

    # Compute absolute difference between frames
    diff1 = cv2.absdiff(gray1, gray2)
    diff2 = cv2.absdiff(gray2, gray3)

    # Combine differences
    motion_mask = cv2.bitwise_and(diff1, diff2)

    # weak wind - 0..5 
    # Apply threshold to ignore small movements: all pixels < 30 ? 0, all = 30 ? 255
    #_, motion_mask = cv2.threshold(motion_mask, 30, 255, cv2.THRESH_BINARY)
    motion_mask = cv2.adaptiveThreshold(motion_mask, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

    # Count nonzero pixels (movement intensity)
    motion_level = np.count_nonzero(motion_mask)
    print("\nmotion level="+ str(motion_level))

    # Only show movement if it exceeds a threshold
    if motion_level >= 30:  # Adjust sensitivity
        print("Significant movement detected!")
        filename = f"frame_{frame_count:04d}.jpg"
        #cv2.imshow("Motion Mask", motion_mask)  # Show detected movement
        cv2.imwrite(filename, motion_mask)  # Save frame as image
        print(f"Saved: {filename}")

    # Shift frames for next comparison
    frame1, frame2, frame3 = frame2, frame3, cap.read()[1]
    #filename = f"frame_{frame_count:04d}.jpg"
    #cv2.imwrite(filename, frame)  # Save frame as image
    #print(f"Saved: {filename}")

    time.sleep(1)  # Wait for 1 second before capturing next frame

cap.release()
cv2.destroyAllWindows()
