import cv2
# ok, img = cap.read()
# w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
# h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
# fourcc = cv2.VideoWriter_fourcc(*'XVID')
# video_writer = cv2.VideoWriter("output_1.mov", fourcc, 25, (w,h))
cap = cv2.VideoCapture(1)
while True:
    ret, frame = cap.read()
    # video_writer.write(frame)
    if not ret:
        break
    if cv2.waitKey(1) & 0xff == 27:
        break
    cv2.imshow('frame', frame)
cap.release()
cv2.destroyAllWindows()