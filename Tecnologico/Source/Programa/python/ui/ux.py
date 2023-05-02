import sys
import os
import multiprocessing as mltp
import threading
from tkinter import *
from tkinter import filedialog
from functools import partial
from typing import List
from ui.controller.preProcess import preProcess
from ui.view.playerWin import PlayerWin
from ui.model.videoController import VideoController
from util.decorators import timed
from util.flag import Flag

class Ux():
    
    def __init__(self, btns = None , flags:List[Flag] = [None]):
        

        #Apos o pre processamento libera os buttons
        preProcess_ok = lambda : self.player.setState()
        finished = Flag("Processed",preProcess_ok)

        #inicia a UI
        self.render(btns, [finished])
        
    def render(self, btns , flags):
        '''Inicia a parte grafica'''
        self.path = "/home/guest/Área de Trabalho/TCC/Tecnologico/Source/Programa/python/midia/c.mp4" #getPath()
        self.controller = VideoController(path=self.path)
        self.player = PlayerWin(self.controller, btns, flags)

        #pre processamento ocorre em paralelo
        fineshed = flags[0]
        thread_process = threading.Thread(target=preProcess, args=(self.controller, fineshed),daemon=True)
        thread_process.start()
        #Persiste o Player
        self.player.run()
