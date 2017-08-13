import numpy as np
import cv2

image = cv2.imread('test2.jpg')
gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)

gradientx = cv2.Sobel(gray,ddepth = cv2.cv.CV_32F,dx=1,dy=0,ksize=-1)
gradienty = cv2.Sobel(gray,ddepth=cv2.cv.CV_32F,dx=0,dy=1,ksize=-1)

gradient = cv2.subtract(gradientx,gradienty)
gradient = cv2.convertScaleAbs(gradient)

blurred = cv2.blur(gradient,(9,9))
_,thresh = cv2.threshold(blurred , 225 , 255 , cv2.THRESH_BINARY)

kernel = cv2.getStructuringElement(cv2.MORPH_RECT , (21,7))
morph_close = cv2.morphologyEx(thresh , cv2.MORPH_CLOSE , kernel)

morph_close = cv2.erode(morph_close ,None , iterations = 4)
morph_close = cv2.dilate(morph_close , None , iterations = 8)
# morph_close = cv2.erode(morph_close,None,iterations = 4)

cnts,_ = cv2.findContours(morph_close.copy(),cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE )
c = sorted(cnts,key=cv2.contourArea,reverse =True)
c = c[0]

rect = cv2.minAreaRect(c)
box = np.int0(cv2.cv.BoxPoints(rect))
cv2.drawContours(image,[box],-1,(0,255,0),3)
cv2.imshow('image',image)
# cv2.imshow('morph_close',morph_close)
# cv2.imshow('thresh',thresh)
cv2.waitKey(0)
cv2.destroyAllWindows()