import cv2
import numpy as np

plate_cascade = cv2.CascadeClassifier('haarcascade_licence_plate_rus_16stages.xml')
# print plate_cascade
img = cv2.imread('russian.jpg')
gray = cv2.cvtColor(img , cv2.COLOR_BGR2GRAY)

plates = plate_cascade.detectMultiScale(gray , 2 , 100)
print plates
for (x,y,w,h) in plates:
    img = cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)


cv2.imshow('img' , img)
cv2.waitKey(0)
cv2.destroyAllWindows()