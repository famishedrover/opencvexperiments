import cv2
import numpy as np
from matplotlib import pyplot as plt
import math

def plotImages(titles , images) :
	num = len(titles)
	for i in range(num) :
		plt.subplot(2,int(math.ceil(num/2.)),i+1),plt.imshow(images[i],'gray')
		plt.title(titles[i])
		plt.xticks([]),plt.yticks([])
	plt.show()


def plotImagesWithHist(titles , images) :
	num = len(titles)

	for i in range(0,num) :
		pp = i*2
		plt.subplot(num,2,pp+1),plt.imshow(images[i],'gray'),plt.title(titles[i]),plt.xticks([]),plt.yticks([])
		plt.subplot(num,2,pp+2),plt.hist(images[i].ravel(),256),plt.xticks([]),plt.yticks([])
	plt.show()


img = cv2.imread('img.jpg',0)

# img = cv2.imread('img1.jpg',0)
# img = cv2.medianBlur(img,5)



ret,th1 = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)

th2 = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY,11,2)

th3 = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,11,2)


ret4 , th4 = cv2.threshold(img , 0 , 255 , cv2.THRESH_BINARY + cv2.THRESH_OTSU)

ret,thresh1 = cv2.threshold(img,127,255,cv2.THRESH_BINARY)
ret,thresh2 = cv2.threshold(img,127,255,cv2.THRESH_BINARY_INV)
ret,thresh3 = cv2.threshold(img,127,255,cv2.THRESH_TRUNC)
ret,thresh4 = cv2.threshold(img,127,255,cv2.THRESH_TOZERO)
ret,thresh5 = cv2.threshold(img,127,255,cv2.THRESH_TOZERO_INV)


print int(math.ceil(10/2.))
titles = ['Original', 'Global', 'Adaptive Mean', 'Adaptive Gaussian' , 
			'Otsu' , 'Binary' ,'Binart_inv' ,'Trunc' , 'Tozero' , 'Tozero_inv',]
images = [img, th1, th2, th3 , th4 , thresh1 , thresh2 , thresh3 , thresh4 , thresh5]

plotImages(titles , images)
plotImagesWithHist(titles[:3] , images[:3])














