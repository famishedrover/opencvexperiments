import cv2
import numpy as np

def nothing(x):
    pass


w_height=300
w_width =512
img = np.zeros((w_height,w_width,3), np.uint8)
cv2.namedWindow('image')


cv2.createTrackbar('R','image',0,255,nothing)
cv2.createTrackbar('G','image',0,255,nothing)
cv2.createTrackbar('B','image',0,255,nothing)


switch = '0 : OFF / 1 : ON'
cv2.createTrackbar(switch, 'image',1,1,nothing)
font = cv2.FONT_HERSHEY_SIMPLEX
r,g,b=0,0,0
while(1):
    txt = 'R:'+str(r)+' '+'G:'+str(g)+' '+'B:'+str(b)
    cv2.putText(img,(txt),(int(w_width/4),int(w_height/4)), font, 1,((r+150)%256,(g+150)%256,(b+150)%256),2)
    cv2.imshow('image',img)

    r = cv2.getTrackbarPos('R','image')
    g = cv2.getTrackbarPos('G','image')
    b = cv2.getTrackbarPos('B','image')
    s = cv2.getTrackbarPos(switch,'image')
    # print (r,g,b,s)

    if s == 0:
        img[:] = 0
        r = 0
        g = 0 
        b = 0
    else:
        img[:] = [b,g,r]

    k = cv2.waitKey(200) & 0xFF
    if k == 27:
        break
        
cv2.destroyAllWindows()