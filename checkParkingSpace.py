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


def checkParkingSpace(imgProcessed, imgRef):
    spaces = 0

    #Cortar as imagens 
    for pos in posList:
        x,y = pos 
        imgCrop = imgProcessed[y:y+height, x:x+width]
        cv2.imshow(str(x*y), imgCrop)
        count = cv2.countNonZero(imgCrop)
        #cv2.putText(imgRef, str(count), (x,y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)

        if count > 900:
            color = (0,0,255)            
        else:
            color = (0,255,0)
            spaces += 1
        cv2.rectangle(imgRef, pos,(pos[0]+width,pos[1]+height), color, 3)
        cv2.putText(imgRef, str(cv2.countNonZero(imgCrop)), (x+2, y + height - 6), cv2.FONT_HERSHEY_PLAIN, 1,
                    color, 2)

    cv2.putText(imgRef, "Vagas Livres: " + str(spaces), (2, 30), cv2.FONT_HERSHEY_PLAIN, 2, (0,255,0), 2)


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


    #Descobrir se há um carro nelas. 
    #Estratégia utilizada: Threshold. Se a imagem for plana e consequentemente tiver menos bordas, 
    #iremos dizer que é vaga vazia. Do contrário, teremos uma vaga ocupada.

    ret, frame = cap.read()
    imgGray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (3,3), 1)    
    imgThreshold = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 25, 16)
    imgMedian = cv2.medianBlur(imgThreshold, 5)
    
    kernel = np.ones((3,3), np.uint8)
    imgDilate = cv2.dilate(imgMedian, kernel, iterations=1)

    checkParkingSpace(imgDilate, frame)
    #Desenha os retangulos nas coordenadas da lista
    #for pos in posList:
    #    cv2.rectangle(frame, pos,(pos[0]+width,pos[1]+height), (255,0,0), 3)

    cv2.imshow("Frame", frame)
    cv2.imshow("FrameDilate", imgDilate)
    cv2.setMouseCallback("Frame", mouseClick)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()