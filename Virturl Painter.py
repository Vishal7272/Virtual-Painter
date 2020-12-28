import cv2
import numpy as np
frameWidth = 1000   # define frame size
frameHeight = 1000
cap = cv2.VideoCapture(0)  # For capture webcam
cap.set(3, frameWidth)
cap.set(4, frameHeight)
cap.set(10,150)

myColors = [[5,107,0,19,255,255],   # color HUE list for orange
            [133,56,0,159,156,255], # pirple
            [57,76,0,100,255,255], # green
            [82,115,164,100,250,255]]  #  Blue

## BGR   color Values
myColorValues = [[51,153,255],          # color  value for orange
                 [255,0,255],  #pirple
                 [0,255,0],     # green
                 [255,0,0]]     #blue

myPoints =  []  ## [x , y , colorId ]

def findColor(img,myColors,myColorValues):  # function for find color
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)  #convert img into HSV image
    count = 0
    newPoints=[]
    for color in myColors:  # for detect all color
        lower = np.array(color[0:3])        # lower limit for masking
        upper = np.array(color[3:6])        # upper limit for masking
        mask = cv2.inRange(imgHSV,lower,upper)
        x,y=getContours(mask)
        cv2.circle(imgResult,(x,y),15,myColorValues[count],cv2.FILLED)   # pointing the circle center in the bounding box
        if x!=0 and y!=0:  # when function getContours return 0,0,0, as a value no need to find color
            newPoints.append([x,y,count])  # save value
        count +=1
        #cv2.imshow(str(color[0]),mask)  # to show the bounding box
    return newPoints

def getContours(img):
    contours,hierarchy = cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    x,y,w,h = 0,0,0,0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area>500:
            #cv2.drawContours(imgResult, cnt, -1, (255, 0, 0), 3)  #  to draw the contour
            peri = cv2.arcLength(cnt,True)
            approx = cv2.approxPolyDP(cnt,0.02*peri,True)
            x, y, w, h = cv2.boundingRect(approx)
    return x+w//2,y  # return the Tip( where the contour point) and center

def drawOnCanvas(myPoints,myColorValues):  #to draw the circle at every point
    for point in myPoints:
        cv2.circle(imgResult, (point[0], point[1]), 10, myColorValues[point[2]], cv2.FILLED)  # points for draw circle


while True:
    success, img = cap.read()
    imgResult = img.copy() # images captur by webcam
    newPoints = findColor(img, myColors,myColorValues)
    if len(newPoints)!=0:
        for newP in newPoints:  # for all color point where the circle move
            myPoints.append(newP)
    if len(myPoints)!=0:
        drawOnCanvas(myPoints,myColorValues)  # draw circle at every point


    cv2.imshow("Result", imgResult)  #print result
    if cv2.waitKey(1) & 0xFF == ord('q'):  # press q for quit
        break