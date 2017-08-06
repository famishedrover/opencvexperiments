import cv2
import numpy as np

# requires webcam
def get_hsv_bounds(color_list) :
	color = np.uint8([[color_list]])
	hsv_color = cv2.cvtColor(color , cv2.COLOR_BGR2HSV)
	c_hsv = hsv_color[0][0][0]
	return (np.array([c_hsv-10 , 100 ,100]),np.array([c_hsv+10 , 255 ,255]))

# BGR
green = [0,255,0]
red = [0,0,255]
blue = [255,0,0]

# low , high  = get_hsv_bounds([0,255,0])
# print low
# print high

cap = cv2.VideoCapture(0)


while(1) :
	_,frame = cap.read()
	# frame = cv2.GaussianBlur(frame,(5,5),0)

	hsv = cv2.cvtColor(frame , cv2.COLOR_BGR2HSV)

	low_red , high_red = get_hsv_bounds(red)
	low_green , high_green = get_hsv_bounds(green)
	low_blue , high_blue = get_hsv_bounds(blue)

	mask_blue = cv2.inRange(hsv , low_blue , high_blue)
	mask_red = cv2.inRange(hsv , low_red , high_red)
	mask_green = cv2.inRange(hsv , low_green , high_green)



	res_blue = cv2.bitwise_and(frame,frame , mask=mask_blue)
	res_green = cv2.bitwise_and(frame , frame , mask = mask_green)
	res_red = cv2.bitwise_and(frame , frame , mask = mask_red)

	res = cv2.add(res_blue , res_green)
	res = cv2.add(res, res_red)



	cv2.imshow('Result',res)
	cv2.imshow('Blue' , res_blue)
	cv2.imshow('Green' , res_green)
	cv2.imshow('Red' , res_red)

	k=cv2.waitKey(5) & 0xFF
	if k==27 :
		break
cv2.destroyAllWindows()

