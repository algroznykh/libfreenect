#!/usr/bin/env python
import freenect
import cv2
import frame_convert2
import numpy as np

import pyautogui
pyautogui.FAILSAFE = False

threshold1 = 500
threshold2 = 300
current_depth = 0

range_x, range_y = 640, 480
resolution = pyautogui.getInfo()[-2]
k_x, k_y = resolution[0] / range_x, resolution[1] / range_y
print(k_x, k_y)

mouseDown = False

# camera = pyfakewebcam.FakeWebcam('/dev/video1', 640, 480)


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

    ind = np.argwhere(depth>0)
    m_x, m_y = np.median(ind[:,1]), np.median(ind[:, 0])
    print(m_x, m_y)
    c_x, c_y = resolution[0] - m_x * k_x, m_y * k_y
    try:
        pyautogui.moveTo(c_x, c_y)
        if not mouseDown:
            pyautogui.mouseDown()
            mouseDown = True
    except ValueError as e:
        print('valueerror', e)
        if mouseDown:
            pyautogui.mouseUp()
            mouseDown = False

def show_video():
    cv2.imshow('Video', frame_convert2.video_cv(freenect.sync_get_video()[0]))


cv2.namedWindow('Depth')
# cv2.namedWindow('Video')

print('Press ESC in window to stop')


while 1:
    show_depth()
    # show_video()
    if cv2.waitKey(10) == 27:
        break
