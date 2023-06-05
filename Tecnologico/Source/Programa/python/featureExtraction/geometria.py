import cv2
import numpy as np 
import math
from featureExtraction.model.lineModel import LineModel

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
    
# Cálculo do ângulo entre dois pontos
def angle_point(pt1, pt2):
    delta_x = pt2[0] - pt1[0]
    delta_y = pt2[1] - pt1[1]
    angle_rad = np.arctan2(delta_y, delta_x)
    angle_deg = np.degrees(angle_rad)
    return angle_deg

def angle_line(line1:LineModel, line2:LineModel) -> float:
    '''Retorna o ângulo entre dois segmentos de reta 0 a 180'''
    # Extrair as coordenadas dos pontos dos segmentos de reta
    pt1, pt2 = line1.getPoints()
    pt3, pt4 = line2.getPoints()
    # Convertendo as linhas para o formato aceito pela função intersectLines
    x1, y1 = pt1
    x2, y2 = pt2
    x3, y3 = pt3
    x4, y4 = pt4
    # Calcular os vetores diretores dos segmentos de reta
    v1 = (x2 - x1, y2 - y1)
    v2 = (x4 - x3, y4 - y3)
    # Calcular o produto escalar
    dot_product = v1[0] * v2[0] + v1[1] * v2[1]
    # Calcular as normas dos vetores diretores
    norm_v1 = math.sqrt(v1[0]**2 + v1[1]**2)
    norm_v2 = math.sqrt(v2[0]**2 + v2[1]**2)
    # Calcular o ângulo em radianos
    angle_rad = math.acos(dot_product / (norm_v1 * norm_v2))
    # Converter o ângulo de radianos para graus
    angle_degrees = math.degrees(angle_rad)
    return abs(angle_degrees)

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