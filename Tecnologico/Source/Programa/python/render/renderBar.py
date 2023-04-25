import cv2
from featureExtraction.poseModel import PosePoints

def renderBar(image, points):
    '''Desenha a barra'''
    start, end = points
    color = (255,255,0)
    # Copia a imagem
    img = image.copy()
    img = cv2.line(img, start, end, color)
    return img

