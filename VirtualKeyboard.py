import cv2 as cv
import time
import Handmodule as hm
import drawkeyboard
import numpy as np
import AImouse
def main():# ce comporte comme  une methode

    cap= cv.VideoCapture(0)
    import keyboard #  permettre d'effectuer la modification sur  la claver de pc directement
    keys=drawkeyboard.keyboardm((10,100),10)#!!
    cap.set(3,700)# resolution
    cap.set(4,1300)
    blank=np.zeros((480,640,3),'uint8')
    detector=hm.HandDetect() #detection de la main
    wait=4 # initialisation de wait  et k
    k=0
    while  1 : # while true
        _,img=cap.read() # je lis de la image de mon webcam

        hand1,hand2,lmls1,lmls2=detector.findHands(img) # je utilise la fonction pour trouver les  doight puis je mette les coordonnnes dans le deux liste resp hand1 and hand2

        if hand1==[0,1,0,0,0] or hand1==[0,1,1,0,0] : #  nous associons les fonction pour chaque doient de chaque mains
            [cx,cy]=lmls1[8][1:] #
            for key in keys.keydict : # les clees des dictionnaire cree  dans draw =keyboard

                    if hand1 == [0, 1, 1, 0, 0]:
                        if k == wait: #pour quoi cette condtion
                            print(key)
                            keyboard.write(key) # ordre d'ecrire
                            k = 0
                        else:
                            k += 1

