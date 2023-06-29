import cv2
from typing import Tuple
from model.featureExtraction.poseModel import PoseModel,Segmento

def renderPose(image, pose:PoseModel):
    '''Desenha os segmentos detectados'''

    try:
        #Desenha os traços
        aux_image = _draw_segment(image, pose, (000,000,255), Segmento.CORPO)
        aux_image = _draw_segment(aux_image, pose, (255,000,000), Segmento.BRACO_DIR)
        aux_image = _draw_segment(aux_image, pose, (255,000,000), Segmento.BRACO_ESQ)
        aux_image = _draw_segment(aux_image, pose, (000,255,000), Segmento.PERNA_DIR)
        aux_image = _draw_segment(aux_image, pose, (000,255,000), Segmento.PERNA_ESQ)
        return aux_image
    except:
        return image


def _draw_segment(image,pose:PoseModel,color:Tuple[int,int,int],segmento:Segmento):
    '''Desenha o Segmento na imagem a partir dos pontos de referencia'''

    if segmento is None:
        print("Erro na obtenção do Segmento")
        return image

    # Copia a imagem
    img = image.copy()
    segmentos = segmento.value
    cycle = (segmento == Segmento.CORPO)

    # Desenha uma linha entre cada par de poses consecutivas
    for i in range( len(segmentos)-1 ):
        points = pose.getPoint()
        start = points[segmentos[i]]
        end = points[segmentos[i+1]]
        img = cv2.line(img, start, end, color)

    # Desenha uma linha entre a última e a primeira pose, caso cycle=True
    if cycle:
        points = pose.getPoint()
        points[segmentos[i]]
        start, end = points[segmentos[-1]],points[segmentos[0]]
        img =  cv2.line(img, start, end, color)
    
    return img