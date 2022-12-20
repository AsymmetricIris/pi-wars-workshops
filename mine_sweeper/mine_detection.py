# Bounding rect came from: https://answers.opencv.org/question/200861/drawing-a-rectangle-around-a-color-as-shown/
# Python openCV tutorials: https://docs.opencv.org/master/d6/d00/tutorial_py_root.html


import cv2
import time
import numpy as np
import DualMotorController as DMC

motorController = DMC.DualMotorController(24, 23, 25, 18, 15, 14, 0, 0)

def processImgMask(mask, ogImg, open, close, erode, dilate):
        maskImg = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((open, open), np.uint8), iterations = 1)
        maskImg = cv2.morphologyEx(maskImg, cv2.MORPH_CLOSE, np.ones((close, close), np.uint8), iterations = 2)
        maskImg = cv2.erode(maskImg, np.ones((erode, erode), np.uint8),iterations = 1)
        maskImg = cv2.dilate(maskImg, np.ones((dilate, dilate), np.uint8), iterations = 1)
        maskImg = cv2.bitwise_and(ogImg, ogImg, mask = maskImg)

        maskImg = 255 - maskImg

        return maskImg

# ===========================================================================
# Surbey the area until the target coloured mark has been found

def findColouredArea(mask, frame):
    xg, yg, wg, hg = 0, 0, 0, 0
    targetFound = False
    # the robot should rotate around in order to put the red area in its field of view
    redContour = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) [-2]
    if len(redContour) > 0 :
        red_area = max(redContour, key = cv2.contourArea)
        (xg, yg, wg, hg) = cv2.boundingRect(red_area)
        cv2.rectangle(frame, (xg, yg), (xg + wg, yg + hg), (0, 255, 0), 2)

    centreRedX = xg + (hg/2)
    centreFrameX = len(frame[0])/2
    distRedToCentre = centreRedX - centreFrameX

    # debug
    # print("Frame width: " + str(len(frame[0])))
    # print("Distance: " + str(distRedToCentre))
    
    if xg > 0:
        if distRedToCentre > -75 and distRedToCentre < 75:
            print("Target: centred\nGo straight")
            targetFound = True
        else:
            print("Rotate left")
            motorController.drive(25, -25)

    return mask, frame, targetFound


# ==========================================================================
# Once the coloured target is found, move toward it while keeping track of its position in the camera and adjusting to keep the taret centered
#
# param mask   the filtered image displaying only thered regions of the original frame from the camera
# param frame   the original frame rom the camera
# param targetFound     a boolean for whether or not the target has been found
# param targetSatOn     a boolean for whether the robot has reached its destination

def followColouredArea(mask, frame, targetFound, targetSatOn):
    xg, yg, wg, hg = 0, 0, 0, 0
    # the robot should move toward the red area and adjust to centre the area if it moves to the left or right of the camera's centre
    redContour = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) [-2]
    if len(redContour) > 0 :
        red_area = max(redContour, key = cv2.contourArea)
        (xg, yg, wg, hg) = cv2.boundingRect(red_area)
        cv2.rectangle(frame, (xg, yg), (xg + wg, yg + hg), (0, 255, 0), 2)

    centreRedX = xg + (hg/2)
    centreFrameX = len(frame[0])/2
    distRedToCentre = centreRedX - centreFrameX
    
    # debug
    # print("Frame width: " + str(len(frame[0])))
    
    if xg > 0:
        print("Distance: " + str(distRedToCentre))
        if distRedToCentre > -15 and distRedToCentre < 15:
            print("Target: centred - Go straight")
            motorController.drive(50, 50)
        elif distRedToCentre < -55:
            print("Adjust left\n")
            motorController.drive(25, 50)
        elif distRedToCentre > 55:
            print("Adjust right\n")
            motorController.drive(50, 25)
        else:
            print("Target: sat upon")
            motorController.halt()
            targetSatOn = True
            targetFound = False

    return mask, frame, targetSatOn

cap = cv2.VideoCapture(0)
targetFound = False
targetSatOn = False
targetsSatOn = 0

lower_red = np.array([0, 153, 77])
upper_red = np.array([30, 255, 255])


while(1):
    _, frame = cap.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    mask =  cv2.inRange(hsv, lower_red, upper_red)

    processedImg = processImgMask(mask, frame, 5, 5, 5, 5)

    if targetSatOn == False:
        if targetFound == False:
            mask, frame, targetFound = findColouredArea(mask, frame)
        elif targetFound:
            mask, frame, targetSatOn = followColouredArea(mask, frame, targetFound, targetSatOn)
            if targetSatOn:
                timeTargetSatOn = time.time()
                targetFound = False
                targetsSatOn+=1
                motorController.halt()
    else:
        print("Time since sitting ocurred: " + str(time.time() - timeTargetSatOn))
        if (time.time() - timeTargetSatOn) >= 3:
            targetSatOn = False

    print("Targets sat on: " + str(targetsSatOn))
    cv2.imshow("OG", frame)
    cv2.imshow("Processed 1", processedImg)

    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()
cap.release()
motorController.powerDown()
