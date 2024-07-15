import cv2 as cv
# 全局变量cap
cap = cv.VideoCapture(0)

ret, frame = cap.read()
print(frame.shape)
cv.imwrite('1.jpg', frame)
# cap.set(6, cv.VideoWriter.fourcc('M', 'J', 'P', 'G'))
cap.set(cv.CAP_PROP_FOURCC, cv.VideoWriter_fourcc('M', 'J', 'P', 'G'))
cap.set(cv.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv.CAP_PROP_FRAME_HEIGHT, 480)
 
