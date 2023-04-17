import sys
import os
from tkinter import *
from tkinter import filedialog
from functools import partial

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from ui.player.playerWin import PlayerWin, Buttons
from ui.player.controllerVideo import ControllerVideo
from processImg.process import Process


def getPath():
    '''Seta o Path do video'''
    aux = Tk()
    currdir = os.getcwd()
    path = filedialog.askopenfilename(parent=aux, initialdir=currdir, title='Selecione o Video')
    aux.destroy()
    return path

class UI():
    
    def __init__(self, process:Process = None, btns = None):
        #inicia a UI
        self.process = process
        self.btns = btns
        self.render()

    def render(self):
        '''Inicia a parte grafica'''
        self.path = "/home/guest/Área de Trabalho/TCC/Tecnologico/Source/Programa/python/midia/c.mp4" #getPath()
        self.controller = ControllerVideo(path=self.path, process_frame=self.processIMG)
        self.player = PlayerWin(self.controller, self.btns)
    
        #Persiste o Player
        self.player.run()
    

    def processIMG(self, frame):
        return self.process.processIMG(frame)

