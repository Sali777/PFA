import numpy as np
import Handmodule as hm
import cv2 as cv
import time
from time import sleep
import autopy as atp
import keyboard
import drawkeyboard
j=False #
selector=0
ptime = 0
detector = hm.HandDetect()
Webcam=1
cap = cv.VideoCapture(Webcam)
wait =5 #it was 7
tim = 4
keys=drawkeyboard.keyboardm((15,100),10,keyboard_color=(0,0,255),character_color=(255,0,0)) # paramettre color de claver et des caracteres
blank=np.zeros((720,1280,3),'uint8') # a zapper
k=4
c=''
ch=''
maxch=20
keyboard_status=0# 0 lower #1 upcase
backspace_time=0
while 1:

    ctime = time.time()
    fps = int(1 / (ctime - ptime))
    ptime = ctime # frame par sc
    succ, img = cap.read()
    img=cv.flip(img,1) #inverser l'image
    hand, hand1, lmls1, lmls2 = detector.findHands(img) # methode findhands from hm
    if selector in [0,1,2,3,4,5,6] :
        cv.putText(img, 'AI mouse ', (150, 450),cv.FONT_HERSHEY_COMPLEX , 2, (255, 0, 0), 1)
        if len(lmls1) != 0: # if une main est presenter  devant l' ecran
            print(lmls1)
            [x_1, y_1] = lmls1[12][1:]
            [x_2, y_2] = lmls1[8][1:]#extrafction des coordonnes des point d'indice 12 et 8
            x_m = int((x_1 + x_2) / 2) #distance  je pense que tout ca zyaed puisque les fonction a bien identifer ce il suffit  de mod/ifier les parametre de chaque methode appelee
            y_m = (y_1 + y_2) // 2
            cv.line(img, (x_1, y_1), (x_2, y_2), (0, 255, 0), 1)
            cv.circle(img, (x_1, y_1), 8, (255,0,0), -1)
            cv.circle(img, (x_2, y_2), 8, (255,0,0), -1)
            cv.circle(img, (x_m, y_m), 8, (0, 0 , 0), -1)
            if (hand == [0, 1, 0, 0, 0] ):#
                xmouse, ymouse = abs (int(((x_2 / 540) * 1000)+130)), abs(int((y_2 / 168) * 300+10)) # la solution est ici le probleme dans la partie negative des axe

                atp.mouse.move( xmouse, ymouse)  #permettre de deplacer la souris

            # je trouver une solution pour la partie out of bounds presque il me reste de comprendre  si je peut de modifier les main utuliser et de comprendre clic exactement
            elif hand == [0, 1, 1, 0, 0]:
                tim += 1 # pour le mise a  jour
                if tim == wait:
                    cv.circle(img, (x_m, y_m), 20, (0, 255, 0), -1)
                    tim = 0 # pour mettre en boucle d' une  autre facon
                    atp.mouse.click();
                    print('left click') # en nepent modifer directement le clic puisque le distance est declaree a 12 et 8  et d'autre
            else:
             if  hand==[0,1,1,1,1]: # j'ai bien modifier
                 selector+=1
        print(hand,hand1)

    if selector>=wait :


        keys.draw(blank,keyboard_status)
        imgOut = cv.addWeighted(img, 0.5, blank, 0.5, 0.5) # c'est quoi l' utilite de blank
        if hand== [0, 1, 0, 0, 0] or hand == [0, 1, 1, 0, 0]:
            [cx, cy] = lmls1[8][1:] # si les point remarquable est representer
            for key in keys.keydict:
                if key == ' ' and (cx in range(keys.keydict[key][0], keys.keydict[key][0] + 400)) and (
                        cy in range(keys.keydict[key][1], keys.keydict[key][1] + 50)):
                    cv.rectangle(imgOut, (keys.keydict[key][0], keys.keydict[key][1]),# deja dessiner et bien positionner dans drawkeyboard
                                 (keys.keydict[key][0] + 400, keys.keydict[key][1] + 50), (0,255 , 0), 1) # pour le cadre qui entoure la rectangle

                    if hand == [0, 1, 1, 0, 0]:

                        if k >= wait:
                            print('space')
                            keyboard.press_and_release('Space') # automatiquement  par la biblio keyboard
                            k = 0
                            c=' '

                            backspace_time=0
                            wait=5
                        else :
                            k = k + 1 # c'est de temps
                elif key == 'backspace' and (cx in range(keys.keydict[key][0], keys.keydict[key][0] + 100)) and (
                                cy in range(keys.keydict[key][1], keys.keydict[key][1] + 50)):
                            cv.rectangle(imgOut, (keys.keydict[key][0], keys.keydict[key][1]),
                                         (keys.keydict[key][0] + 100, keys.keydict[key][1] + 50), (0, 255, 0), 1)
                            if hand == [0, 1, 1, 0, 0]:
                                if k >= wait:
                                    print(key)
                                    keyboard.press_and_release('Backspace')
                                    k = 0
                                    ch=ch[:len(ch)-1] #Permettre de supprimer
                                    j==True # il faut que  ch prend tout les lettre
                                    backspace_time+=1
                                    if 6>backspace_time>4 :
                                        wait=3
                                    elif 10>backspace_time>6 :
                                        wait=1
                                else:
                                     k += 1
                elif key == 'enter' and (cx in range(keys.keydict[key][0], keys.keydict[key][0] + 110)) and (
                                cy in range(keys.keydict[key][1], keys.keydict[key][1] + 40)):
                            cv.rectangle(imgOut, (keys.keydict[key][0], keys.keydict[key][1]),
                                         (keys.keydict[key][0] + 110, keys.keydict[key][1] + 40), (0, 255, 0), 1)
                            if hand == [0, 1, 1, 0, 0]:
                                if k >= wait:
                                    print(key)
                                    keyboard.press_and_release('Enter') # directement
                                    k = 0
                                    ch=''
                                    backspace_time=0
                                    wait=7
                                else:
                                     k += 1
                elif key == 'low/up' and (cx in range(keys.keydict[key][0], keys.keydict[key][0] + 100)) and (
                                cy in range(keys.keydict[key][1], keys.keydict[key][1] + 50)):
                            cv.rectangle(imgOut, (keys.keydict[key][0], keys.keydict[key][1]),
                                         (keys.keydict[key][0] + 100, keys.keydict[key][1] + 50), (0, 255, 0), 1)
                            if hand == [0, 1, 1, 0, 0]:
                                if k >= wait:
                                    print(key)
                                    keyboard.press_and_release('caps lock')
                                    k = 0
                                    keyboard_status+=1 # changement d' etat de clavier
                                    backspace_time = 0
                                    wait=7
                                    if keyboard_status>1 : # cette condition nous permettre   d'ajouter un autre mode de clavier
                                        keyboard_status=0 # si en selection une autre fois elle return a l'etat initial
                                else:
                                     k += 1
                elif (cx in range(keys.keydict[key][0], keys.keydict[key][0] + 50)) and (
                        cy in range(keys.keydict[key][1], keys.keydict[key][1] + 50)) and key not in ['enter','space','backspace']:
                    cv.rectangle(imgOut, (keys.keydict[key][0], keys.keydict[key][1]),
                                 (keys.keydict[key][0] + 50, keys.keydict[key][1] + 50), (0, 255, 0), 1) # si non chaque  rectangle de chaque lettre est encadrer par un rec vert
                    if hand == [0, 1, 1, 0, 0]:
                        if k >= wait:
                            print(key)
                            if key=='.' :
                                keyboard.write('.') # deja existe dans la clavier!  peut etre non declarer dans la clavier reel
                            else :
                             keyboard.press_and_release(key) #  a la condition que  le doight se coincide avec les coordonner de l lettre  et key =lettre desiere conserver dans les clee de dictionnaire en ecrit
                            k = 0
                            c=key
                            backspace_time = 0
                            wait=7
                        else:
                            k += 1
        cv.putText(imgOut, 'AI Keyboard', (100, 400), cv.FONT_HERSHEY_COMPLEX, 2, (152,245,255), 1)
        if keyboard_status==0 :
            cv.putText(imgOut, 'Lower Characters', (10, 470),cv.FONT_HERSHEY_SCRIPT_SIMPLEX , 1, (0, 0, 150), 1)

        elif keyboard_status == 1:
                cv.putText(imgOut, 'Upper Characters', (10, 470), cv.FONT_HERSHEY_SCRIPT_SIMPLEX, 1, (0,255,0 ), 1)
        if  hand==[0,1,1,1,1] : # permettre de modifier des que le doight est presenter en camera
                print('switch')
                sleep(0.2)
                selector+=1
                if selector>11 :
                    selector=0
        ch=ch[:]+c # mise a jour  de chaine
        ch1=ch[:] #  la nouvelle chaine
        if len(ch1)>=maxch :
            ch1=ch1[len(ch)-maxch:len(ch)] # mise a jour  pour mettre la chaine plus courte
        elif j==True: # le role de j
            if len(ch)>=maxch:
             ch1=ch[len(ch)-maxch:]
            else :
                ch1=ch[:]
            j=False
        c=''
        cv.putText(imgOut,ch1,(keys.origin[0]+60,keys.origin[1]-25),cv.FONT_HERSHEY_PLAIN,2,(0,255,0),2)
        print(k)
    cv.putText(img, str(fps), (50, 70), cv.FONT_HERSHEY_PLAIN, 2, (255, 0, 255), 2)
    if selector>=8:
         cv.putText(imgOut, str(wait), (50, 90), cv.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
    if selector in [0,1,2,3,4,5,6,7] :
        cv.imshow('Keyboard & Mouse', img)
    elif selector>=8 :
        cv.imshow('Keyboard & Mouse',imgOut)

    cv.waitKey(1) # le role de selector end j