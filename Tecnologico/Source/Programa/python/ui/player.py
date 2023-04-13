import sys
import os
import cv2
from tkinter import *
from tkinter import filedialog
import multiprocessing as mltp
from PIL import ImageTk, Image
from ui import controllerVideo

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from  ui.controllerVideo import ControllerVideo


def getPath():
    '''Seta o Path do video'''
    aux = Tk()
    currdir = os.getcwd()
    path = filedialog.askopenfilename(parent=aux, initialdir=currdir, title='Selecione o Video')
    aux.destroy()
    return path

class PlayerWin():
    def __init__(self,controller):
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

        #Carrega o Video
        self.controller = controller

        #Cria a Janela baseada nas configurações do video
        self.window = Tk()
        self.window.title( self.conf["title"] )
        self.window.configure( bg=self.conf["color"] )
        self.window.resizable( False, False )
        self.resize()
        self.canvas = Label( self.window )

        self.menuPlayer = MenuPlayerWin(self.controller)

        
        #Linka o Player e o ControllerPlayer para fecharem juntas
        player = self.window
        menu = self.menuPlayer.window
        on_close = lambda: (player.destroy(), menu.destroy())
        menu.protocol("WM_DELETE_WINDOW", on_close)
        player.protocol("WM_DELETE_WINDOW", on_close)
        
        #Cria uma tred para desenhar
        mltp.Process(target=self.play())
    
    def switchController(self, controller):
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
            frame_cv = cv2.resize(frame_cv, self._getSizeFrame() )
            frame_cv = cv2.cvtColor(frame_cv, cv2.COLOR_BGRA2RGB)
            img = Image.fromarray(frame_cv)
            picture = ImageTk.PhotoImage(img)
            self.canvas.configure(image=picture)
            self.canvas.image = picture
            w, h  = self.conf['bord']
            self.canvas.place(x=w,y=h)
            cv2.destroyAllWindows()
            
class MenuPlayerWin():
    
    def __init__(self, controller):
        self.controller = controller 
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


    
        

    def switchController(self, controller):
        self.controller = controller
        self.slider2Frame()
        self.confSlider()

    def confSlider(self):
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

class UI():
    def __init__(self):
        self.path = getPath()
        self.controller = ControllerVideo(path=self.path)
        self.player = PlayerWin(self.controller)

        self.player.switchController(ControllerVideo(path=getPath()))
        self.player.switchController(ControllerVideo(path=getPath()))
        #Persiste o Player
        self.player.run()

