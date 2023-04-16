from bdb import Bdb
import cv2
import numpy as np
import mediapipe as mp
from enum import Enum


mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose

# Argumentos para mp_pose.Pose()
# STATIC_IMAGE_MODE  ->  Se definido como false, a solução trata as imagens de entrada como um fluxo de vídeo. Ele tentará detectar a pessoa mais proeminente nas primeiras imagens e, após uma detecção bem-sucedida, localiza ainda mais os marcos da pose. Em imagens subsequentes, ele simplesmente rastreia esses pontos de referência sem invocar outra detecção até que perca o rastreamento, reduzindo a computação e a latência. Se definido como true, a detecção de pessoas executa cada imagem de entrada, ideal para processar um lote de imagens estáticas, possivelmente não relacionadas. Padrão para false.
# MODEL_COMPLEXITY  ->  Complexidade do modelo marco postura: 0, 1ou 2. A precisão do ponto de referência, bem como a latência de inferência, geralmente aumentam com a complexidade do modelo. Padrão para 1.
# SMOOTH_LANDMARKS  ->  Se definido como true, os filtros de solução representam pontos de referência em diferentes imagens de entrada para reduzir o jitter, mas são ignorados se static_image_mode também estiver definido como true. Padrão para true.
# ENABLE_SEGMENTATION  ->  Se definido como true, além dos marcos de pose, a solução também gera a máscara de segmentação. Padrão para false.
# SMOOTH_SEGMENTATION  ->  Se definido como true, a solução filtra as máscaras de segmentação em diferentes imagens de entrada para reduzir o jitter. Ignorado se enable_segmentation for false ou static_image_mode for true. Padrão para true.
# MIN_DETECTION_CONFIDENCE  ->  Valor de confiança mínimo ( [0.0, 1.0]) do modelo de detecção de pessoa para que a detecção seja considerada bem-sucedida. Padrão para 0.5.
# MIN_TRACKING_CONFIDENCE  ->  Valor de confiança mínimo ( [0.0, 1.0]) do modelo de rastreamento de pontos de referência para os pontos de referência de pose a serem considerados rastreados com sucesso, caso contrário, a detecção de pessoa será chamada automaticamente na próxima imagem de entrada. Configurá-lo com um valor mais alto pode aumentar a robustez da solução, às custas de uma latência mais alta. Ignorado se static_image_mode for true, em que a detecção de pessoas simplesmente é executada em todas as imagens. Padrão para 0.5.
pose = mp_pose.Pose(
		static_image_mode=True,
		enable_segmentation=True,
		model_complexity=2,
		min_detection_confidence=0.5,
		min_tracking_confidence=0.5
	)

#ENUM
_braco_dis = lambda lado:('Pulso '+lado,'Cotovelo '+lado)
_braco_prox = lambda lado:('Cotovelo '+lado,'Ombro '+lado)
_perna_dis = lambda lado:('Calcanhar '+lado,'Joelho '+lado)
_perna_prox = lambda lado:('Joelho '+lado,'Quadril '+lado)
Pose=Enum('Pose', ['BRACO_DIR','BRACO_ESQ','PERNA_DIR','PERNA_ESQ','CORPO'])

class Segmento(Enum):
    BRACO_DIR = _braco_dis("Direito")+_braco_prox("Direito")
    BRACO_ESQ = _braco_dis("Esquerdo")+_braco_prox("Esquerdo")
    PERNA_DIR = _perna_dis("Direito")+_perna_prox("Direito")
    PERNA_ESQ = _perna_dis("Esquerdo")+_perna_prox("Esquerdo")
    CORPO = ('Ombro Esquerdo','Ombro Direito','Quadril Direito','Quadril Esquerdo')



def process_img(image):
    '''Faz a estimativa de pose da imagem'''
    results = pose.process(image)
    #Pontos utilizaveis
    points = _point_scale(image,results.pose_landmarks.landmark)
    return points


def _point_scale(image, poseTensor):
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
    '''Passa por todos os pontos de referencia e rastreia o segmento'''
    #copia a imagem
    img = image.copy()
    #Traça uma linha entre os segmentos de acordo com a sequencia 
    end = len(poses.value)-1
    for i in range(end):
        first = points_pose[poses.value[i]]
        end = points_pose[poses.value[i+1]]
        cv2.line(img,first,end,color)
    #Encontra o ultimo ponto com o primeiro
    if(cycle):
        first = points_pose[poses.value[-1]]
        end = points_pose[poses.value[0]]
        cv2.line(img,first,end,color)
    return img

def draw(image,pose,color,points):
    '''Desenha o Segmento na iamgem a partir dos pontos de referencia'''
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