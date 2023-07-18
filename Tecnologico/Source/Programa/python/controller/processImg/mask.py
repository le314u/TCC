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
        color = (255,255,255)
        # Criar uma imagem preta
        mask_blank = np.zeros((300, 300), dtype=np.uint8)
        mask_resized = cv2.resize(mask_blank, (frame.shape[1], frame.shape[0]))
        img = cv2.line(mask_resized, p1, p2, color, thickness)
        return img