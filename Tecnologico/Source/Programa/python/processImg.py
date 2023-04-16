from ast import Num
import cv2
import numpy as np 

def bar(frame) -> object:
    '''Destaca a barra'''
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
        cv2.line(img,(x1,y1), (x2,y2), (0,0,255),2) 
    return img

def intercept(line1, line2) -> bool:
    '''Retorna se as duas linhas se cruzam em algum momento'''
    # Convertendo as linhas para o formato aceito pela função intersectLines
    pt1, pt2 = line1
    pt3, pt4 = line2
    line1 = np.array([pt1[0], pt1[1], pt2[0], pt2[1]], dtype=np.float32)
    line2 = np.array([pt3[0], pt3[1], pt4[0], pt4[1]], dtype=np.float32)

    # Encontrando o ponto de interseção das duas linhas
    point = cv2.intersectLines(line1, line2, tolerance=0.1)

    return point[2] == 1
    

def angle(line1, line2) -> Num:
    '''Retorna o angulo entre dois segmentos de reta'''
    # Convertendo as linhas para o formato aceito pela função intersectLines
    pt1, pt2 = line1
    pt3, pt4 = line2

    # Calcule o vetor diretor de cada segmento de reta
    vec1 = cv2.subtract(pt2, pt1)
    vec2 = cv2.subtract(pt4, pt3)

    # Calcule o ângulo entre os dois vetores diretores
    angle = cv2.fastAtan2(vec1[1], vec1[0]) - cv2.fastAtan2(vec2[1], vec2[0])
    
    # Converta o ângulo de graus para radianos
    angle_rad = np.deg2rad(angle)

    return angle


