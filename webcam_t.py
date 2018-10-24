import cv2
import time


video = cv2.VideoCapture(0)

check, frame = video.read()

cv2.imshow("Capturing", frame)

cv2.imwrite('/home/biot/Pictures/newfilename.png', frame)

cv2.waitKey(2000)

video.release()

