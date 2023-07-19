import cv2
import numpy as np

def count_white_pixels(frame):
    # Converter o frame para escala de cinza (isso é importante para trabalhar com cores)
    gray_frame = frame

    # Definir um limite para considerar o pixel como branco
    threshold = 200

    # Criar uma máscara com os pixels brancos (pixels com intensidade acima do limite)
    white_mask = gray_frame > threshold

    # Contar a quantidade de pixels brancos na máscara
    white_pixel_count = white_mask.sum()

    return white_pixel_count

def count_discontinuities(frame, threshold):
    # Converter a imagem para escala de cinza (isso é importante para trabalhar com cores)
    gray_image = frame

    # Calcular o gradiente da imagem usando o filtro de Sobel
    grad_x = cv2.Sobel(gray_image, cv2.CV_64F, 1, 0, ksize=3)
    grad_y = cv2.Sobel(gray_image, cv2.CV_64F, 0, 1, ksize=3)
    gradient_magnitude = np.sqrt(grad_x ** 2 + grad_y ** 2)

    # Contar quantos pontos do gradiente excedem o limiar
    count = np.count_nonzero(gradient_magnitude > threshold)

    return count
