import numpy as np
import cv2
import tkinter as tk
from PIL import Image, ImageTk
import main
from roi_grip import ROIgrip
import imutils
import matplotlib
import multiprocessing
matplotlib.use("TkAgg")
from matplotlib.figure import Figure
import plotScript
'''
This file is part of the FollowMe's program and is protected by the CC BY-NC-ND 3.0 licence.
Written by Ofir Siboni in 2/2021

This file is taking care of the GUI of the 
'''
#Set up GUI
window = tk.Tk()  #Makes main window
window.wm_title("Object tracking")
window.config(background="#FFFFFF")

#Graphics window
imageFrame = tk.Frame(window, width=600, height=500)
imageFrame.grid(row=0, column=0)#, padx=10, pady=2)

#Capture video frames
lmain = tk.Label(imageFrame)
lmain.grid(row=0, column=0)
showImg = True
roiGRIP = ROIgrip()

def switchInput():
    global showImg
    showImg = not showImg

def selectRoi(f):
    r = cv2.selectROI(f)
    bbox = f[int(r[1]):int(r[1] + r[3]), int(r[0]):int(r[0] + r[2])] #Points in the frame
    resized = imutils.resize(bbox, width=900)
    roiGRIP.process(bbox)
    r = roiGRIP.filter_contours_output #list of contours
    r = sorted(r,key=lambda contour: -cv2.contourArea(contour)) # sorted list of contours(points)
    r = np.array(r)[[cv2.contourArea(c) > 10 for c in r]] #filer - only with area bigger than 10
    grains = [np.int0(cv2.boxPoints(cv2.minAreaRect(c))) for c in r]
    centroids = [(grain[2][1] - (grain[2][1] - grain[0][1]) // 2, grain[2][0] - (grain[2][0] - grain[0][0]) // 2) for
                 grain in grains]

    colors = [resized[centroid] for centroid in centroids]
    print(colors)

#buttons and other controlers
showImgBotton = tk.Button(window, text = "show img", command = switchInput)
showImgBotton.grid(row = 1,column = 0)
selectRoiButton = tk.Button(window, text = "select new object" , command = lambda : selectRoi(frame))
#selectRoiButton.grid(row = 1, column = 1) #TODO: fix change target function

#plotting stuff
''' TODO: FIX MEMORY OVEREATING
distanceData = []
timeData = []
f = Figure(figsize=(5,5), dpi=100)
a = f.add_subplot(111)
'''

def run():

    global frame,a
    data = main.show_frame(showImg)

    frame = data["image"]
    plotJob = multiprocessing.Process(target= plotScript.update, args=(data["distance"],data["time"])).start()
    print(plotJob)
    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    img = Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=img, master=window)
    lmain.imgtk = imgtk
    lmain.configure(image=imgtk)
    lmain.after(10, run)



run()
window.mainloop()
