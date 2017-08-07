import cv2 
import numpy as np

def nothing (x):
	pass


cap = cv2.VideoCapture(0)

cv2.namedWindow('image')
cv2.createTrackbar('minVal' , 'image' , 100,255 , nothing)
cv2.createTrackbar('maxVal' , 'image' , 200,255 , nothing)
font = cv2.FONT_HERSHEY_SIMPLEX
while(1):
	_,frame = cap.read()
	frame = cv2.cvtColor(frame , cv2.COLOR_BGR2GRAY)
	minVal = cv2.getTrackbarPos('minVal' , 'image')
	maxVal = cv2.getTrackbarPos('maxVal' , 'image')
	frame = cv2.Canny(frame , minVal , maxVal)
# cv2.putText(img,(txt),(int(w_width/4),int(w_height/4)), font, 1,((r+150)%256,(g+150)%256,(b+150)%256),2)
	txt = 'minVal :'+str(minVal) +' '+ 'maxVal :'+str(maxVal)
	cv2.putText(frame , txt , (int(frame.shape[0]/3) , int(frame.shape[1]/8) ) , font , 1 , (255,0,0) , 4)
	# print(frame.shape)

	cv2.imshow('Result' , frame)

	k = cv2.waitKey(100) & 0xFF
	if k == 27 :
		break
cv2.destroyAllWindows()
