import cv2 as cv
import time
import autopy as atp
import numpy as np
import mediapipe as mp
from math import sqrt #distance maybe
from numpy import angle #

class HandDetect():
    def __init__(self,mode=False,max_hands=2,detection_confidence=0.5,track_confidence=0.5):
        self.mode=mode
        self.max_hands=max_hands
        self.detection_confidence=detection_confidence
        self.track_confidence=track_confidence
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands()
        self.mpDraw = mp.solutions.drawing_utils#meme variable que la classe handmodule
    def findHands(self,img,draw=True):
            h, w, c = img.shape
            x_1, y_1, x_2, y_2=None,None,None,None
            distance=50
            imgRGB = cv.cvtColor(img, cv.COLOR_BGRA2RGB)
            results = self.hands.process(imgRGB)
            if draw:
                if results.multi_hand_landmarks:
                        for hanLms in results.multi_hand_landmarks:
                            for id, lm in enumerate(hanLms.landmark):
                                cx, cy = int(lm.x * w), int(lm.y * h)
                                cv.circle(img,(cx,cy),10,(0,0,255),-1)
                            self.mpDraw.draw_landmarks(img,landmark_list=hanLms,connections=self.mpHands.HAND_CONNECTIONS)
                            lx = [int(hanLms.landmark[i].x * w) for i in range(len(hanLms.landmark))]
                            ly = [int(hanLms.landmark[i].y * h) for i in range(len(hanLms.landmark))]
                            x1 = min(lx)
                            y1 = min(ly)
                            x2 = max(lx)
                            y2 = max(ly)
                            cv.rectangle(img, (x1-20, y1-20), (x2+20, y2+20), (0, 255, 0), thickness=1)
                            x_1 = int(hanLms.landmark[12].x * w) #position de le middle finger
                            y_1 = int(hanLms.landmark[12].y * h)
                            x_2 = int(hanLms.landmark[8].x * w) #position de  chhada finger
                            y_2 = int(hanLms.landmark[8].y * h)
                            x_m = int((x_1 + x_2) / 2)
                            y_m = (y_1 + y_2) // 2
                            cv.line(img, (x_1, y_1), (x_2, y_2), (0, 255, 0), 2) # partie color de la main
                            cv.line(img,(int(hanLms.landmark[4].x * w),int(hanLms.landmark[4].y * h)),(int(hanLms.landmark[3].x * w),int(hanLms.landmark[3].y * h)),(0, 255, 0), 2)
                            cv.line(img, (int(hanLms.landmark[3].x * w), int(hanLms.landmark[3].y * h)),
                                    (int(hanLms.landmark[0].x * w), int(hanLms.landmark[0].y * h)), (0, 255, 0), 2) # les lignes qui relient les les cercle remarquable
                            cv.circle(img, (x_1, y_1), 10, (

                            ), -1)
                            cv.circle(img, (x_2, y_2), 10, (152,245,255), -1)
                            cv.circle(img, (x_m, y_m), 10, (152,245,255), -1)
                            distance = int(sqrt((x_1 - x_2) ** 2 + (y_1 - y_2) ** 2)) #distance variable qui suit le mouvement de ces deux doight  remarquable
                            # atp.mouse.move(x_1,y_1)
            return distance,x_1,y_1,x_2,y_2
    def detectFind(self,img,hand=1):
        h, w, c = img.shape
        lmls=[]
        imgRGB = cv.cvtColor(img, cv.COLOR_BGRA2RGB)
        results=self.hands.process(imgRGB)
        if results.multi_hand_landmarks:
            hanlms=results.multi_hand_landmarks[hand-1]
            for id, lm in enumerate(hanlms.landmark):
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmls.append([id,cx,cy])
        return lmls
    def fingersUP(self,img):
        h,w,c=img.shape
        l=[0,0,0,0,0]
        lmls=self.detectFind(img)
        hand={1:[1,2,3,4],2:[5,6,7,8],3:[9,10,11,12],4:[13,14,15,16],5:[17,18,19,20]}
        if len(lmls)!=0 :
            for m in hand.keys():
                if lmls[hand[m][3]][2]==min([lmls[k][2] for k in hand[m]]):
                    l[m-1]=1

            x1=lmls[0][1]
            x2=lmls[3][1]
            x3=lmls[4][1]
            y1=lmls[0][2]
            y2=lmls[3][2]
            y3=lmls[4][2]
            z1=complex((x3-x2),(y3-y2))
            z2=complex((x2-x1),(y2-y1))
            a=-angle(z2/z1,True)
            cv.putText(img,str(a),(100,100),cv.FONT_HERSHEY_PLAIN,1,(0,0,0),1)
            if abs(a) >10 :
                l[0]=0


        return l
#meme demarche pour le mouse controlle pour etre plus libre


# def main():
#     ctime = 0
#     ptime = 0
#     cap = cv.VideoCapture(0)
#     detector=HandDetect()
#     while True:
#         succ, img = cap.read()
#         img=cv.flip(img,1)
#         detector.findHands(img,True,1)
#         lmls=detector.detectFind(img,1)
#         if len(lmls)!=0 :
#             print('id={} , x={} , y={} '.format(lmls[4][0],lmls[4][1],lmls[4][2]))
#         ctime = time.time()
#         fps = 1 / (ctime - ptime)
#         ptime = ctime
#         cv.putText(img, str(int(fps)), (70, 50), cv.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), 2)
#         cv.imshow('cap', img)
#         cv.waitKey(1)
#
# main()
print('hello')
# vraiment ce code est !!!! repitition de principe  le chose supplementaire c'est le distanceen peu tutiliser cette condition pour ameliorer la detection  dees le pointage