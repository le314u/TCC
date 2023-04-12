#from asyncio import windows_events
from turtle import title
import cv2
from tkinter import *
from tkinter import filedialog
import multiprocessing as mltp
from PIL import ImageTk, Image
import os
from  controllerVideo import ControllerVideo

class Player():
    def __init__(self):
        #Meta dados da Janela Tkinter
        self.conf = {
            "title":"TCC - Lucas Mateus Fernandes",
            "path":"",
            "scale":0.25,
            "bord":(0,0),
            "color":"gray17",
            "last_frame":-1,
            "velocidade":0.25
        }


        #Carrega o path video
        path = self.getPath()
        #Carrega o Video
        self.controller = ControllerVideo(path)
        #Da Play no Video
        self.controller.play()

        #Cria a Janela baseada nas configurações do video
        self.window = Tk()
        self.window.title( self.conf["title"] )
        self.window.configure( bg=self.conf["color"] )
        self.window.resizable( False, False )
        self.resize()
        self.canvas = Label( self.window )

        self.controllerPlayer = ControllerPlayer(self.controller)

        
        #Linka o Player e o ControllerPlayer para fecharem juntas
        player = self.window
        control = self.controllerPlayer.window
        on_close = lambda: (player.destroy(), control.destroy())
        player.protocol("WM_DELETE_WINDOW", on_close)
        control.protocol("WM_DELETE_WINDOW", on_close)
        
        #Cria uma tred para desenhar
        mltp.Process(target=self.play())
        self.run()
    
    def hasModifcation(self):
        '''Verifica se o frame foi alterado e precisa redesenhar'''
        return self.conf['last_frame'] != self.controller.getIdFrame()  

    def getPath(self):
        '''Seta o Path do video'''
        aux = Tk()
        currdir = os.getcwd()
        path = filedialog.askopenfilename(parent=aux, initialdir=currdir, title='Selecione o Video')
        aux.destroy()
        self.conf['path'] = path
        return path
    
    def play(self):
        '''Desenha o video no Canvas'''

        self.controllerPlayer.attSlider()

        if self.controller.isRunning():
            self.controller.next()
        frame =  self.controller.getFrame() 
        self.draw( frame )
        self.window.after( round(1/self.conf['velocidade']*20) , self.play  )

    def run(self):
        '''Main Loop'''
        self.window.mainloop();
       
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
            frame_cv = cv2.resize(frame_cv, self._getSizeFrame() )
            frame_cv = cv2.cvtColor(frame_cv, cv2.COLOR_BGRA2RGB)
            img = Image.fromarray(frame_cv)
            picture = ImageTk.PhotoImage(img)
            self.canvas.configure(image=picture)
            self.canvas.image = picture
            w, h  = self.conf['bord']
            self.canvas.place(x=w,y=h)
            cv2.destroyAllWindows()
            

class ControllerPlayer():
    def __init__(self, controller=None):
        self.controller =  controller 
        self.conf = {
            "title":"Controlador",
            "scale":0.25,
            "bord":(0,0),
            "color":"gray17",
        }

        #Cria a Janela a ser usada como controlador do Player
        self.window = Tk()
        self.window.title( self.conf["title"] )
        self.window.configure( bg=self.conf["color"] )
        self.window.geometry("600x100")
        #self.window.resizable( False, False )

        win = self.window


        self.playButton = Button(win, text ="PLAY")
        self.playButton.place(x=50, y=0, width=50)
        self.playButton.bind("<ButtonPress-1>", lambda e: self.alter())
        
        var = DoubleVar()
        self.frameSlider = Scale(win, from_=0, to=self.controller.getTotalFrame() - 1, orient=HORIZONTAL,variable=var,bg="gray17",fg="white", activebackground='#339999')
        self.frameSlider.set(0)
        self.frameSlider.place(x=50, y=50, width=500)
        
        #Funções Frame Slider
        self.frameSlider.bind("<ButtonPress-1>", lambda e: self.active_scaler())
        self.frameSlider.bind("<ButtonRelease-1>", lambda e: self.active_auto())


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

    def active_auto(self):
        '''Quando clicado'''
        self.controller.play()

    def active_scaler(self):
        '''Quando Segurado'''
        self.controller.pause()

    def alter(self):
        '''Altera entre Play/Pause'''
        if(self.controller.isRunning()):
            self.controller.pause()
        else:
            self.controller.play()

    


Player()

#cap.release()