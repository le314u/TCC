import cv2
import numpy as np 

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
    

def angle(line1, line2) -> float:
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

def angle(theta):
    '''Converte um ângulo em graus para radianos.'''
    return theta * 180 / np.pi

def segment(rho, theta, comprimento=2000):
    '''Representação de um segmento de reta'''
    cos = np.cos(theta) 
    sen = np.sin(theta) 
    x = cos*rho
    y = sen*rho
    x1 = int(x + comprimento *(-sen)) 
    x2 = int(x - comprimento *(-sen)) 
    y1 = int(y + comprimento *(cos)) 
    y2 = int(y - comprimento *(cos))  
    return( (x1,y1), (x2,y2) )