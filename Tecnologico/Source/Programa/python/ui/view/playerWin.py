import sys
import os
from turtle import width
from typing import Callable, Dict, List
from warnings import catch_warnings
import cv2
import numpy as np 
from tkinter import *
from tkinter import filedialog
import multiprocessing as mltp
from PIL import ImageTk, Image

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from  ui.model.videoController import VideoController
from  ui.model.buttonSketch import ButtonSketch
from  ui.view.menuPlayerWin import MenuPlayerWin

class PlayerWin():
    def __init__(self,controller:VideoController,  buttons:List[ButtonSketch] = None):
        #Meta dados da Janela Tkinter
        self.conf = {
            "title":"TCC - Lucas Mateus Fernandes",
            "path":"",
            "scale":0.5,
            "bord":(0,0),
            "color":"gray17",
            "last_frame":-1,
            "velocidade":1
        }
        #Carrega o Video
        self.controller = controller

        #Cria a Janela baseada nas configurações do video
        self.window = Tk()
        self.window.title( self.conf["title"] )
        self.window.configure( bg=self.conf["color"] )
        self.window.resizable( False, False )
        self.resize()
        self.canvas = Label( self.window )

        self.menuPlayer = MenuPlayerWin(self.controller, buttons)

        #Linka o Player e o ControllerPlayer para fecharem juntas
        player = self.window
        menu = self.menuPlayer.window
        on_close = lambda: (player.destroy(), menu.destroy(), sys.exit())
        menu.protocol("WM_DELETE_WINDOW", on_close)
        player.protocol("WM_DELETE_WINDOW", on_close)
        
        # #Cria uma tred para desenhar
        mltp.Process(target=self.play())

        # #Cria uma tred para desenhar
        # play_thread = mltp.Process(target=self.play)
        # play_thread.start()
    
    def switchController(self, controller:VideoController):
        '''Altera o Video em exibição'''
        #Altera o Switch
        self.controller = controller
        self.resize()
        #Reconfigura o menu associando ao novo controller
        self.menuPlayer.switchController(controller)

    def run(self):
        '''Main Loop'''
        self.window.mainloop();

    def hasModifcation(self):
        '''Verifica se o frame foi alterado e precisa redesenhar'''
        return self.conf['last_frame'] != self.controller.getIdFrame()  
    
    def play(self):
        '''Executa o video frame a frame'''
        self.menuPlayer.attSlider()
        if self.controller.isRunning():
            self.controller.next()
        frame =  self.controller.getFrame() 
        self.draw( frame )
        self.window.after( round(1/self.conf['velocidade']*20) , self.play  )
       
    def resize(self):
        '''Redimensiona o 'Player' '''
        w, h = self._getSizeFrame()
        self.window.geometry( str(w)+"x"+str(h) )
    
    def _getSizeFrame(self):
        '''Retorna a dimensão do frame baseado no scalar do "Player"'''
        a = self.conf["scale"]
        w,h = self.controller.getSize()
        bw, bh = self.conf['bord']
        new_w = round( (w*a)+bw*2 )
        new_h = round( (h*a)+bh*2 )
        return (new_w,new_h)

    def draw(self, frame_cv):
        '''Desenha o frame no Player apenas se teve modificação'''
        if(self.hasModifcation()):
            self.conf['last_frame'] = self.controller.getIdFrame()
            frame_cp = frame_cv.copy()
            frame_cp = cv2.resize(frame_cp, self._getSizeFrame() )
            frame_cp = cv2.cvtColor(frame_cp, cv2.COLOR_BGRA2RGB)
            img = Image.fromarray(frame_cp)
            picture = ImageTk.PhotoImage(img)
            self.canvas.configure(image=picture)
            self.canvas.image = picture
            w, h  = self.conf['bord']
            self.canvas.place(x=w,y=h)
            cv2.destroyAllWindows()