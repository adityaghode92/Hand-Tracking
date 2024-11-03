import cv2
from cvzone.HandTrackingModule import HandDetector
import socket

# Webcam
cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 360)

# Hand Detector
detector = HandDetector(maxHands=1, detectionCon=0.8)

# # communication
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serverAddressPort = ("127.0.0.1", 5052)

while True:

    # get the frames from webCam

    success, img = cap.read()
    # Hands
    hands, img = detector.findHands(img)

    # data to be transfer
    data = []

    # landmark = (x,y,z)*21
    if hands:
        hand = hands[0]
        lmList = hand['lmList']
        print(lmList)

        for lm in lmList:
            data.extend([lm[0], 360 - lm[1], lm[2]])
        print(data)
        sock.sendto(str.encode(str(data)), serverAddressPort)

    cv2.imshow("Image", img)
    cv2.waitKey(1)
