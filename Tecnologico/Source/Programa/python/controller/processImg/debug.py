import cv2
import math
import numpy as np


def resize(frame, scalar):
    altura, largura = frame.shape[:2]
    newSize = (round(largura*scalar), round(altura*scalar))
    newImage = cv2.resize(frame, newSize, interpolation=cv2.INTER_NEAREST)
    return newImage


def join_imgs(*frames):
    if len(frames) < 2:
        raise ValueError("Pelo menos duas imagens devem ser fornecidas.")

    # Verificar as dimensões das imagens
    alturas = [frame.shape[0] for frame in frames]
    larguras = [frame.shape[1] for frame in frames]

    # Encontrar a altura e a largura máxima
    altura_maxima = max(alturas)
    largura_total = sum(larguras)

    # Criar uma imagem vazia para combinar todas as imagens
    imagem_combinada = np.zeros((altura_maxima, largura_total), dtype=np.uint8)

    # Copiar as imagens para a imagem combinada, mantendo as escalas
    inicio = 0
    for frame in frames:
        altura, largura = frame.shape[:2]
        proporcao = altura_maxima / altura
        largura_redimensionada = int(largura * proporcao)

        frame_redimensionado = cv2.resize(frame, (largura_redimensionada, altura_maxima))
        imagem_combinada[:, inicio:inicio + largura_redimensionada] = frame_redimensionado
        inicio += largura_redimensionada
    
    return imagem_combinada

def display_img(frame,name="DEBUG_IMAGE"):
    # Exibir a imagem combinada
    cv2.imshow(name, frame)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def save_img(frame,name):
    cv2.imwrite(f"{name}.png", frame)


def matchGeral(foto,mask):

    # Verifique se os pixels são brancos (valor 255) em ambas as imagens (Mask e foto)
    matching_pixels_mask = (mask == 255) & (foto == 255)

    # Defina o valor da cor laranja (ou o valor de intensidade correspondente em escala de cinza).
    orange_intensity = 128

    # Crie uma matriz com o mesmo shape da imagem da foto, preenchida com o valor da cor laranja.
    orange_image = np.full_like(foto, orange_intensity)

    # Substitua os pixels correspondentes na imagem da foto pela cor laranja.
    foto_colored = np.where(matching_pixels_mask, orange_image, foto)

    return foto_colored