import sys
import os
import multiprocessing as mltp
import threading
from tkinter import *
from tkinter import filedialog
from functools import partial
from typing import List
from featureExtraction.process import indice_not_process,fix_barra,fix_pose
from ui.controller.preProcess import preProcess
from ui.view.playerWin import PlayerWin
from ui.model.videoController import VideoController
from util.decorators import timed
from util.flag import Flag

class Ux():
    
    def __init__(self, btns = None, flags:List[Flag] = [None], preRender = lambda frame,cel:frame):

        #Apos o pre processamento libera os buttons
        finished = Flag("Processed")

        #inicia a UI
        self.render(btns=btns, flags=[finished], preRender=preRender)
        
    def render(self, btns , flags , preRender = lambda id,frame:frame):
        '''Inicia a parte grafica'''

        #self.path = "/home/guest/Área de Trabalho/TCC/Tecnologico/Source/Programa/python/midia/c.mp4" #getPath()
        self.path = "/home/guest/Área de Trabalho/TCC/Tecnologico/Source/Programa/python/midia/lazy.mp4" #getPath()
        self.controller = VideoController(path=self.path)
        self.player = PlayerWin(self.controller, btns, flags, preRender)

        finished = flags[0]
        def fx():
            not_allocated = indice_not_process(self.controller.buffer)
            for i in not_allocated['barra']:
                fix_barra(self.controller.buffer, i)
            for i in not_allocated['pose']:
                fix_pose(self.controller.buffer, i)
        fy = lambda : self.player.setState()
        finished.setFx(lambda : (fx(), fy()))


        #pre processamento ocorre em paralelo
        thread_process = threading.Thread(target=preProcess, args=(self.controller, finished),daemon=True)
        thread_process.start()
        #Persiste o Player
        self.player.run()