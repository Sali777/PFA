import cv2 as cv
import time
import autopy as atp
import numpy as np
import mediapipe as mp
from numpy import angle

class HandDetect(): # nous avons reecrire un modele existe deja maybe version
    def __init__(self,mode=False,max_hands=2,detection_confidence=0.5,track_confidence=0.5):
        self.mode=mode
        self.max_hands=max_hands
        self.detection_confidence=detection_confidence
        self.track_confidence=track_confidence
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands()
        self.mpDraw = mp.solutions.drawing_utils
    def findHands(self,img,draw=True):
            h, w, c = img.shape # return 3 value (toul,3ordh , ..)
            l=[0,0,0,0,0] #liste de  5 elements initialiser a 0
            l1= [0, 0, 0, 0, 0]
            distance=250 #distance de quoi LE D
            lmls1 = [] #liste vide pour main1
            lmls2=[]#liste vide pour main 2
            i=0
            imgRGB = cv.cvtColor(img, cv.COLOR_BGRA2RGB) #convertion  vers rgb pour l'utilisattion de mediapipe
            results = self.hands.process(imgRGB) #traitement
            if draw:
                if results.multi_hand_landmarks:# si la main presenter devant l' ecran donner les coordonnee sans tracage sur la main
                    m=-1 #declaration de m a valeur pour indiquer  les 2 mains
                    l3=[] #liste vide
                    for k in range(len(results.multi_hand_landmarks)-1,-1,-1):
                            hanLms=results.multi_hand_landmarks[k]#en metrre les coordonnee de  dans une liste hanlms
                            lmls=[] #liste vide
                            for idd, lm in enumerate(hanLms.landmark):
                                cx, cy = int(lm.x * w), int(lm.y * h)
                                lmls.append([idd,cx,cy])
                                #
                            if i==0 :
                                lmls1=lmls

                            else:
                                lmls2=lmls
                            i+=1
                            self.mpDraw.draw_landmarks(img,landmark_list=hanLms,connections=self.mpHands.HAND_CONNECTIONS)
                            #tracage des points et de connection a l' aide de landmark_list qui prend ces valeur de la liste hanlms
                            lx = [int(hanLms.landmark[i].x * w) for i in range(len(hanLms.landmark))]#centration des points
                            ly = [int(hanLms.landmark[i].y * h) for i in range(len(hanLms.landmark))]
                            x1 = min(lx)#le minimum de coordonnees pour x puis y
                            y1 = min(ly)
                            x2 = max(lx)#le max des coordonnes pour x puis y
                            y2 = max(ly)
                            l3.append([x1,y1,x2,y2]) # mettre ces coordonnes  dans la liste l3 ( coordonner adabter )
                            print(len(l3)) #taille de l3
                            cv.rectangle(img, (x1-20, y2+20), (x2+20, y2 + 40), (150, 150, 150), -1)
                            if m == -1: #if existe une unique main  par default  la main prend le nom right
                                cv.putText(img, 'Right', ((lmls1[0][1], lmls1[0][2] + 30)), cv.FONT_ITALIC, 1,
                                           (0, 255, 255), 1)
                            elif len(lmls2)!=0 : #autrement en peut utiliser directement i

                                cv.putText(img, 'Right', (lmls1[0][1], lmls1[0][2] + 30), cv.FONT_ITALIC, 1,
                                           (0, 255, 255), 1)
                                cv.putText(img, 'Left', (lmls2[0][1], lmls2[0][2] + 30), cv.FONT_ITALIC, 1,
                                           (0, 255, 255),
                                           1)

                            m+=1
                            cv.rectangle(img, (x1-20, y1-20), (x2+20, y2+20), (0, 0, 0), thickness=1)


                    hand = {1: [1, 2, 3, 4], 2: [5, 6, 7, 8], 3: [9, 10, 11, 12],
                            4: [13, 14, 15, 16], 5: [17, 18, 19, 20]}
                    if len(lmls1) != 0:
                                for  n in hand.keys():
                                    if lmls1[hand[n][3]][2] == min([lmls1[k][2] for k in hand[n]]):
                                        l[n- 1] = 1
                                x1 = lmls1[0][1] # pour tr ouver la position de la main1la plus proche
                                x2 = lmls1[3][1]
                                x3 = lmls1[4][1]
                                y1 = lmls1[0][2]
                                y2 = lmls1[3][2]
                                y3 = lmls1[4][2]
                                z1 = complex((x3 - x2), (y3 - y2))
                                z2 = complex((x2 - x1), (y2 - y1))
                                if z1!=0 :#calcule de langle pour verifier  la coincidence
                                    a = -angle(z2 / z1, True)
                                    # cv.putText(img, str(a), (100, 100), cv.FONT_HERSHEY_PLAIN, 1, (0, 0, 0), 1)
                                    if abs(a) > 10:
                                        l[0] = 0
                    if len(lmls2) != 0:
                                for n in hand.keys():
                                    if lmls2[hand[n][3]][2] == min([lmls2[k][2] for k in hand[n]]):
                                        l1[n- 1] = 1 # identifer deque le  doight est  detectees

                                x1 = lmls2[0][1]
                                x2 = lmls2[3][1] #meme chose pour
                                x3 = lmls2[4][1]
                                y1 = lmls2[0][2]
                                y2 = lmls2[3][2]
                                y3 = lmls2[4][2]
                                z1 = complex((x3 - x2), (y3 - y2))
                                z2 = complex((x2 - x1), (y2 - y1))
                                if z1 != 0:
                                    a = -angle(z2 / z1, True)
                                    # cv.putText(img, str(a), (100, 100), cv.FONT_HERSHEY_PLAIN, 1, (0, 0, 0), 1)
                                    if abs(a) > 10:
                                        l1[0] = 0
                            # atp.mouse.move(x_1,y_1)
            return l,l1,lmls1,lmls2 # cette classe renvoie les coordonnes  des points , ainsi  une liste de point existe  en coordonnee en y  sur la camera  , hand se comporte comme modelisation