import cv2
import numpy as np
from matplotlib import pyplot as plt

BLUE_BGR = [255,0,0]
img1 = cv2.imread('opencv_logo.png')

# img1[img1[:,: ,0] == 255] = 0
# img1[img1[:,: ,2] == 255] = 0
# img1[img1[:,: ,1] == 255] = 0


img1 = cv2.cvtColor(img1 , cv2.COLOR_RGB2BGR)
BLUE_RGB = [BLUE_BGR[2] , BLUE_BGR[1] , BLUE_BGR[0]]

replicate 	= cv2.copyMakeBorder(img1,100,100,100,100,cv2.BORDER_REPLICATE 			)
reflect 	= cv2.copyMakeBorder(img1,100,100,100,100,cv2.BORDER_REFLECT 			)
reflect101 	= cv2.copyMakeBorder(img1,100,100,100,100,cv2.BORDER_REFLECT_101		)
wrap 		= cv2.copyMakeBorder(img1,100,100,100,100,cv2.BORDER_WRAP				)
constant 	= cv2.copyMakeBorder(img1,100,100,100,100,cv2.BORDER_CONSTANT,value=BLUE_RGB)

# replicate 	= cv2.cvtColor(replicate 	,cv2.COLOR_RGB2BGR)
# reflect 	= cv2.cvtColor(reflect 		,cv2.COLOR_RGB2BGR)
# reflect101 	= cv2.cvtColor(reflect101 	,cv2.COLOR_RGB2BGR)
# wrap 		= cv2.cvtColor(wrap 		,cv2.COLOR_RGB2BGR)
# constant 	= cv2.cvtColor(constant 	,cv2.COLOR_RGB2BGR)

plt.subplot(231),plt.imshow(img1,'gray')		,plt.title('ORIGINAL')		,plt.axis('off')
plt.subplot(232),plt.imshow(replicate,'gray')	,plt.title('REPLICATE')		,plt.axis('off')
plt.subplot(233),plt.imshow(reflect,'gray')		,plt.title('REFLECT')		,plt.axis('off')
plt.subplot(234),plt.imshow(reflect101,'gray')	,plt.title('REFLECT_101')	,plt.axis('off')
plt.subplot(235),plt.imshow(wrap,'gray')		,plt.title('WRAP')			,plt.axis('off')
plt.subplot(236),plt.imshow(constant,'gray')	,plt.title('CONSTANT')		,plt.axis('off')

plt.show()