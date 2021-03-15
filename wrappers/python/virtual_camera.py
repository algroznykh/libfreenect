#!/usr/bin/env python
import freenect
import cv2
import frame_convert2
import numpy as np

import pyautogui
pyautogui.FAILSAFE = False

import pyfakewebcam

threshold1 = 500
threshold2 = 300
current_depth = 0

range_x, range_y = 640, 480
resolution = pyautogui.getInfo()[-2]
k_x, k_y = resolution[0] / range_x, resolution[1] / range_y
print(k_x, k_y)

mouseDown = False

camera = pyfakewebcam.FakeWebcam('/dev/video1', 640, 480)


def show_depth():
    global mouseDown
    global threshold1
    global threshold2
    global current_depth

    depth, timestamp = freenect.sync_get_depth()
    depth = 255 * np.logical_and(depth >= current_depth - threshold1,
                                 depth <= current_depth + threshold1)
    depth = depth.astype(np.uint8)
    cv2.imshow('Depth', depth)

    frame = np.zeros((480, 640, 3), dtype=np.uint8)

    frame[:,:,0] = depth
    
    camera.schedule_frame(frame)


cv2.namedWindow('Depth')
# cv2.namedWindow('Video')

print('Press ESC in window to stop')


while 1:
    show_depth()
    if cv2.waitKey(10) == 27:
        break

