import numpy as np
import cv2
def resize(image, width=None, height=None, inter=cv2.INTER_AREA):
    dim = None
    (h, w) = image.shape[:2]
    if width is None and height is None:
        return image
    if width is None:
        r = height / float(h)
        dim = (int(w * r), height)
    else:
        r = width / float(w)
        dim = (width, int(h * r))
    resized = cv2.resize(image, dim, interpolation=inter)
    return resized




def extract_digit_symbols(image ,charCnts,minW=5,minH=15):
	charIter = charCnts.__iter__()
	rois = []
	locs = []
	while True :
		try :
			c = next(charIter)
			(cX,cY,cW,cH) = cv2.boundingRect(c)
			roi = None
			if cW >= minW and cH >= minH :
				roi = image[cY:cY+cH , cX:cX+cW]
				rois.append(roi)
				locs.append((cX,cY,cX+cW,cY+cH))
			else :
				# special symbol found.
				# 3 parts are there in the special symbol.
				parts = [c,next(charIter),next(charIter)]
				(sXA,sYA,sXB,sYB) = (100,100,-100,-100)
				
				for p in parts:
					(pX,pY,pW,pH) = cv2.boundingRect(p)
					sXA = min(sXA,pX)
					sYB = min(sXB,pY)
					sXB = min(sXB,pX+pW)
					sYB = min(sYB,pY+pH)
				roi = image[sYA:sYB , sXA:sXB]
				rois.append(roi)
				locs.append((sXA,sYA,sXB,sYB))
		except StopIteration:
			break
	return (rois ,locs)

num = [str(x) for x in range(0,10)]
# alphabetsLower = [chr(x) for x in range(ord('a'),ord('z')+1)]
alphabetsUpper = [chr(x) for x in range(ord('A'),ord('Z')+1)]
charsNames = num+alphabetsUpper
# print charsNames

ref = cv2.imread('reference.png')
ref = cv2.cvtColor(ref,cv2.COLOR_BGR2GRAY)
ref = resize(ref ,width=400)
ref = cv2.threshold(ref,0,255,cv2.THRESH_BINARY_INV|cv2.THRESH_OTSU)[1]


refCnts = cv2.findContours(ref.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
refCnts = refCnts [0]
refCnts = sorted(refCnts ,key=cv2.contourArea)

# # normal method.
# clone = np.dstack([ref.copy()]*3)
# for c in refCnts :
# 	(x,y,w,h) = cv2.boundingRect(c)
# 	cv2.rectangle(clone , (x,y) , (x+w,y+h), (0,255,0),1)


# # better method.
# (refROIs,refLocs) = extract_digit_symbols(ref,refCnts,minW=4,minH=5)
# chars = {}
# clone = np.dstack([ref.copy()]*3)
# for (name,roi,loc) in zip(charsNames,refROIs,refLocs):
# 	(xA,yA,xB,yB) = loc 
# 	cv2.rectangle(clone,(xA,yA),(xB,yB),(0,255,0),1)
	
# 	print roi
# 	if len(roi) == 0 :
# 		continue
# 	roi = cv2.resize(roi,(36,36))
# 	chars[name] = roi
# 	# cv2.imshow('Char',roi)
# 	# cv2.waitKey(0)




refROIs,_ = extract_digit_symbols(ref,refCnts,minW=4,minH=5)
# for template matching algorithm.
chars = {}
for (name,roi) in zip(charsNames,refROIs) :
	roi = cv2.resize(roi,(36,36))
	chars[name] = roi
rectKernel = cv2.getStructuringElement(cv2.MORPH_RECT , (17,7))
output = []

image = cv2.imread('test1.png')
(h,w,) = image.shape[:2]
# hardcoded 0.2 i.e. expecting micr to lie in bottom 20% of image.
delta = int(h-(h*0.2))
bottom = image[delta:h,0:w]
gray_bottom = cv2.cvtColor(bottom,cv2.COLOR_BGR2GRAY)
blackhat = cv2.morphologyEx(gray_bottom,cv2.MORPH_BLACKHAT,rectKernel)
gradX = cv2.Sobel(blackhat,ddepth=cv2.CV_32F,dx=1,dy=0,ksize=-1)
gradX = np.absolute(gradX)
(minVal,maxVal) = (np.min(gradX),np.max(gradX))
gradX = (255*((gradX-minVal) - (maxVal - minVal)))
gradX = gradX.astype('uint8')
gradX = cv2.morphologyEx(gradX,cv2.MORPH_CLOSE,rectKernel)
thresh = cv2.threshold(gradX,0,255,cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
circularKernel =cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(19,2))

thresh = cv2.erode(thresh,rectKernel,iterations = 1)

thresh = cv2.dilate(thresh,circularKernel,iterations = 2)
rectKernel2 = cv2.getStructuringElement(cv2.MORPH_RECT,(5,2))

thresh = cv2.erode(thresh,rectKernel2,iterations=5)
thresh =cv2.dilate(thresh, rectKernel,iterations=1)

groupLocs = []
groupCnts = cv2.findContours(thresh.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
groupCnts = groupCnts[0]
for (i,c) in enumerate(groupCnts):
	(x,y,w,h) = cv2.boundingRect(c)
	# print 'dsaf'
	if w>80 and h>10:
		groupLocs.append((x,y,w,h))
		# cv2.rectangle(gray_bottom,(x,y),(x+w,y+h),(0,255,0),1)
groupLocs = sorted(groupLocs , key=lambda x:x[0])

print len(groupLocs)
for (gX,gY,gW,gH) in groupLocs :
	# groupOutput = []
	group = gray_bottom[gY-5:gY+gH+5 , gX-5:gX+gW+5]
	# print group
	
	group = cv2.threshold(group,0,255,cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
	cv2.imshow('group',group)
	cv2.waitKey(0)




ref = thresh


# cv2.imshow('gray_bottom',gray_bottom)
cv2.imshow('ref',ref)
# cv2.imshow('clone',clone)
cv2.waitKey(0)
cv2.destroyAllWindows()






