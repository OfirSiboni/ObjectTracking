import cv2
import threading
from grip import GripPipeline

import plotScript as plt
focal_length = 960

grip = GripPipeline()
cap = cv2.VideoCapture(1)

# TRACKER INITIALIZATION
success ,frame = cap.read()
grip.process(frame)
img = grip.hsv_threshold_output
grip = GripPipeline()

def drawBox(img,bbox):

    """"draws a box around the bbox parameter on the img. in addition - adds the Width, Height and distance from the target(experimental)"""
    x, y, w, h = cv2.boundingRect(bbox)
    cv2.rectangle(img, (x, y), ((x + w), (y + h)), (255, 0, 255), 3, 3 )
    cv2.putText(img, "Tracking", (100, 75), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
    d = int(2.25*focal_length / h)
    cv2.putText(img, "w: " + str(w) + " h:" + str(h) + " d: " + str(d), (100,100),cv2.FONT_HERSHEY_SIMPLEX,0.7,(255, 255, 0), 2)
    return d

def show_frame(show_img = False):

    if show_img:
        return {"distance": 0, "time":0, "image" : cap.read()[1]} #if we are told to show only image - return the current frame.
    timer = cv2.getTickCount()
    success, img = cap.read() # get input
    grip.process(img) #proccess on grip file.
    bbox = grip.filter_contours_output # raw contours
    success = len(bbox) > 0
    bbox.sort(key=lambda contour: -cv2.contourArea(contour)) #sorted contours
    bbox = bbox[0] if success else [] #only the biggest.

    #img = grip.hsv_threshold_output
    d = 0
    if success:
        d = drawBox(img,bbox)
    else:
        cv2.putText(img, "Lost", (100, 75), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    cv2.putText(img, "Fps:", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,0,255), 2);
    cv2.putText(img, "Status:", (20, 75), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 255), 2);

    fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer);
    if fps>60: myColor = (20,230,20)
    elif fps>20: myColor = (230,20,20)
    else: myColor = (20,20,230)
    cv2.putText(img,str(int(fps)), (75, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, myColor, 2);

    #cv2.imshow("Tracking", img) #uncomment this line if there is no GUI
    return {"distance": d, "time":cv2.getTickCount() - timer, "image" : img}
