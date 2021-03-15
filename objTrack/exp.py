import cv2

cap = cv2.VideoCapture(1)

cv2.imshow('cap', cap.read()[1])
cv2.waitKey(0)
