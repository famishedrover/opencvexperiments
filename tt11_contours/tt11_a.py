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



img = read_img('test2.jpg')
imgray = cv2.cvtColor(img , cv2.COLOR_BGR2GRAY) 
# thresh = cv2.adaptiveThreshold(imgray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,113,2)
_,thresh = cv2.threshold(imgray,100,255,cv2.THRESH_BINARY)
# print cv2.THRESH_BINARY  # is value 0
contours , hierarchy = cv2.findContours(thresh,1,2)
contours = sorted(contours,key=cv2.contourArea,reverse = True)
cnt = contours[5]

# CONTOUR APPLICATIONS / PARAMETERS.


# MOMENTS.
M = cv2.moments(cnt)
print M
print 'Cx = m10/m00 and Cy =m01/m00'

# AREA
area = cv2.contourArea(cnt)
print 'Area',area , M['m00']

# PERIMETER - True / false (closed /open)
perimeter =cv2.arcLength(cnt,True)
print 'perimeter',perimeter

# CONTOUR APPROXIMATION.
# epsilon is the max distance from contour to approx. contour
# DP = Douglas-Peucker Algo.
epsilon = 0.1*cv2.arcLength(cnt,True)
approx = cv2.approxPolyDP(cnt,epsilon,True)

# CONVEX HULL.
hull = cv2.convexHull(cnt)

# CHECKING CONVEXITY.
k=cv2.isContourConvex(cnt)

# BOUNDING RECTANGLE. (onty boundingRect in cv 2.x)
x,y,w,h = cv2.boundingRect(cnt)
cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)

# MINIMUM ENCLOSING CIRCLE
(x,y),radius = cv2.minEnclosingCircle(cnt)
center = (int(x),int(y))
radius = int(radius)
cv2.circle(img,center,radius,(0,255,0),2)

# FITTING AN ELLIPSE
ellipse = cv2.fitEllipse(cnt)
cv2.ellipse(img,ellipse,(0,255,255),2)

# # FITTING A LINE
# r,c = img.shape[:2]
# [vx,vy,x,y] = cv2.fitLine(cnt,cv2.cv.DIST_L2,0,0.01,0.01)
# lefty = int(-x*vy/vx + y)
# righty= int(((cols-x)*vy/vx)+y)
# cv2.line(img,(cols-1,righty),(0,lefty),(0,255,0),2)


cv2.imshow('img',img)
cv2.waitKey(0)
cv2.destroyAllWindows()



