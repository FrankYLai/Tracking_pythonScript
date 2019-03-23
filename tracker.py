import cv2
import numpy as np


class detectMarker:

    def __init__(self):
        self.lowerBoundR2 = np.array([170, 60, 66])
        self.upperBoundR2 = np.array([180, 150, 150])

        self.lowerBoundR1 = np.array([0, 130, 90])
        self.upperBoundR1 = np.array([10, 255, 250])

        self.lowerBoundB1 = np.array([110, 73, 86])
        self.upperBoundB1 = np.array([134, 190, 190])

        self.kernelOpen = np.ones((6, 6))
        self.kernelClose = np.ones((18, 18))

    def bounds(self, img):


        imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        maskR1 = cv2.inRange(imgHSV, self.lowerBoundR1, self.upperBoundR1)
        maskR2 = cv2.inRange(imgHSV, self.lowerBoundR2, self.upperBoundR2)
        maskB1 = cv2.inRange(imgHSV, self.lowerBoundB1, self.upperBoundB1)
        totmask= maskR1 + maskR2 + maskB1

        maskOpen = cv2.morphologyEx(totmask, cv2.MORPH_OPEN, self.kernelOpen)
        maskClose = cv2.morphologyEx(maskOpen, cv2.MORPH_CLOSE, self.kernelClose)

        maskFinal = maskClose
        conts, h = cv2.findContours(maskFinal.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

        largestS = 0
        largest = (0, 0, 0, 0)
        for i in range(len(conts)):
            if np.size(conts[i]) > 400:
                x, y, w, h = cv2.boundingRect(conts[i])
                if w < h:
                    h = w
                else:
                    w = h
                if w > largestS:
                    largestS = w
                    largest = (x, y, w, h)

        #uncomment the following to show the masks and filters during the detection process

        # cv2.imshow("maskClose", maskClose)
        # cv2.imshow("maskOpen", maskOpen)
        # cv2.imshow("R1", maskR1)
        # cv2.imshow("R2", maskR2)
        # cv2.imshow("B1", maskB1)
        # cv2.imshow("mask", totmask)
        # cv2.imshow("cam", img)

        return largest






detector=detectMarker()

cam=cv2.VideoCapture(0)

track=[]

TOL=(20,20,20,20)
posrange=(0,0,0,0)
counter=0

while True:
    ret,frame=cam.read()
    success = False
    if len(track)==0:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        object=detector.bounds(frame)
        multiTracker = cv2.MultiTracker_create()
        cv2.putText(frame, "please hold the marker still and close to the camera",(5,20),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,0,255),2)
        if object != (0,0,0,0):
            if np.all(np.abs(np.subtract(posrange,object)))<8:
                counter+=1
                cv2.rectangle(frame, (object[0], object[1]), (object[0] + object[2], object[2] + object[3]),
                              (0, 0, 255), 2, 1)
                print(counter)
            else:
                counter=0
            posrange=object
            if counter>100:
                multiTracker.add(cv2.TrackerCSRT_create(), frame, object)
                counter=0
        else:
            counter=0


    success, track = multiTracker.update(frame)
    if not success:
        track=[]
        multiTracker.clear()
    for i, newbox in enumerate(track):
        cv2.putText(frame, "tracking", (5, 20), cv2.FONT_HERSHEY_SIMPLEX,
                    0.7, (0, 255, 0), 2)
        p1 = (int(newbox[0]), int(newbox[1]))
        p2 = (int(newbox[0] + newbox[2]), int(newbox[1] + newbox[3]))
        cv2.rectangle(frame, p1, p2, (0,255,0), 2, 1)

        objectframe=frame[int(newbox[1]):int(newbox[1]+newbox[3]), int(newbox[0]):int(newbox[0]+newbox[2])]


    cv2.imshow("feed",frame)

    if cv2.waitKey(30)==ord('q'):
        break

cam.release()
cv2.destroyAllWindows()




