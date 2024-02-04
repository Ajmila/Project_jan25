import cv2
import numpy as np
from datetime import datetime

class VideoCaptureManager:
    def __init__(self, frame_size=(640, 480), codec='XVID'):
        self.frame_size = frame_size
        self.codec = codec
        self.is_capturing = False
        self.capture_duration = 0
        self.frames_buffer = []  # Store frames in a temporary buffer

    def start_capture(self, capture_duration):
        self.capture_duration = capture_duration
        self.is_capturing = True

        # Open the default camera (camera index 0)
        cap = cv2.VideoCapture(0)

        # Add the namedWindow line
        cv2.namedWindow('Video Capture', cv2.WINDOW_NORMAL)

        start_time = cv2.getTickCount()
        while self.is_capturing:
            ret, frame = cap.read()

            if not ret:
                print("Failed to capture video.")
                break

            self.frames_buffer.append(frame)

            # Add the namedWindow line
            cv2.imshow('Video Capture', frame)

            # Bring the window to the front
            cv2.setWindowProperty('Video Capture', cv2.WND_PROP_TOPMOST, 1)

            # Break the loop if 'q' key is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                self.stop_capture()

            elapsed_time = (cv2.getTickCount() - start_time) / cv2.getTickFrequency()
            if elapsed_time >= self.capture_duration:
                self.stop_capture()

        # Release resources after capturing is done
        cap.release()
        cv2.destroyAllWindows()

    def stop_capture(self):
        self.is_capturing = False
    
    def read_frames_from_buffer(self):
        return self.frames_buffer
    
    def reduce_frame_count(self,frames_arr):
        self.frames = []
        self.frames.append(frames_arr[0])
        orb = cv2.ORB_create()
        bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
        for i in range(1, len(frames_arr)):
            keypoints1, descriptors1 = orb.detectAndCompute(self.frames[-1], None)
            keypoints2, descriptors2 = orb.detectAndCompute(frames_arr[i], None)
            matches = bf.match(descriptors1, descriptors2)
            if len(matches) < 300:
                self.frames.append(frames_arr[i])
        return self.frames
   
    
    def read_video(self):
        self.video = cv2.VideoCapture('Data/Video/input2.MOV')
        
        self.frames_arr = []
        while self.video.isOpened():
            ret, frame = self.video.read()

            if not ret:
                break
            self.frames_arr.append(frame)                                         # Frames stored in frames_arr
            
        self.video.release()
        return self.frames_arr
    
    
    
    

