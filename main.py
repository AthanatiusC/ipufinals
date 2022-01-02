import cv2
import numpy as np
from module import *

module = Module()
frame1 = None
frame2 = None

if __name__ == '__main__':
    while True:
        ret,frame = module.get_frame()
        if not ret:
            module.error('Failed to get frame')
            continue
        frame1 = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame1 = cv2.GaussianBlur(frame1, (21, 21), 0)
        
        if frame2 is None:
            frame2 = frame1
            continue

        det_list = module.detect_motion(frame,frame1,frame2)
        show = module.draw_rectangle(frame,det_list)

        cv2.imshow("frame", show)
        frame2= None
        frame = None
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break