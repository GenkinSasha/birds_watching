#Author:      Alexander Genkin
#Email:       Genkin.Sasha@gmail.com
#Date:        2025

# This script will detect birds approaching a rice farm via an external camera.
# It is Tested with OpenCV3 on linux ubuntu 16.4 running Python 3 or above

import cv2
import os
import numpy as np
import birds_mathlib
from dataclasses import dataclass

#cap = cv2.VideoCapture(0) #for automatic USBCam (0-web cam default)

@dataclass
class Object:
    frame_number: int
    mass_centre: int
    square: int

class ObjectsList:    
    def __init__(self, max_list_size = 100):
        self.MAX_LIST_SIZE = max_list_size
        self.items = []

    def add(self, frame_number, mass_centre, square):
        if len(self.items) < self.MAX_LIST_SIZE:
            self.items.append(Object(frame_number, mass_centre, square))

    def modify(self, index, frame_number=None, mass_centre=None, square=None):
        """Modify an existing person based on index."""
        if 0 <= index < len(self.items):
            if frame_number is not None:
                self.items[index].frame_number = frame_number
            if mass_centre is not None:
                self.items[index].mass_centre = mass_centre
            if square is not None:
                self.items[index].square = square
        else:
            print("Error: Index out of range!")

    def display(self):
        """Print all people in the list."""
        for i, item in enumerate(self.items):
            print(f"frame_number: {item.frame_number}, mass_centre: {item.mass_centre}, square: {item.square}")
            
    def getByFrameNumber(self, frame_number):
        """Return a list """
        return [(ind, item) for ind, item in enumerate(self.items) if item.frame_number == frame_number]        
        
    def isEmpty(self):
        return len(self.items) == 0

class Tracker:
    
    def __init__(self, centre_moving = 20, square_change = 20):
        self.birds_list = ObjectsList()
        self.birds_count = 0
        self.CENTRE_MOVING = centre_moving
        self.SQUARE_CHANGE = square_change
        
    def addObjectToTrack(self, frames_counter, box):
        mass_centre = birds_mathlib.massCentre(box)
        square = birds_mathlib.Square(box)
        self.birds_count = self.birds_count + 1
        self.birds_list.add(frames_counter, mass_centre, square)

    def printAll(self):
        if self.birds_list.isEmpty():
            print("No objects to track")
        else:
            self.birds_list.display()
            print("Tracked ", len(self.birds_list.items), "birds(?)")

    # find closest by Eucleadean distance box in the list
    def getClosest(self, frames_counter, box):
        prev_frame_objects = self.birds_list.getByFrameNumber(frames_counter)   # returns list, usually {1}
        return 
        
    def track(self, frames_counter, bounding_box):
        mass_centre = birds_mathlib.massCentre(bounding_box)
        square = birds_mathlib.Square(bounding_box)
        print("mass_centre=", mass_centre, "square=", square)
        
        prev_frame_objects = self.birds_list.getByFrameNumber(frames_counter - 1) # get all boxes from prev. frame
        #print(prev_frame_objects)

        if prev_frame_objects:            
            dist_v = [(index, birds_mathlib.distEuclides(bird_obj.mass_centre, mass_centre)) for index, bird_obj in prev_frame_objects] 
            #print("dist_v=", dist_v)        
            min_index, min_dist = min(dist_v, key=lambda x: x[1])  
            #print(min_index, min_dist)
            if min_dist < self.CENTRE_MOVING:# and  diffSq < self.SQUARE_CHANGE:
                print("Frame ", frames_counter, ": modify tracked object ", min_index)
                # it is the same object as in frame N-1 - update it
                self.birds_list.modify(min_index, frames_counter, mass_centre, square)
                is_new_added = False
            else:
                print("Frame ", frames_counter, ": difference are too big, add new tracked object ")
                self.addObjectToTrack(frames_counter, bounding_box)
                is_new_added = True

        else:
            print("Frame ", frames_counter, ": add new tracked object ")
            self.addObjectToTrack(frames_counter, bounding_box)
            is_new_added = True
        return is_new_added

class DetectBirds(object):
    HISTORY = 100
    
    def __init__(self, camera_url, mx_num_birds = 1):
        self.cap = cv2.VideoCapture(camera_url)
        self.MAX_NUM_BIRDS = mx_num_birds        
        # Object detection from Stable camera
        self.object_detector = cv2.createBackgroundSubtractorMOG2(history=DetectBirds.HISTORY, varThreshold=40, detectShadows=False)
        self.tracker = Tracker(20, 20)
        self.running = True

    def preDetect(self):
        # Read first self.HISTORY frames to learn the algorithm
        for frames_counter in range(DetectBirds.HISTORY):
            ret, raw_frame = self.cap.read()
            if not ret:
                self.running = False
        
    def detect(self):
        frames_counter = 0
        birds_counter = 0
        # Define kernel for noise removal
        kernel = np.ones((3, 3), np.uint8)
        
        self.preDetect()
           
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
                
                # 2. Clean the moving backgroung from noises
                #_, mask = cv2.threshold(mask, 128, 255, cv2.THRESH_BINARY)
                mask = self.object_detector.apply(frame)
                # **Noise Reduction using Morphological Operations**
                mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)  # Removes small noise
                #mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)  # Closes small gaps
                
                # 3. Object Detection
                contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
                #    # Display the resulting frame
                for cnt in contours:
                    # Calculate area and remove small elements
                    area = cv2.contourArea(cnt)
                    if area > 100:
                        #Show image
                        x, y, w, h = cv2.boundingRect(cnt)
                        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
                        #print("frames_counter=", frames_counter)
                        is_new_bird = self.tracker.track(frames_counter, [x, y, w, h])
                        if is_new_bird:
                            birds_counter = birds_counter + 1
                            cv2.imwrite(f"birds_images/bird_{birds_counter}.jpg", frame)
                        cv2.imshow('frame', frame)
                        #cv2.imshow('mask', mask)                        
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    self.running = False
            else:
                self.running = False

        # When everything done, release the capture and go back take another one
        print("Processed {} frames, {} of them contains bird(s)".format(frames_counter, birds_counter))
        self.tracker.printAll()
        self.cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    directory = "birds_images"    # Create the directory if it does not exist
    os.makedirs(directory, exist_ok=True)
    
    D = DetectBirds("bird_on_tree.mp4")
    D.detect()
    
