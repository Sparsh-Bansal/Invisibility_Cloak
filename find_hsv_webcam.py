import cv2
import numpy as np
import time

url='http://25.75.207.5:8080/shot.jpg'

time.sleep(0.1)
background = 0

def nothing():
    pass

cv2.namedWindow('CHECK')
cv2.createTrackbar('H_lower', 'CHECK', 0, 180, nothing)
cv2.createTrackbar('S_lower', 'CHECK', 0, 255, nothing)
cv2.createTrackbar('V_lower', 'CHECK', 0, 255, nothing)
cv2.createTrackbar('H_upper', 'CHECK', 0, 180, nothing)
cv2.createTrackbar('S_upper', 'CHECK', 0, 255, nothing)
cv2.createTrackbar('V_upper', 'CHECK', 0, 255, nothing)
# print('Create')
cap = cv2.VideoCapture(0)

for i in range(20):
    ret , background = cap.read()

background = cv2.resize(background , (400,400))
background = np.flip(background ,axis = 1)
# print('Baackground')

while True:

    ret2 , img = cap.read()

    # print('1')

    h_value_l = cv2.getTrackbarPos('H_lower','CHECK')
    s_value_l = cv2.getTrackbarPos('S_lower','CHECK')
    v_value_l = cv2.getTrackbarPos('V_lower','CHECK')
    h_value_u = cv2.getTrackbarPos('H_upper','CHECK')
    s_value_u = cv2.getTrackbarPos('S_upper','CHECK')
    v_value_u = cv2.getTrackbarPos('V_upper','CHECK')

    # print('2')
    img = cv2.resize(img,(400,400))
    img = np.flip(img , axis = 1)
    hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)

    lower_red = np.array([h_value_l , s_value_l , v_value_l ])
    upper_red = np.array([h_value_u , s_value_u , v_value_u ])
    mask1 = cv2.inRange(hsv , lower_red , upper_red)

    kernel = np.ones((3,3))
    mask_open = cv2.morphologyEx(mask1 , cv2.MORPH_OPEN , kernel,iterations=2)
    mask_close = cv2.morphologyEx(mask_open , cv2.MORPH_CLOSE , kernel ,iterations=2)
    mask_dilate = cv2.morphologyEx(mask_close , cv2.MORPH_DILATE , kernel,iterations=2)

    mask_dilate_not = cv2.bitwise_not(mask_dilate)
    mask_background = cv2.bitwise_and(background,background, mask = mask_dilate)
    mask_img = cv2.bitwise_and(img ,img, mask = mask_dilate_not)
    final_output = cv2.addWeighted(mask_img , 1 ,mask_background , 1 , 0)
    # print('2')

    check = cv2.resize(img , (800,400))

    cv2.imshow('CHECK' , check)
    cv2.imshow('Mask1' , mask1)
    cv2.imshow('Mask2' , mask_dilate)
    cv2.imshow('Check_invisibility' , final_output)

    time.sleep(0.1)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break