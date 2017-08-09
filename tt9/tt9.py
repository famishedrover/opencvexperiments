import cv2
import numpy as np
# from matplotlib import pyplot as plt

A = cv2.imread('one.png')
B = cv2.imread('two.png')
# A = A[:,:400,:]
# B = B[:472,:,:]
# print(A.shape , B.shape)

A = cv2.resize(A,(512,512))
B = cv2.resize(B,(512,512))
print(A.shape,B.shape)

def gaussian_pyr(img , layers):
	g = img.copy()
	# print ('image shape',g.shape)
	gpa = [g]
	for i in range(layers) :
		g = cv2.pyrDown(g)
		gpa.append(g)
	return gpa

def laplacian_pyr(gaussian):
	# print len(gaussian)
	length = len(gaussian)
	# last layer in the laplacian.
	lpa = [gaussian[length-2]]
	for i in range(length-2,0,-1) :
		GE = cv2.pyrUp(gaussian[i])
		# print(GE.shape , gaussian[i-1].shape)
		L = cv2.subtract(gaussian[i-1] , GE)

		lpa.append(L)
	return lpa

def get_pyramid_mixed_image(A,B,n_layers):
	n_layers = 7
	ga = gaussian_pyr(A , n_layers)
	gb = gaussian_pyr(B, n_layers)
	# for i in ga :
	# 	print i.shape
	la = laplacian_pyr(ga)
	lb = laplacian_pyr(gb)
	# add halves at each level.
	LS = []
	for lxa , lxb in zip(la,lb):
		rows , cols , dpt = lxa.shape
		ls = np.hstack((lxa[:,0:cols/2],lxb[:,cols/2:]))
		LS.append(ls)
	# reconstructing image.
	lss = LS[0]
	for i in range(1,n_layers) :
		lss = cv2.pyrUp(lss)
		lss = cv2.add(lss , LS[i])
	return lss


lss = get_pyramid_mixed_image(A,B,n_layers)

# for comparison , directly connecting the two halves.
real = np.hstack((A[:,:cols/2],B[:,cols/2:]))

cv2.imshow('Pyramid',lss)
cv2.imshow('Raw addition',real)
cv2.waitKey(0)
cv2.destroyAllWindows()









