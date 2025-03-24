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
import time
#cap = cv2.VideoCapture(0) #for automatic USBCam (0-web cam default)

class DetectBirds(object):
    def __init__(self, camera_url, mx_num_birds = 1):
        self.cap = cv2.VideoCapture(camera_url)
        self.birdsCascade = cv2.CascadeClassifier("birds.xml")
        if self.birdsCascade.empty():
            print("Error: Cascade file not found!")
        self.MAX_NUM_BIRDS = mx_num_birds
        self.running = True

    def detect(self):
        frames_counter = 0
        birds_counter = 0
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
                frame = cv2.resize(frame, (640, 480))   # resize to 640*480

                # 2. convert the frame into gray scale for better analysis
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                # 3. Improve contrast  (Histogram Equalization)
                gray = cv2.equalizeHist(gray)
                # Processing:
                # Detect birds in the gray scale image
                birds = self.birdsCascade.detectMultiScale(
                    gray,
                    scaleFactor=1.05, #1.4,
                    minNeighbors=3,
                    #minSize=(15, 15),#(30,30), #(10, 10),
                    #minSize=(10, 10),
                    maxSize=(30, 30), #(50, 50),
                    flags = cv2.CASCADE_SCALE_IMAGE
                )
                if (len(birds)>=self.MAX_NUM_BIRDS):
                    print("Processed frames", frames_counter)
                    print("Detected {0} birds".format(len(birds)))
                    birds_counter = birds_counter + 1

                    # Draw a rectangle around the detected birds
                    for (x, y, w, h) in birds:
                        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 200, 0), 2)


                    # Display the resulting frame
                    cv2.imshow('frame', frame)
                    time.sleep(0.1)
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        self.running = False
            else:
                self.running = False

        # When everything done, release the capture and go back take another one
        print("Processed {} frames, {} of them contains bird(s)".format(frames_counter, birds_counter))
        self.cap.release()
        cv2.destroyAllWindows()

# Create the haar cascade that reads the properties of objects to be detected from an already made xml file.
# The xml file is generated as a result of machine learning from all possible object samples provided.


if __name__ == "__main__":
    #D1 = DetectBirds("tree_on_wind_#1.mp4")
    #D1.detect()
    #D2 = DetectBirds("tree_on_wind_#2.mp4")
    #D2.detect()
    #D3 = DetectBirds("tree_on_wind_#3.mp4")
    #D3.detect()
    #D4 = DetectBirds("tree_on_wind_#4.mp4")
    #D4.detect()
    D5 = DetectBirds("bird_on_tree.mp4")
    D5.detect()
    #D6 = DetectBirds("birds.mp4")
    #D6.detect()
    
