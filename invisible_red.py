import cv2
import numpy as np
import urllib.request
import time

url='http://192.168.43.1:8080/shot.jpg'

time.sleep(0.1)

background = 0

for i in range(20):
    background = urllib.request.urlopen(url)
    background = np.array(bytearray(background.read()), dtype=np.uint8)
    background = cv2.imdecode(background, -1)

background = cv2.resize(background , (400,400))
background = np.flip(background ,axis = 1)

while True:

    # Use urllib to get the image and convert into a cv2 usable format
    imgResp = urllib.request.urlopen(url)
    imgNp = np.array(bytearray(imgResp.read()),dtype=np.uint8)
    img = cv2.imdecode(imgNp,-1)

    img = cv2.resize(img,(400,400))
    img = np.flip(img , axis = 1)
    hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)

    lower_red = np.array([0,120,70])
    upper_red = np.array([20,255,255])
    mask1 = cv2.inRange(hsv , lower_red , upper_red)

    kernel = np.ones((3,3))
    mask_open = cv2.morphologyEx(mask1 , cv2.MORPH_OPEN , kernel,iterations=2)
    mask_close = cv2.morphologyEx(mask_open , cv2.MORPH_CLOSE , kernel ,iterations=2)
    mask_dilate = cv2.morphologyEx(mask_close , cv2.MORPH_DILATE , kernel,iterations=2)
    mask_dilate_not = cv2.bitwise_not(mask_dilate)

    mask_background = cv2.bitwise_and(background,background, mask = mask_dilate)
    mask_img = cv2.bitwise_and(img ,img, mask = mask_dilate_not)
    final_output = cv2.addWeighted(mask_img , 1 ,mask_background , 1 , 0)

    cv2.imshow('Mask_Dilate', mask_dilate)
    cv2.imshow('Original',img)
    cv2.imshow('Background' , background)
    cv2.imshow('Invisible' , final_output)
    #To give the processor some less stress
    time.sleep(0.1)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break