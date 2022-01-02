import time
import cv2
from chat import *
from threading import Thread
from queue import Queue
import time

class Module:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.chat = Chat()
        self.countdown = 0
        pass

    def error(self,message):
        print("\033[91m" + "[ERROR] {} \033[0m".format(message))
        exit()

    
    def get_frame(self):
        ret, frame = self.cap.read()
        return ret,frame

    def detect_motion(self,frame,frame1,frame2):
        frameDelta = cv2.absdiff(frame1, frame2)
        thresh = cv2.threshold(frameDelta, 30, 255, cv2.THRESH_BINARY)[1]
        thresh = cv2.dilate(thresh, None, iterations=2)
        contours,_ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE)

        motion_list = []
        for c in contours:
            area = cv2.contourArea(c)
            
            if area < 1500:
                continue
            if time.time() - self.countdown > 5 or self.countdown==0:
                thread = Thread(target=self.update_telegram, args=(frame,))
                thread.daemon = True
                thread.start()
                self.countdown = time.time()
        
            motion_list.append(c)
        return motion_list

    def draw_rectangle(self,frame,contours):
        temp = frame.copy()
        for c in contours:
            x, y, w, h = cv2.boundingRect(c)
            cv2.rectangle(temp, (x, y), (x + w, y + h), (0, 255, 0), 2)
        return temp

    def update_telegram(self,frame):
        cv2.imwrite("temp.jpg", frame)
        self.chat.send_message("Motion detected at {}".format(time.strftime("%H:%M:%S")))