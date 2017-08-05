path = './images/'
outpath = './output/'
import os
import cv2
import numpy as np

imgs = os.listdir(path)
final = []
for x in imgs :
	if ('.jpg' in x) or ('.png' in x) :
		final.append(x)
	else :
		pass
del imgs
# print final
imgs = final



print ('Number of Images Found:', len(imgs))
# assert len(imgs)>1 : 'Less than one Image Found!'

# outimg 
# fourcc = cv2.VideoWriter_fourcc(*'XVID')
frameRate = 10.0
transformRate = 0.1
output_size = (640,480)
outputfilename = 'output.mp4'

fourcc = cv2.cv.CV_FOURCC(*'XVID')
out = cv2.VideoWriter(outpath+outputfilename , fourcc , frameRate , output_size)

def read_img(img):
	img = cv2.imread(img)
	try:
		img = cv2.resize(img , output_size)
	except :
		# print 'at img',img
		pass
	return img

img1 = read_img(path+imgs[0])

for i in range(1,len(imgs)):
	img2 = read_img(path+imgs[i])
	percent = 1.0
	while(percent>=0.0) :
		temp = cv2.addWeighted(img1,percent,img2,1.0-percent,0)
		out.write(temp)
		percent -= transformRate
	img1 = img2


