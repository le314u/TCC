
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from model.featureExtraction.contracaoModel import ContracaoModel

def renderTxt(image, data:ContracaoModel):
    '''Desenha os segmentos detectados'''
    data = str(data)
    
    altura, largura, _ = image.shape
    x,y = 50,100

    # Converter a imagem do OpenCV para o formato Pillow
    pillow_image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(pillow_image)
    
    # Definir a fonte
    font_path = "/home/guest/Área de Trabalho/TCC/Tecnologico/Source/Programa/python/midia/static/Cabin-Bold.ttf"  # Substitua pelo caminho para a fonte que deseja usar
    font_size = int(min(largura, altura) * 0.03)  # Ajuste o fator multiplicador conforme necessário
    font = ImageFont.truetype(font_path, font_size)
    color = (255,255,0)
    lines = data.split("\n")

    
    for line in lines:
        draw.text((x, y), line, font=font, fill=color)
        y += font.getsize(line)[1]  # Espaçamento entre as linhas

    # Converter a imagem de volta para o formato OpenCV
    image_with_text = cv2.cvtColor(np.array(pillow_image), cv2.COLOR_RGB2BGR)

    return image_with_text
