import cv2
from featureExtraction.lineModel import LineModel

def renderBar(image, line:LineModel):
    '''Desenha a barra'''
    start, end = line.getPoints
    color = (255,255,0)
    # Copia a imagem
    img = image.copy()
    img = cv2.line(img, start, end, color)
    return img

