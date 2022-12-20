import cv2
import numpy as np

cam = cv2.VideoCapture(0)

while True:
    __, frame = cam.read()
    cv2.imshow("Feed", frame)
    k = cv2.waitKey(25)
    if k == ord('q'): 
        break

cam.release()
cv2.destoryAllWindows()
