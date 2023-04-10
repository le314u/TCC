from bdb import Bdb
import cv2
import numpy as np
import mediapipe as mp
from enum import Enum

#ENUM
_braco = lambda lado:('Pulso '+lado,'Cotovelo '+lado,'Ombro '+lado)
_perna = lambda lado:('Calcanhar '+lado,'Joelho '+lado,'Quadril '+lado)
Pose=Enum('Pose', ['BRACO_DIR','BRACO_ESQ','PERNA_DIR','PERNA_ESQ','CORPO'])

class Segmento(Enum):
    BRACO_DIR = _braco("Direito")
    BRACO_ESQ = _braco("Esquerdo")
    PERNA_DIR = _perna("Direito")
    PERNA_ESQ = _perna("Esquerdo")
    CORPO = ('Ombro Esquerdo','Ombro Direito','Quadril Direito','Quadril Esquerdo')



def point_scale(image, poseTensor):
    '''Dado uma pose extrai apenas os dados que serão usados'''
    pose_enum = mp.solutions.pose.PoseLandmark
    hight, width, _ = image.shape
    rPoint = lambda pose:(round(pose.x*width) , round(pose.y*hight) )
    struct = {
        'Tornozelo Esquerdo':rPoint(poseTensor[pose_enum.LEFT_ANKLE]),
        'Cotovelo Esquerdo':rPoint(poseTensor[pose_enum.LEFT_ELBOW]),
        'Ombro Esquerdo':rPoint(poseTensor[pose_enum.LEFT_SHOULDER]),
        'Calcanhar Esquerdo':rPoint(poseTensor[pose_enum.LEFT_HEEL]),
        'Quadril Esquerdo':rPoint(poseTensor[pose_enum.LEFT_HIP]),
        'Joelho Esquerdo':rPoint(poseTensor[pose_enum.LEFT_KNEE]),
        'Pulso Esquerdo':rPoint(poseTensor[pose_enum.LEFT_WRIST]),
        'Tornozelo Direito':rPoint(poseTensor[pose_enum.RIGHT_ANKLE]),
        'Cotovelo Direito':rPoint(poseTensor[pose_enum.RIGHT_ELBOW]),
        'Ombro Direito':rPoint(poseTensor[pose_enum.RIGHT_SHOULDER]),
        'Calcanhar Direito':rPoint(poseTensor[pose_enum.RIGHT_HEEL]),
        'Quadril Direito':rPoint(poseTensor[pose_enum.RIGHT_HIP]),
        'Joelho Direito':rPoint(poseTensor[pose_enum.RIGHT_KNEE]),
        'Pulso Direito':rPoint(poseTensor[pose_enum.RIGHT_WRIST])
    }
    return struct

def _draw_segment(color,image,poses,points_pose,cycle=False):
    print("\n")
    #copia a imagem
    img = image.copy()
    #Traça uma linha entre os segmentos de acordo com a sequencia 
    end = len(poses.value)-1
    for i in range(end):
        first = points_pose[poses.value[i]]
        end = points_pose[poses.value[i+1]]

        print(poses.value[i])
        print( points_pose[poses.value[i]])

        print(poses.value[i+1])
        print( points_pose[poses.value[i+1]])


        print( poses.value[i] +"->"+poses.value[i+1])
        print( str(first) +"->"+str(end))
        
        cv2.line(img,first,end,color)
    #Encontra o ultimo ponto com o primeiro
    if(cycle):
        first = points_pose[poses.value[-1]]
        end = points_pose[poses.value[0]]
        cv2.line(img,first,end,color)
        
    return img

def draw(image,pose,color,points):
    if pose == Pose.BRACO_DIR:
        return _draw_segment(color,image,Segmento.BRACO_DIR,points,False)
    elif pose == Pose.BRACO_ESQ:
        return _draw_segment(color,image,Segmento.BRACO_ESQ,points,False)
    elif pose == Pose.PERNA_DIR:
        return _draw_segment(color,image,Segmento.PERNA_DIR,points,False)
    elif pose == Pose.PERNA_ESQ:
        return _draw_segment(color,image,Segmento.PERNA_ESQ,points,False)
    elif pose == Pose.CORPO:
        return _draw_segment(color,image,Segmento.CORPO,points,True)
    else:
        return image