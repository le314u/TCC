from io import BytesIO
import cv2
import numpy as np
from controller.render.pipe import PipeLine

from controller.video.videoController import VideoController

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


def createVideo(pipeRender:PipeLine, controller:VideoController):
    '''Pega um conjunto de frames e cria um video'''

    #Video Original
    video_original = controller.getVideo()

    #Frames
    frames = []
    for id in range(controller.getTotalFrame()):
        cel = controller.getCel(id)
        frame = cel.getFrame()
        frame_processed = pipeRender.processImg(frame, cel)
        frames.append(frame_processed)

    #Quantidade de fps
    fps = int(video_original.get(cv2.CAP_PROP_FPS))
    #Dimensão do video
    frame_size = (int(video_original.get(cv2.CAP_PROP_FRAME_WIDTH)), int(video_original.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    #codex
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # ou outro codec
    #Salva na memoria
    buffer = BytesIO()
    writer = cv2.VideoWriter(buffer, fourcc, fps, frame_size)
    #Passa frame a frame
    for f in frames:
        writer.write(f)
    #Encerra o video
    writer.release()
    #retorna o novo video
    video_data = buffer.getvalue()
    return video_data