import cv2
import math
import numpy as np 
from typing import List,Tuple
from model.featureExtraction.lineModel import LineModel

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
    
def angle_point(pt1, pt2):
    '''Cálcula o ângulo entre dois pontos'''
    x,y = 0,1 # Alias
    delta_x = pt2[x] - pt1[x] #Calcula a diferença entre as coordenadas x dos dois pontos:
    delta_y = pt2[y] - pt1[y] #Calcula a diferença entre as coordenadas y dos dois pontos
    angle_rad = np.arctan2(delta_y, delta_x) #Calcula o ângulo em radianos, levando em consideração os sinais das diferenças das coordenadas.
    angle_deg = np.degrees(angle_rad) #converter o ângulo de radianos para graus.
    return angle_deg

def inclinacao_reta(pt1,pt2):
    '''m = (y2 - y1) / (x2 - x1)'''
    x,y = 0,1 # Alias
    delta_x = pt2[x] - pt1[x] #Calcula a diferença entre as coordenadas x dos dois pontos:
    delta_y = pt2[y] - pt1[y] #Calcula a diferença entre as coordenadas y dos dois pontos
    coeficiente_angular = delta_y / delta_x
    angulo_radianos = math.atan(coeficiente_angular)
    angulo_graus = math.degrees(angulo_radianos)
    return angulo_graus


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


def distance_point_line(ponto:Tuple[int,int], segmento:LineModel):
    x, y = ponto
    points = segmento.getPoints()
    x1, y1 = points[0]
    x2, y2 = points[1]

    # Calcula a distância entre o ponto e a reta usando a fórmula matemática
    distancia = abs((y2-y1)*x - (x2-x1)*y + x2*y1 - y2*x1) / math.sqrt((y2-y1)**2 + (x2-x1)**2)

    return distancia

def distance_points(ponto1:Tuple[int,int], ponto2:Tuple[int,int]):
    x1,y1 = ponto1
    x2,y2 = ponto2
    distancia = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    return distancia


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


def rotate_segment(ponto1:Tuple[int,int], ponto2:Tuple[int,int], angle)->Tuple[int,int]:
    #Referencia
    reference_point = (0,0)
    x,y = 0,1

    # Calcula as coordenadas relativas aos pontos de referência
    p1_relative = ponto1[0] - reference_point[0], ponto1[1] - reference_point[1]
    p2_relative = ponto2[0] - reference_point[0], ponto2[1] - reference_point[1]

    # Converte o ângulo para radianos
    angle_rad = math.radians(angle)
    
    # Aplica as fórmulas de rotação
    rotate_point = lambda p_relative,angle_rad:(
        p_relative[x] * math.cos(angle_rad) - p_relative[y] * math.sin(angle_rad),
        p_relative[x] * math.sin(angle_rad) + p_relative[y] * math.cos(angle_rad)
    )
    p1_rotated = rotate_point(p1_relative,angle_rad)
    p2_rotated = rotate_point(p2_relative,angle_rad)

    # Retorna as coordenadas rotacionadas com o ponto de referência adicionado novamente
    return (round(p1_rotated[x] + reference_point[x]), round(p1_rotated[y] + reference_point[y])
        ), (round(p2_rotated[x] + reference_point[x]), round(p2_rotated[y] + reference_point[y]))
