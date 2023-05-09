import numpy as np
import mouseHM as hm
import cv2 as cv
import time
import autopy as atp
#import SoundControle

ptime=0
detector=hm.HandDetect()
cap=cv.VideoCapture(0)
while 1 :
    ctime=time.time()
    fps=int(1/(ctime-ptime))
    ptime=ctime
    succ,img=cap.read()
    img=cv.flip(img,1)
    hand=detector.fingersUP(img)
    distance,x_1,y_1,x_2,y_2=detector.findHands(img)
    if (x_1,y_1)!= (None,None) and (hand==[0,1,0,0,0]):
        xmouse, ymouse = abs(int(((x_2 / 540) * 1000) + 130)), abs(int((y_2 / 170) * 300 + 10))
        atp.mouse.move(xmouse,ymouse)


    if  hand==[0,1,1,0,0] :
        atp.mouse.click();print('left click')
    cv.putText(img,str(fps),(50,70),cv.FONT_HERSHEY_PLAIN,2,(0,0,255),2)

    cv.imshow('AI mouse',img)
    if hand==[0,1,0,0,1]  :
        print('volume controle------') #cecode est probablement pour controller le

        break
    cv.waitKey(1)
