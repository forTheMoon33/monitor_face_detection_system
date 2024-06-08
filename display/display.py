#!/usr/bin/env python3
import RPi.GPIO as GPIO
from flask import Flask,render_template, Response, request, redirect
import cv2
import time
from time import sleep

import paho.mqtt.client as mqtt

app = Flask(__name__)

# GPIO initialization
GPIO.setmode(GPIO.BCM)


GPIO.setup(23, GPIO.OUT)
GPIO.output(23, GPIO.LOW)

# MQTT initialization

client = mqtt.Client()
#client.on_connect = on_connect
              
broker_ip = "10.16.230.161"
client.username_pw_set("iotstudent","coen")
client.connect(broker_ip,1883,60)

# If the swith state should be changed.
#face_showed = 0
#face_before = 2

# the directory of the xml file to set up the classifier
face_cascade = cv2.CascadeClassifier('/home/waterbottle/test/haarcascade_frontalface_default.xml')

# Deal with the footage
def generate_frames():
    #open the camera
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Couldn't open the camera.")
        exit()
    
    # If the swith state should be changed.
    face_showed = 0
    face_before = 2

    while True:
        # Sample
        ret,frame = cap.read()
        if not ret:
            print("Unable to sample")
            break

        # Transform into gray-range
        gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        

        faces = face_cascade.detectMultiScale(gray,scaleFactor=1.1,minNeighbors=5,minSize=(30,30))
        
        # If no human face is detected, set face_showed to 0.
        if len(faces)==0:
            face_showed=0
        else:
            face_showed=1

        # If detection state is not the same, need to send a new command to the cyper board.
        if face_showed!=face_before:
            client.reconnect()

            if face_showed==1:
                client.publish('light/led1',payload="LIGHT ON-")
            if face_showed==0:
                client.publish('light/led1',payload="LIGHT OFF-")

        face_before = face_showed
        

        for(x,y,w,h) in faces:
            #client.publish('light/led1',payload="LIGHT ON-")

            cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
            #print(f"face detected,x={x},y={y},w={w},h={h}")

        r,buffer = cv2.imencode('.jpg',frame)

        rp = buffer.tobytes()
        yield (b'--frame\r\n' b'Content-Type: image/jpg\r\n\r\n' + rp + b'\r\n')
        
        sleep(0.1)

        if cv2.waitKey(1)&0xFF == ord('q'):
            break

@app.route('/')
def home():

    return render_template('index.html')



@app.route('/doorlock/')
def open_door():
    pin_state = GPIO.input(23)
    if pin_state == GPIO.HIGH:
        GPIO.output(23,GPIO.LOW)
    else:
        GPIO.output(23,GPIO.HIGH)
    
    return redirect('/')



@app.route('/video/')
def video_feed():
    return Response(generate_frames(),mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000)
