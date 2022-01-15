import os
from turtle import width 
import cv2 
import pickle 

width, height = 105, 50
os.chdir("CarParkProject")
img = cv2.imread('carParkImg.png')

try:
    with open('CarParkPositions', 'rb') as f:
        posList = pickle.load(f)
except:
    posList = []


#No caso da imagem não irá funcionar, pois a imagem é carregada apenas uma vez. 
#Porém ser for um vídeo isso será corrigido, pois o vídeo é composto por vários frames carregados em sequência.
#Para isso é necessário inserir o cv2.imread dentro do loop para estar sempre recarregando a imagem.
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
    img = cv2.imread('carParkImg.png')

    for pos in posList:
        cv2.rectangle(img, pos,(pos[0]+width,pos[1]+height), (0,255,0), 3)
    
    cv2.imshow("image", img)    
    cv2.setMouseCallback("image", mouseClick)
    cv2.waitKey(1)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
