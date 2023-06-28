import sys
import os
import multiprocessing as mltp
import threading
from tkinter import *
from tkinter import filedialog
from functools import partial
from typing import List
from featureExtraction.process.fix import indice_not_process,fix_barra,fix_barra_moda,fix_pose
from ui.controller.preProcess import preProcess
from ui.view.playerWin import PlayerWin
from ui.view.getPath import getPath
from ui.controller.videoController import VideoController
from util.decorators import timed
from util.flag import Flag

class MainWindow():
    
    def __init__(self, btns = None, flags:List[Flag] = [None], preRender = lambda frame,cel:frame):
        finished = Flag("Processed")
        all_flags = [finished] + flags
        initial_state = {
          "frame":0,
          "velocidade":1.0,
          "flags":flags
        }      
        fy = lambda : self.player.setState(initial_state)
        finished.setFx(lambda : (self.fix(), fy()))

        #inicia a UI
        self.render(btns=btns, flags=all_flags, preRender=preRender)
        
    def render(self, btns , flags , preRender = lambda id,frame:frame):
        '''Inicia a parte grafica'''

        #self.path = getPath()
        self.path = "/home/guest/Área de Trabalho/TCC/Tecnologico/Source/Programa/python/midia/lazy_white.mp4" 
        self.controller = VideoController(path=self.path)
        self.player = PlayerWin(self.controller, btns, flags, preRender)


        #pre processamento ocorre em paralelo
        thread_process = threading.Thread(target=preProcess, args=(self.controller, flags),daemon=True)
        thread_process.start()
        #Persiste o Player
        self.player.run()

    def fix(self):
        not_allocated = indice_not_process(self.controller.buffer)
        for i in not_allocated['line']:
            fix_barra(self.controller.buffer, i)
        for i in not_allocated['pose']:
            fix_pose(self.controller.buffer, i)
        fix_barra_moda(self.controller.buffer)