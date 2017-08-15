# learn about cv2.findContours() and cv2.drawContours

# Contours can be explained simply as a curve joining all the
# continuous points (along the boundary),
# having same color or intensity.
def read_img(img) :
	img =cv2.imread(img)
	default_size_w,default_size_h=400,400
	if img is None :
		print 'Unable to read'
		exit()
	factor = int(img.shape[0]/default_size_w)
	default_size_h = int(img.shape[1]/factor)
	if img.shape[0]>default_size_w or img.shape[1] > default_size_h :
		img = cv2.resize(img ,(default_size_w,default_size_h))
	return img



import cv2
import numpy as np



img = read_img('test1.jpg')

imgray = cv2.cvtColor(img , cv2.COLOR_BGR2GRAY) 
# thresh = cv2.adaptiveThreshold(imgray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,113,2)
_,thresh = cv2.threshold(imgray,100,255,cv2.THRESH_BINARY)
# print cv2.THRESH_BINARY  # is value 0
contours , hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
cv2.drawContours(img,contours,-1,(0,255,0),3)

cv2.imshow('img',img)
# cv2.imshow('thresh',thresh)
# cv2.imshow('imgray',imgray)
cv2.waitKey(0)
cv2.destroyAllWindows()