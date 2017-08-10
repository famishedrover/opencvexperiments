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




kernel = np.ones((3,3) , np.uint8)

sample_color = np.ones((100,100,3),np.uint8)

# print sample_color
B,G,R = 255,0,0
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
	# gray = cv2.cvtColor(frame , cv2.COLOR_BGR2GRAY)

	hsv = cv2.cvtColor(frame , cv2.COLOR_BGR2HSV)
	low , high = get_hsv_bounds(color)
	mask = cv2.inRange(hsv , low , high)


	# # frame = cv2.GaussianBlur(frame , (5,5) , 0)
	# med = np.mean(frame)
	# # edge = cv2.Canny(frame , med-100, med+100)
	# edge = cv2.Canny(edge , 50 , 200)
	
	
	erosion = cv2.erode(mask , kernel , iterations = 1)
	dilation = cv2.dilate(erosion , kernel , iterations=1)

	result = cv2.bitwise_and(frame , frame , mask = dilation)
	# cv2.imshow('edge' , edge)
	# # cv2.imshow('erosion' , erosion)
	# cv2.imshow('Opening' , dilation)
	# # cv2.imshow('edge' , edge)
	cv2.imshow('Trackbar' , sample_color)
	# cv2.imshow('mask' , mask)
	# cv2.imshow('erosion',erosion)
	# cv2.imshow('original' , frame)
	txt = 'R:'+str(R)+' '+'G:'+str(G)+' '+'B:'+str(B)
	cv2.putText(result,(txt),(int(w_width/4),int(w_height/4)), font, 1,((R+150)%256,(G+150)%256,(B+150)%256),2)
	cv2.imshow('result' , result)

	k = cv2.waitKey(500) & 0xFF
	if k == 27 :
		break
cv2.destroyAllWindows()
