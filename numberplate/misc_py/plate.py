import cv2
import numpy as np

def rectify(h):
	h = h.reshape((4,2))
	print h
	hnew = np.zeros((4,2),dtype = np.float32)
	add = h.sum(1)
	# print add
	hnew[0] = h[np.argmin(add)]
	hnew[2] = h[np.argmax(add)]
	diff = np.diff(h,axis = 1) 
	hnew[1] = h[np.argmin(diff)]
	hnew[3] = h[np.argmax(diff)]
	return hnew



def get_numberplate(image):

	kernel = cv2.getStructuringElement(cv2.MORPH_RECT , (5,5))
	img = cv2.imread(image)

	imgray = cv2.cvtColor(img , cv2.COLOR_BGR2GRAY)
	# imgray = cv2.GaussianBlur(imgray , (5,5) , 0)
	
	imgray = cv2.bilateralFilter(imgray , 9 , 75 , 75)
	eql = cv2.equalizeHist(imgray)
	# edge = cv2.Canny(imgray , 200 ,200)
	morphed_open = cv2.morphologyEx(eql , cv2.MORPH_OPEN , kernel , iterations = 15)
	sub_img = cv2.subtract(eql,morphed_open)
	ret,thresh = cv2.threshold(sub_img,0,255,cv2.THRESH_OTSU)
	edge = cv2.Canny(thresh , 250 ,255)

	kernel = np.ones((3,3),np.uint8)
	dilated = cv2.dilate(edge,kernel , iterations =1)
	# morphed_close = cv2.morphologyEx(threshold , cv2.MORPH_CLOSE , kernel)
	# morphed_open = cv2.morphologyEx(morphed_close , cv2.MORPH_OPEN , kernel)

	# edged = cv2.dilate(morphed_open , kernel , iterations = 1)
	contours , hierarchy = cv2.findContours(dilated.copy() , cv2.RETR_TREE  ,cv2.CHAIN_APPROX_SIMPLE)
	print len(contours)
	contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]
	
	counter = 0
	screen = None
	for cnt in contours :
		epsilon = 0.06*cv2.arcLength(cnt,True)
		approx = cv2.approxPolyDP(cnt,epsilon,True)
		# print approx
		if len(approx) == 4 :
			screen = approx
			
			# approx = rectify(approx)
			# print approx.shape
			cv2.drawContours(img , [screen] , -1 , (0,255,0) , 1)
		
			# x,y,w,h = cv2.boundingRect(approx)
			# cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
			
		# if counter == 5:
		# 	break


	cv2.imshow('result' , img)

	
	# cv2.imshow('original' , img)
	cv2.waitKey(0)
	cv2.destroyAllWindows()




for i in range(1,6):
	get_numberplate('test'+str(i)+'.jpg')