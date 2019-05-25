import numpy as np
import cv2 as cv

import paho.mqtt.client as mqtt
client=mqtt.Client("control1")
client.connect("172.18.0.2", port=1883, keepalive=60)

face_cascade = cv.CascadeClassifier('/usr/share/OpenCV/haarcascades/haarcascade_frontalface_default.xml')

cap = cv.VideoCapture("nvarguscamerasrc ! video/x-raw(memory:NVMM), width=(int)1920, height=(int)1080,format=(string)NV12, framerate=(fraction)30/1 ! nvvidconv ! video/x-raw, format=(string)BGRx ! videoconvert ! video/x-raw, format=(string)BGR ! appsink")

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # We don't use the color information, so might as well save space
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    # face detection and other logic goes here
    # gray here is the gray frame you will be getting from a camera

    # gray here is the gray frame you will be getting from a camera
    #gray = cv.cvtColor(gray, cv.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    for (x,y,w,h) in faces:
        cv.rectangle(gray,(x,y),(x+w,y+h),(255,0,0),2)
        roi_gray = gray[y:y+h, x:x+w]
        cv.imshow('frame',gray)
        rc,jpg = cv.imencode('.png', gray)
        msg = jpg.tobytes()
        #print ("mesage",msg)
        #client.publish("tx2/face", "im alive")
        client.publish("tx2/face",msg)
        #client.publish("tx2/face","Third time"+msg)
        #client.publish("tx2/face", cv.imencode('.png',gray)[1].tobytes())
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv.destroyAllWindows()
