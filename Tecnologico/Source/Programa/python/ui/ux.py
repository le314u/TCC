import sys
import os
from tkinter import *
from tkinter import filedialog
from functools import partial
from ui.view.playerWin import PlayerWin
from ui.model.videoController import VideoController


class Ux():
    
    def __init__(self, btns = None):
        #inicia a UI
        self.btns = btns
        self.render()

    def render(self):
        '''Inicia a parte grafica'''
        self.path = "/home/guest/Área de Trabalho/TCC/Tecnologico/Source/Programa/python/midia/c.mp4" #getPath()
        self.controller = VideoController(path=self.path)
        self.preProcessIMG( self.controller )
        self.player = PlayerWin(self.controller, self.btns)
        
        #Persiste o Player
        self.player.run()
    
    def preProcessIMG(self, controller:VideoController):
        #Para cada frame do video faz o processamento

        #pega o frame faz detecção da pose
        #encontra a barra
        #
        controller.buffer
        pass


