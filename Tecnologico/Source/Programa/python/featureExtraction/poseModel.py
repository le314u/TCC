import cv2
import numpy as np
import mediapipe as mp
from enum import Enum
from bdb import Bdb

from dec_time import TIME

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
pose_midia_pipe = mp_pose.Pose(
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

class Segmento(Enum):
    CORPO = ('Ombro Esquerdo','Ombro Direito','Quadril Direito','Quadril Esquerdo')
    BRACO_DIR = _braco_dis("Direito")+_braco_prox("Direito")
    BRACO_ESQ = _braco_dis("Esquerdo")+_braco_prox("Esquerdo")
    PERNA_DIR = _perna_dis("Direito")+_perna_prox("Direito")
    PERNA_ESQ = _perna_dis("Esquerdo")+_perna_prox("Esquerdo")

class Pose(Enum):
    CORPO = 0
    BRACO_DIR = 1
    BRACO_ESQ = 2
    PERNA_DIR = 3
    PERNA_ESQ = 4


class PosePoints():
    #Variavel de classe
    midia_pipe_ENUM = mp.solutions.pose.PoseLandmark
    pose_midia_pipe = pose_midia_pipe #Midia Pipe
    #Enum
    Segmento = Segmento
    Pose = Pose

    @staticmethod
    def getPose(image):
        '''Retorna a Pose de acordo com tensor Flow'''
        return PosePoints.pose_midia_pipe.process(image)

    def __init__(self,image) -> None:
        
        hight, width, _ = image.shape
        poseTensor = PosePoints.getPose(image)

        rPoint = lambda point:(round(point.x*width) , round(point.y*hight) )
        access = lambda key: rPoint(poseTensor.pose_landmarks.landmark[PosePoints.midia_pipe_ENUM[key]])

        self.pose_points = {
            'Tornozelo Esquerdo': access("LEFT_ANKLE") ,
            'Cotovelo Esquerdo': access("LEFT_ELBOW") ,
            'Ombro Esquerdo': access("LEFT_SHOULDER") ,
            'Calcanhar Esquerdo': access("LEFT_HEEL") ,
            'Quadril Esquerdo': access("LEFT_HIP") ,
            'Joelho Esquerdo': access("LEFT_KNEE") ,
            'Pulso Esquerdo': access("LEFT_WRIST") ,
            'Tornozelo Direito': access("RIGHT_ANKLE") ,
            'Cotovelo Direito': access("RIGHT_ELBOW") ,
            'Ombro Direito': access("RIGHT_SHOULDER") ,
            'Calcanhar Direito': access("RIGHT_HEEL") ,
            'Quadril Direito': access("RIGHT_HIP") ,
            'Joelho Direito': access("RIGHT_KNEE") ,
            'Pulso Direito': access("RIGHT_WRIST") 
        }    

    def getPoints(self):
        return self.pose_points