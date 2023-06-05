import sys
import os
from turtle import width
from typing import Callable, Dict, List
import cv2
import numpy as np 
from tkinter import *
from tkinter import filedialog
import multiprocessing as mltp
from PIL import ImageTk, Image
from ui.model.buttonSketch import ButtonSketch
from ui.controller.videoController import VideoController
from util.flag import Flag

            
class MenuPlayerWin():
    
    def __init__(self, controller:VideoController , buttons:List[ButtonSketch] = None, flags:List[Flag]=[None]):
        self.controller = controller
        self.flags = flags
        self.conf = {
            "title":"Controlador",
            "scale":0.5,
            "bord":(0,0),
            "color":"gray17"
        }

        #Cria a Janela a ser usada como controlador do Player
        self.window = Tk()
        self.window.title( self.conf["title"] )
        self.window.configure( bg=self.conf["color"] )
        desvioX = str(round(((self.window.winfo_screenwidth()-600)/2)))
        self.window.geometry("600x100"+"+"+desvioX+"+0")
        self.window.resizable( False, False )

        #Cria o Time line do video
        win = self.window
        self.frameSlider = Scale(win, from_=0, to=self.controller.getTotalFrame() - 1, orient=HORIZONTAL,variable=DoubleVar(),bg="gray17",fg="white", activebackground='#339999')
        self.frameSlider.place(x=50, y=50, width=500)
        self.frameSlider.set(0)
        self.frameSlider.bind("<ButtonPress-1>", lambda e: self.slider_press())
        self.frameSlider.bind("<ButtonRelease-1>", lambda e: self.slider_release())

        #Cria o botao Play/Pause e N botoes Switcher de flag
        self.n_buttons = 0
        self.switchers = []
        self.playButton =self._createButton("PLAY",self.alter)
        self.activeButton(self.playButton)
        if not buttons  is None:
            for button in buttons:
                name, fx, flag = button.get()
                btn = self._createButton(name, fx) 
                storage_struct = {
                    "button":btn,
                    "flag": flag
                }
                self.switchers.append(storage_struct)

        
    def _createButton(self, name, fx = lambda : None):
        '''Função interna usado para criar um button na tela'''
        WIDTH, BORDER, INTER_BORDER = 50, 50, 10
        i = self.n_buttons
        x = BORDER+(WIDTH*i)+(INTER_BORDER*i)
        
        #Cria o Button
        newButton = Button(self.window, text = name)
        newButton.place(x=x, y=0, width=WIDTH)
        newButton.bind("<ButtonPress-1>", lambda e: fx())
        self.desactiveButton(newButton)
        #Atualiza o indice :
        self.n_buttons = self.n_buttons + 1

        return newButton


    def activeButton(self, btn:Button):
        '''Ativa um button na tela'''
        btn.config(state="normal")
    
    def desactiveButton(self, btn:Button):
        '''Desativa um button na tela'''
        btn.config(state="disable")

    def setState(self, state = None):
        '''Altera o estado dos buttons de acordo com o State'''
        switchers:List[Dict[Button, Flag]] = self.switchers
        for switcher in switchers:
            button = switcher["button"]
            flag = switcher["flag"]
            self.activeButton(button)


    def switchController(self, controller:VideoController):
        '''Altera o controller associado a tela'''
        self.controller = controller
        self.slider2Frame()
        old_value = self.frameSlider.get()
        self.frameSlider.config(from_=0, to=self.controller.getTotalFrame() - 1)
        self.frameSlider.set(old_value)        
       
    def attSlider(self):
        '''Atualiza o player de acordo com o controlador de midia'''
        if(self.controller.isRunning()):
            self.frame2Slider()
        else:
            self.slider2Frame()

    def slider2Frame(self):
        '''Atualiza o controller de acordo com a barra'''
        val_slider = self.frameSlider.get()
        self.controller.setFrame(val_slider)
    
    def frame2Slider(self):
        '''Atualiza a barra de acordo com o controller'''
        id_frame = self.controller.getIdFrame()
        self.frameSlider.set(id_frame)

    def slider_press(self):
        '''Quando clicado'''
        self.conf['state'] = self.controller.isRunning()
        self.controller.pause()

    def slider_release(self):
        '''Quando solto'''
        if self.conf['state']:
            self.controller.play()
        else:
            self.controller.pause()

    def alter(self):
        '''Altera entre Play/Pause'''
        if(self.controller.isRunning()):
            self.controller.pause()
        else:
            self.controller.play()