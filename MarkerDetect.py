import cv2
import numpy as np

lowerBoundR2 = np.array([170,60,66])
upperBoundR2 = np.array([180,150,150])

lowerBoundR1 = np.array([0,110,90])
upperBoundR1 = np.array([10,255,250])

lowerBoundB1 = np.array([112,73,86])
upperBoundB1 = np.array([134,190,190])


cam = cv2.VideoCapture(0)
kernelOpen = np.ones((6, 6))
kernelClose = np.ones((20, 20))


while True:
    ret, img = cam.read()
    #img = cv2.resize(img, (340, 250))

    # convert BGR to HSV
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # create the Mask
    maskR1 = cv2.inRange(imgHSV, lowerBoundR1, upperBoundR1)
    maskR2 = cv2.inRange(imgHSV, lowerBoundR2, upperBoundR2)
    maskB1 = cv2.inRange(imgHSV, lowerBoundB1, upperBoundB1)
    totmask= maskR1 + maskR2 + maskB1
    # morphology
    maskOpen = cv2.morphologyEx(totmask, cv2.MORPH_OPEN, kernelOpen)
    maskClose = cv2.morphologyEx(maskOpen, cv2.MORPH_CLOSE, kernelClose)

    maskFinal = maskClose
    conts, h = cv2.findContours(maskFinal.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    # deleteVal=[]
    # for i in range(len(conts)):
    #     if np.size(conts[i])<500:
    #         deleteVal.append(i)
    #
    # subtract=0
    # for i in deleteVal:
    #     del(conts[i-subtract])
    #     subtract+=1
    #
    # for i in range(len(conts)):
    #     x, y, w, h = cv2.boundingRect(conts[i])
    #     if w<h:
    #         h=w
    #     else:
    #         w=h
    #     cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)

    largestS=0
    largest=(0,0,0,0)
    for i in range(len(conts)):
        if np.size(conts[i]) > 500:
            x,y,w,h=cv2.boundingRect(conts[i])
            if w<h:
                h=w
            else:
                w=h
            if w>largestS:
                largestS=w
                largest=(x,y,w,h)

    x,y,w,h=largest
    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)

    #cv2.drawContours(img, conts, -1, (255, 0, 0), 3)

    cv2.imshow("maskClose", maskClose)
    cv2.imshow("maskOpen", maskOpen)
    cv2.imshow("R1", maskR1)
    cv2.imshow("R2", maskR2)
    cv2.imshow("B1", maskB1)
    cv2.imshow("mask", totmask)
    cv2.imshow("cam", img)
    if cv2.waitKey(10)==ord("q"):
        break