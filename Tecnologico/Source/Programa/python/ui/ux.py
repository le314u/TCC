import sys
import os
import multiprocessing as mltp
import threading
from tkinter import *
from tkinter import filedialog
from functools import partial
from ui.controller.preProcess import preProcess
from ui.view.playerWin import PlayerWin
from ui.model.videoController import VideoController
from util.decorators import timed

class Ux():
    
    def __init__(self, btns = None):
        #inicia a UI
        self.btns = btns
        self.render()
        
    def render(self):
        '''Inicia a parte grafica'''
        self.path = "/home/guest/Área de Trabalho/TCC/Tecnologico/Source/Programa/python/midia/c.mp4" #getPath()
        self.controller = VideoController(path=self.path)
        self.player = PlayerWin(self.controller, self.btns)
        #pre processamento ocorre em paralelo
        thread_process = threading.Thread(target=preProcess,args=(self.controller,))
        thread_process.start()
        #Persiste o Player
        self.player.run()
        
