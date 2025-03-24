#Author:        Kiryamwibo Yenusu
#contact:       +256 776 656 200
#Email:         kiryamwiboyenusu@gmail.com
#Education:     BSc. Softaware Engineering (Makerere University)
#Home:          Mayuge-Uganda
#github:        www.github.com/yenusu
#stackoverflow: www.stackoverflow.com/users/5442050/kiryamwibo-yenusu
#facebook:      www.facebook.com/yenusu
#twitter:       www.twitter.com/kyenusu
#Linkedin:      www.linkedin.com/yenusu
#date:          24/feb/2018

# This script will detect birds approaching a rice farm via an external camera.
# It is Tested with OpenCV3 on linux ubuntu 16.4 running Python 3 or above

import cv2
import numpy as np
#cap = cv2.VideoCapture(0) #for automatic USBCam (0-web cam default)

class DetectBirds(object):
    def __init__(self, camera_url, mx_num_birds = 1):
        self.cap = cv2.VideoCapture(camera_url)
        self.MAX_NUM_BIRDS = mx_num_birds
        # Object detection from Stable camera
        self.object_detector = cv2.createBackgroundSubtractorMOG2(history=100, varThreshold=40, detectShadows=False)
        self.running = True

    def detect(self):
        frames_counter = 0
        birds_counter = 0
        # Define kernel for noise removal
        kernel = np.ones((3, 3), np.uint8)
        
        while self.running:
            # Capture frame-by-frame from a video
            ret, raw_frame = self.cap.read()
            if ret:
                frames_counter = frames_counter + 1
                # Image preprocessing:
                # 1. Cropping
                # Define crop area (x, y, width, height)
                x, y, w, h = 100, 150, 1000, 400     # set "trees" area 
                frame = raw_frame[y:y+h, x:x+w]      # Crop the frame
                
                # 2. Object Detection
                mask = self.object_detector.apply(frame)
                # **Noise Reduction using Morphological Operations**
                mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)  # Removes small noise
                #mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)  # Closes small gaps
                #_, mask = cv2.threshold(mask, 128, 255, cv2.THRESH_BINARY)
                contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

                #    # Display the resulting frame
                for cnt in contours:
                    # Calculate area and remove small elements
                    area = cv2.contourArea(cnt)
                    if area > 100:
                        #Show image
                        x, y, w, h = cv2.boundingRect(cnt)
                        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
                        cv2.imshow('frame', frame)
                        cv2.imshow('mask', mask)
                        birds_counter = birds_counter + 1
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    self.running = False
            else:
                self.running = False

        # When everything done, release the capture and go back take another one
        print("Processed {} frames, {} of them contains bird(s)".format(frames_counter, birds_counter))
        self.cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    D = DetectBirds("bird_on_tree.mp4")
    D.detect()
    
