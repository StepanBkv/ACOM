import cv2
cap = cv2.VideoCapture("img/output.mov")
while (True):
	ok, img = cap.read()
	if not ok:
		break
	cv2.imshow('img', img)
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break
cap.release()
cv2.destroyAllWindows()