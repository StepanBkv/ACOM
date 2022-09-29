import cv2
import numpy as np
import math
from numba import njit 
import time
video = cv2.VideoCapture("img/video_4.mov", cv2.CAP_ANY)
ok, img = video.read()
old_frame_1 = img
w = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
h = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
fourcc = cv2.VideoWriter_fourcc(*'XVID')
video_writer = cv2.VideoWriter("img/output.mov", fourcc, 25, (w, h))
countr = 0
while (True):
	ok, img_2 = video.read()
	if ok == False:
		break
	frame_1 = img_2
	old_frame = cv2.GaussianBlur(cv2.cvtColor(old_frame_1, cv2.COLOR_BGR2GRAY), (11,11), 0)
	frame = cv2.GaussianBlur(cv2.cvtColor(frame_1, cv2.COLOR_BGR2GRAY), (11,11), 0)
	frame_diff = cv2.absdiff(frame, old_frame)
	rt,frame_diff = cv2.threshold(frame_diff, 15, 255, cv2.THRESH_BINARY)
	contours, hierarchy  = cv2.findContours(frame_diff, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	if contours != ():
		countr_now = cv2.contourArea(contours[0])
		if countr_now >= countr:
			video_writer.write(frame_1)
		countr = countr_now
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break
	old_frame_1 = frame_1.copy()
video.release()
video_writer.release()
cap = cv2.VideoCapture("img/output.mov",cv2.CAP_ANY)
while (True):
	ok, img = cap.read()
	if not ok:
		break
	time.sleep(0.04)
	cv2.imshow('img', img)
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break
cap.release()
cv2.destroyAllWindows()