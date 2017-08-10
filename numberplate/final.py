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


def working(image):
	img = cv2.imread(image)
	original = img.copy()
	# print img
	img_gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
	# removing noise
	img_gray = cv2.bilateralFilter(img_gray,9,75,75)  
	equal_histogram = cv2.equalizeHist(img_gray)

	kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(5,5))
	morph_image = cv2.morphologyEx(equal_histogram,cv2.MORPH_OPEN,kernel,iterations=15)

	sub_morp_image = cv2.subtract(equal_histogram,morph_image)

	ret,thresh_image = cv2.threshold(sub_morp_image,0,255,cv2.THRESH_OTSU)
	canny_image = cv2.Canny(thresh_image,250,255)
	canny_image = cv2.convertScaleAbs(canny_image)

	kernel = np.ones((3,3), np.uint8)
	dilated_image = cv2.dilate(canny_image,kernel,iterations=1)

	contours, hierarchy = cv2.findContours(dilated_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	contours= sorted(contours, key = cv2.contourArea, reverse = True)[:10]
	screenCnt = None
	approx = None
	for c in contours:
		peri = cv2.arcLength(c, True)
		approx = cv2.approxPolyDP(c, 0.06 * peri, True) 
		if len(approx) == 4:  # Select the contour with 4 corners
  			screenCnt = approx
  			break

  	# cv2.drawContours(img, [screenCnt], 0, (0, 255, 0), 3)
  	mask = np.zeros(img_gray.shape , np.uint8)
  	new_image = cv2.drawContours(mask , [screenCnt] , 0 , 255 , -1)
  	new_image = cv2.bitwise_and(img, img , mask =mask)

  	y,cr,cb = cv2.split(cv2.cvtColor(new_image,cv2.COLOR_BGR2YCR_CB))
  	y = cv2.equalizeHist(y)
  	final_img = cv2.cvtColor(cv2.merge([y,cr,cb]),cv2.COLOR_YCR_CB2BGR)
  	
  	x,y,w,h = cv2.boundingRect(screenCnt)
	# cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)

	approx =rectify(screenCnt)
  	pts = np.float32([[0,0],[200,0],[200,50],[0,50]])
	M = cv2.getPerspectiveTransform(approx , pts)
	dst = cv2.warpPerspective(original,M,(200,50))

	# final = cv2.resize(dst , (200,50))




  	# cv2.imshow('final_img' , final_img)
  	# cv2.imshow('final___img',img)
  	cv2.imshow('final' , dst)



  	cv2.waitKey(0)
  	cv2.destroyAllWindows()


for i in range(1,7):
	working('./passed/test'+str(i)+'.jpg')

# working('russian.jpg')

