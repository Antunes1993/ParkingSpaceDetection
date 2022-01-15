import os 
import cv2 
import pickle 
import numpy as np 

width, height = 105, 50

os.chdir("CarParkProject")
cap = cv2.VideoCapture('carPark.mp4')

try:
    with open('CarParkPositions', 'rb') as f:
        posList = pickle.load(f)
except:
    posList = []

def mouseClick(events, x, y, flags, param):    
    #Se clicarmos com botão esquerdo, iremos adicionar a posição do clique na lista
    if events == cv2.EVENT_LBUTTONDOWN:
        posList.append((x,y))
        print ("Posição: ", x, y)
   
    if events == cv2.EVENT_RBUTTONDOWN:
        for i,pos in enumerate(posList):
            x1,y1 = pos 
            if x1 < x < x1 + width and y1 <y < y1 + height:
                posList.pop(i)

    with open('CarParkPositions', 'wb') as f:
        pickle.dump(posList, f)


while True:  

    #Repete o video quando ele termina
    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    ret, frame = cap.read()

    #Desenha os retangulos nas coordenadas da lista
    for pos in posList:
        cv2.rectangle(frame, pos,(pos[0]+width,pos[1]+height), (0,255,0), 3)

    cv2.imshow("Frame", frame)
    cv2.setMouseCallback("Frame", mouseClick)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()