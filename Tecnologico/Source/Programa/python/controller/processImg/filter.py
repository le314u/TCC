import cv2
import math
import numpy as np

from controller.processImg.debug import save_img, display_img, join_imgs,resize, matchGeral


def pixelizacao(frame,size):
    size_block = round(size)
    # Carregar a imagem
    imagem = frame.copy()
    # Obter as dimensões da imagem
    altura, largura = imagem.shape[:2]
    # Definir o tamanho dos blocos
    # Redimensionar a imagem para a pixelização
    imagem_pixelada = cv2.resize(imagem, (largura // size_block, altura // size_block), interpolation=cv2.INTER_LINEAR)
    imagem_tratada = cv2.resize(imagem_pixelada, (largura, altura), interpolation=cv2.INTER_NEAREST)
    return imagem_tratada

def limiarizacao(frame, valor, to_white=True):
    # Carregar a imagem
    imagem = frame.copy()
    #Acima do valor para para Branco
    type = cv2.THRESH_BINARY if to_white else cv2.THRESH_BINARY_INV
    # Aplicar a limiarização
    _, imagem_tratada = cv2.threshold(imagem, valor, 255, type)
    return imagem_tratada

def imagem_cinza(frame):
    # Converter a imagem para escala de cinza
    imagem_cinza = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    return imagem_cinza

def suavizacao(frame,size):
    newSize = round(size)
    return cv2.blur(frame, (newSize, newSize))

def rotacao(frame, angulo):
    # Obtém a altura e a largura da imagem
    altura, largura = frame.shape[:2]
    # Calcula o ponto central da imagem
    centro = (largura // 2, altura // 2)
    # Cria a matriz de rotação usando o ângulo e o ponto central
    matriz_rotacao = cv2.getRotationMatrix2D(centro, angulo, 1.0)
    # Aplica a transformação de rotação na imagem
    imagem_rotacionada = cv2.warpAffine(frame, matriz_rotacao, (largura, altura))
    return imagem_rotacionada