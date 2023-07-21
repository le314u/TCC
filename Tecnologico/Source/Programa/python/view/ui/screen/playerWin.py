import sys
import cv2
import signal
import multiprocessing as mltp
import numpy as np
import traceback
from typing import Callable, Dict, List
from PIL import ImageTk, Image
from tkinter import Label,Tk
from controller.render.pipe import PipeLine
from controller.util.flag import Flag
from controller.video.videoController import VideoController
from view.ui.components.buttonSketch import ButtonSketch
from view.ui.screen.menuPlayerWin import MenuPlayerWin


class PlayerWin():
    def __init__(self,controller:VideoController,  buttons:List[ButtonSketch] = None, flags:List[Flag]=[None], pip_render=None):
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
        #Carrega arg's do construtor
        self.controller = controller
        self.pip_render = pip_render
        self.flags = flags

        #Cria a Janela baseada nas configurações do video
        self.window = Tk()
        self.window.title( self.conf["title"] )
        self.window.configure( bg=self.conf["color"] )
        self.window.resizable( False, False )
        self.resize()
        self.canvas = Label( self.window )
        self.menuPlayer = MenuPlayerWin(self.conf, self.controller, buttons, self.flags)

        #Linka o Player e o ControllerPlayer para fecharem juntas
        player = self.window
        menu = self.menuPlayer.window
        def on_close():
            player.destroy()
            menu.destroy()
            sys.exit()



        player.protocol("WM_DELETE_WINDOW", on_close)
        menu.protocol("WM_DELETE_WINDOW", on_close)
        # Configura o tratamento para o sinal de interrupção (SIGINT)
        signal.signal(signal.SIGINT, on_close)

        #Cria uma tred para desenhar
        processo = mltp.Process(target=self.play)
        #processo.start()       

        self.play()

    def setState(self, state=None):
        '''Altera o estado do Menu ativando os buttons'''
        fx = lambda : self.menuPlayer.setState(state)
        self.window.after(0,fx)
    
    def switchController(self, controller:VideoController):
        '''Altera o Video em exibição'''
        #Altera o Switch
        self.controller = controller
        self.resize()
        #Reconfigura o menu associando ao novo controller
        self.menuPlayer.switchController(controller)

    def run(self):
        '''Main Loop'''
        try:
            self.window.mainloop()
        except Exception as e:
            # Faça o tratamento adequado da exceção, como imprimir uma mensagem de erro
            traceback.print_exc()
            print("Ocorreu um erro na thread:", e)
            

    def hasModifcation(self):
        '''Verifica se o frame foi alterado e precisa redesenhar'''
        return self.conf['last_frame'] != self.controller.getIdFrame()  
    
    def play(self):
        '''Executa o video frame a frame'''
        try:
            self.menuPlayer.attFrame()
            if self.controller.isRunning():
                self.controller.next()
            newFrame = self.pip_render.exec(self.controller)
            time = round(1/self.conf['velocidade']*20)
            self.draw( newFrame )
            self.window.after( time , self.play  )
        except Exception as e:
            traceback.print_exc()
            print(f"Ocorreu um erro na thread: {e}")

       
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
        try:
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

        except Exception as e:
            traceback.print_exc()
            cv2.destroyAllWindows()