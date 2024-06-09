This project is a monitor and doorlock system.

The raspberry pi represent the door part. It collects footage from the camera, analyzes and transmits the videostream to the web page. 
Face detection is implemented in this side, boxing the detected faces. 
Once a human face is detected, it sends a signal through MQTT to the broad beside the monitor, indicating that someone is standing in front of the door.

On the monitor side, admin can see the video footage from the web page.
A button is put below the streaming window. Click the button, the status of the doorlock(in this case, we use the turn on or off of a light connected to 
the raspberry pi to simulate the doorlock status) would reverse.

# File descriptions
display folder is the flask app file.
    display.py is the main flask app execute file.
    the templates folder stores the html files.
    
display.service is the service setup file that regulates the path, pythonpath and execute start point and directory of the display service

default is the set up file for nginx



