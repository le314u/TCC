import cv2
import math
import numpy as np

def display_imgs(frame1,frame2):
    # Carregar as imagens
    imagem1 = frame1
    imagem2 = frame2

    # Verificar as dimensões das imagens
    altura, largura = imagem1.shape[:2]

    # Criar uma imagem vazia para combinar as duas imagens
    imagem_combinada = np.zeros((altura, largura * 2), dtype=np.uint8)

    # Copiar as imagens para a imagem combinada
    imagem_combinada[:, :largura] = imagem1
    imagem_combinada[:, largura:] = imagem2

    imagem_combinada = cv2.resize(imagem_combinada, (largura // 1, altura // 1))

    # Exibir a imagem combinada
    cv2.imshow('Imagens Combinadas', imagem_combinada)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def display_img(frame,):
    # Exibir a imagem combinada
    cv2.imshow('Imagem', frame)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def save_img(frame,name):
    cv2.imwrite(f"{name}.png", frame)