import cv2
import threading
from grip import GripPipeline
import plotScript as plt

'''
This file is part of the FollowMe's program and is protected by the CC BY-NC-ND 3.0 licence.
Written by Ofir Siboni in 2/2021
'''

FOCAL_LENGTH = 960
CM_HEIGHT = 2.25

grip = GripPipeline()
cap = cv2.VideoCapture(1)

# TRACKER INITIALIZATION
success ,frame = cap.read()
grip.process(frame)
img = grip.hsv_threshold_output
grip = GripPipeline()

def drawBox(img,bbox,console):

    """"draws a box around the bbox parameter on the img. in addition - adds the Width, Height and distance from the target"""
    x, y, w, h = cv2.boundingRect(bbox)
    cv2.rectangle(img, (x, y), ((x + w), (y + h)), (255, 0, 255), 3, 3 )
    
    d = int(CM_HEIGHT*FOCAL_LENGTH / h) #IMPORTANT: calculates the distance from the target, using the following formula: d * h = cm * f
    if console:
        cv2.putText(img, "w: " + str(w) + " h:" + str(h) + " d: " + str(d), (100,100),cv2.FONT_HERSHEY_SIMPLEX,0.7,(255, 255, 0), 2)
        cv2.putText(img, "Tracking", (100, 75), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
    return {x,y,d,h}
'''
return format:
    if console is true -> {x,y,d,h}
    else -> {d,img}
'''
def show_frame(show_img = False, console = True):

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
    boxData = None
    d = 0
    if success:
        boxData = drawBox(img,bbox,console)
        return boxData
    else:
        if console:
            return {0,0,0,0}
        else:
            cv2.putText(img, "Lost", (100, 75), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    if not console:
        cv2.putText(img, "Fps:", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,0,255), 2);
        cv2.putText(img, "Status:", (20, 75), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 255), 2);
    
    #changing the color of the FPS 
    fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer);
    if not console:
        if fps>60: FPScolor = (20,230,20)
        elif fps>20: FPScolor = (230,20,20)
        else: FPScolor = (20,20,230)
        cv2.putText(img,str(int(fps)), (75, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, FPScolor, 2);

    #cv2.imshow("Tracking", img) #uncomment this line if there is no GUI
    return {"distance": d, "time":cv2.getTickCount() - timer, "image" : img}
