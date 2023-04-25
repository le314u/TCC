import cv2
import numpy as np 

def bar(frame) -> object:
    '''Dado um frame retorna a barra'''
    img = frame.copy()
    #converte em preto e branco
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY) 
    #Detecção de borda
    edges = cv2.Canny(gray,550,150,apertureSize = 3) 
    lines = cv2.HoughLines(edges,1,np.pi/180, 200) 
    for r,theta in lines[0]: 
        a = np.cos(theta) 
        b = np.sin(theta) 
        x0 = a*r 
        y0 = b*r 
        x1 = int(x0 + 2000*(-b)) 
        y1 = int(y0 + 2000*(a)) 
        x2 = int(x0 - 2000*(-b)) 
        y2 = int(y0 - 2000*(a))           
        #cv2.line(img,(x1,y1), (x2,y2), (0,0,255),2) 
    return ( (x1,y1), (x2,y2) )
