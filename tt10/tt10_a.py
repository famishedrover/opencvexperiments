import cv2
import numpy as np

cap = cv2.VideoCapture(0)
def get_hsv_bounds(color_list) :
	color = np.uint8([[color_list]])
	hsv_color = cv2.cvtColor(color , cv2.COLOR_BGR2HSV)
	c_hsv = hsv_color[0][0][0]
	return (np.array([c_hsv-10 , 100 ,100]),np.array([c_hsv+10 , 255 ,255]))
def nothing (x):
	pass



kernel = np.ones((5,5) , np.uint8)


kernel = cv2.getStructuringElement(cv2.MORPH_RECT , (5,5))
print ('MORPH_RECT\n',kernel)
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE , (5,5))
print ('MORPH_ELLIPSE\n',kernel)
kernel =cv2.getStructuringElement(cv2.MORPH_CROSS , (5,5))
print ('MORPH_CROSS\n',kernel)


# DEFAULT_BGR_VALUES
B,G,R = 255,0,0
sample_color = np.ones((100,100,3),np.uint8)
cv2.namedWindow('Trackbar')
cv2.createTrackbar('B' , 'Trackbar' , B, 255 , nothing)
cv2.createTrackbar('G' , 'Trackbar' , G, 255 , nothing)
cv2.createTrackbar('R' , 'Trackbar' , R, 255 , nothing)

font = cv2.FONT_HERSHEY_SIMPLEX

while (1) :
	B = cv2.getTrackbarPos('B' , 'Trackbar')
	G = cv2.getTrackbarPos('G' , 'Trackbar')
	R = cv2.getTrackbarPos('R' , 'Trackbar')
	color = [B,G,R]
	sample_color[:,:,:] = color

	ret,frame = cap.read()
	w_width , w_height = frame.shape[0],frame.shape[1]

	hsv = cv2.cvtColor(frame , cv2.COLOR_BGR2HSV)
	low , high = get_hsv_bounds(color)
	mask = cv2.inRange(hsv , low , high)


	opening  = cv2.morphologyEx(mask , cv2.MORPH_OPEN , kernel)
	closing = cv2.morphologyEx(mask, cv2.MORPH_CLOSE , kernel)
# input - opening(input)
	tophat = cv2.morphologyEx(mask , cv2.MORPH_TOPHAT , kernel)
	# input - closing(input)
	blackhat = cv2.morphologyEx(mask , cv2.MORPH_BLACKHAT , kernel)
	# dilation - erosion
	gradient = cv2.morphologyEx(mask , cv2.MORPH_GRADIENT , kernel)

	result = cv2.bitwise_and(frame , frame , mask = blackhat)


	cv2.imshow('Trackbar' , sample_color)
	cv2.imshow('gradient' , gradient)
	txt = 'R:'+str(R)+' '+'G:'+str(G)+' '+'B:'+str(B)
	cv2.putText(result,(txt),(int(w_width/4),int(w_height/4)), font, 1,((R+150)%256,(G+150)%256,(B+150)%256),2)
	cv2.imshow('result' , result)

	k = cv2.waitKey(500) & 0xFF
	if k == 27 :
		break
cv2.destroyAllWindows()
