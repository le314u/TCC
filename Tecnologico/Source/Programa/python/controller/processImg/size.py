import cv2
import numpy as np

def resize_A2B(frame1_wrong, frame2_correct):
    # Redimensionar a máscara para corresponder às dimensões da imagem
    frame_redimensionada = cv2.resize(frame1_wrong, (frame2_correct.shape[1], frame2_correct.shape[0]))
    return frame_redimensionada


def createLineMask(frame,p1,p2,thickness=10):
    color = (255,255,255)
    # Criar uma imagem preta
    blank = np.zeros((300, 300), dtype=np.uint8)
    mask = resize_A2B(blank,frame)

    img = cv2.line(mask, p1, p2, color, thickness)
    return img

