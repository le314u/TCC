import cv2
import numpy as np

class Mask():
    
    def __init__(self, path_mask="/home/guest/Área de Trabalho/TCC/Tecnologico/Source/Programa/python/midia/mascara/mask.png"):
        #Cada flag é associada a um numero que define a ordem de prioridade
        self.path_mask = path_mask 
        self.mask = cv2.imread(self.path_mask)

    def getMask(self):
        return self.mask
    
    def getPathMask(self):
        return self.path_mask
    
    def setMask(self, mask):
        self.mask=mask
    
    def setPathMask(self, path_mask):
        mask = cv2.imread(self.path_mask)
        self.path_mask=path_mask
        self.setMask(mask)

    def putMask_path(self, frame, path_mask=None):
        mask = cv2.imread(path_mask)
        return cv2.bitwise_and(frame, mask)

    def putMask(self, frame, mask):
        return cv2.bitwise_and(frame, mask)
    
    def createLineMask(self, frame,p1,p2,thickness=10):
        thickness = round(thickness)
        color = (255,255,255)
        # Criar uma imagem preta
        mask_blank = np.zeros((300, 300), dtype=np.uint8)
        mask_resized = cv2.resize(mask_blank, (frame.shape[1], frame.shape[0]))
        img = cv2.line(mask_resized, p1, p2, color, thickness)
        return img
    
    def createBlockMask(self,frame,start,end):
        # Alias
        x1, y1 = start
        x2, y2 = end
        # Criar uma máscara preta com o mesmo tamanho da imagem
        altura,largura = frame.shape[:2]
        newFrame = np.zeros((altura, largura), dtype=np.uint8)
        # Definir os pontos do polígono que representam o bloco
        pts = np.array([[x1, y1], [x2, y1], [x2, y2], [x1, y2]], np.int32)
        pts = pts.reshape((-1, 1, 2))
        # desenha o Bloco na imagem com a cor branca (255)
        cv2.fillPoly(newFrame, [pts], 255)
        return newFrame

    def highLight_skin(self,frame):
        # Converter a imagem para o espaço de cores HSV
        imagem_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        #Definir os intervalos de cor da pele
        lower_skin = np.array([0, 25, 0], dtype=np.uint8)
        upper_skin = np.array([20, 255, 255], dtype=np.uint8)

        # Aplicar uma máscara para obter apenas a parte da cor da imagem
        mascara = cv2.inRange(imagem_hsv, lower_skin, upper_skin)
        canal_x = cv2.bitwise_and(frame, frame, mask=mascara)
        return canal_x