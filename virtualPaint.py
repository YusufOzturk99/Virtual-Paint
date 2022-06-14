import cv2
from matplotlib.pyplot import draw 
import numpy as np

frameWidth = 640
frameHeight = 480
cap = cv2.VideoCapture(0)
cap.set(3, frameWidth)
cap.set(4, frameHeight)
cap.set(10, 150)

myColors = [54,114, 0, 79, 255, 255]
myColorValues = [0, 255, 0] #BGR

myPoints = []

def findColor(img, myColors, myColorValues):
    imgHvs = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower = np.array(myColors[0:3])
    upper = np.array(myColors[3:6])
    mask = cv2.inRange(imgHvs, lower, upper)
    newPoints = []
    x,y = getContours(mask) 
    cv2.circle(imgResult, (x,y), 10, myColorValues, cv2.FILLED) 

    if x!=0 and y != 0:
        newPoints.append([x,y])

    return newPoints

def getContours(img):
    contours, hiearchy = cv2.findContours(img, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    x,y,w,h = 0,0,0,0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area>500:
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02*peri, True)
            x,y,w,h = cv2.boundingRect(approx)
    return x+w//2, y

def drawOnCanvas(myPoints, myColorValues):
    for point in myPoints:
        cv2.circle(imgResult, (point[0], point[1]), 10, myColorValues, cv2.FILLED)

while True:
    succes, img = cap.read()
    imgResult = img.copy()
    newPoints = findColor(img, myColors, myColorValues)

    if len(newPoints) !=0:
        for newP in newPoints:
            myPoints.append(newP)
            
        drawOnCanvas(myPoints,myColorValues)

    cv2.imshow("Result", imgResult)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break