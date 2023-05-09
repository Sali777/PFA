import numpy as np
import Handmodule as hm
import cv2 as cv
import time
import autopy as atp
import VirtualKeyboard
import  math
# import SoundControle
def main () :
    ptime=0
    detector=hm.HandDetect()
    cap=cv.VideoCapture(0)
    wait=2
    tim=0
    while 1 :
        ctime=time.time()
        fps=int(1/(ctime-ptime))
        ptime=ctime # frame/s
        succ,img=cap.read()
        # img=cv.flip(img,1)
        hand,hand1,lmls1,lmls2=detector.findHands(img)
        if len(lmls1)!=0 :
           [x_1, y_1] = lmls1[12][1:]
           [x_2, y_2] = lmls1[8][1:]
           x_m = int((x_1 + x_2) / 2)
           y_m = (y_1 + y_2) // 2
           cv.line(img, (x_1, y_1), (x_2, y_2), (0, 255, 0), 2)
           cv.circle(img, (x_1, y_1), 10, (152,245,255), -1)
           cv.circle(img, (x_2, y_2), 10, (152,245,255), -1)
           cv.circle(img, (x_m, y_m), 10, (152,245,255), -1)
           if (hand==[0,1,0,0,0]):
               xmouse, ymouse = abs(int(((x_2 / 540) * 1000) + 130)), abs(int((y_2 / 170) * 300 + 10))

               atp.mouse.move(xmouse,ymouse)


           elif  hand==[0,1,1,0,0] :
                tim+=1
                if tim==wait:
                    cv.circle(img, (x_m, y_m), 20, (152,245,255), -1)
                    tim=0
                atp.mouse.click();print('left click')
        cv.putText(img,str(fps),(50,70),cv.FONT_HERSHEY_PLAIN,2,(0,0,255),2)
        cv.imshow('AI mouse',img)
        if hand==[0,1,1,1,1] :
            VirtualKeyboard.main()
        cv.waitKey(1)
main()