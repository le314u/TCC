#from asyncio import windows_events
from turtle import title
import cv2
from tkinter import *
from tkinter import filedialog
import multiprocessing as mltp
from PIL import ImageTk, Image
import os
from  controllerVideo import ControllerVideo

class Ui():
    def __init__(self):
        #Meta dados da Janela Tkinter
        self.conf = {
            "title":"TCC - Lucas Mateus Fernandes",
            "path":"",
            "scale":0.25,
            "bord":(0,0),
            "color":"gray17",
        }


        #Carrega o path video
        path = self.getPath()
        #Carrega o Video
        self.controller = ControllerVideo(path)
        #Cria a Janela baseada nas configurações do video
        self.window = Tk()
        self.window.title( self.conf["title"] )
        self.window.configure( bg=self.conf["color"] )
        self.window.resizable( False, False )
        self.resize()
        self.canvas = Label( self.window )

        #Executa
        self.controller.play()
        mltp.Process(target=self.play())
        self.run()
     
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
        if self.controller.isRunning():
            self.controller.next()
            frame =  self.controller.getFrame() 
            self.draw( frame )
            self.window.after(20, self.play  )
        else:
            self.controller.restart()
            self.window.after(20, self.play  )

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
        '''Desenha o frame no Player'''
        frame_cv = cv2.resize(frame_cv, self._getSizeFrame() )
        frame_cv = cv2.cvtColor(frame_cv, cv2.COLOR_BGRA2RGB)
        img = Image.fromarray(frame_cv)
        picture = ImageTk.PhotoImage(img)
        self.canvas.configure(image=picture)
        self.canvas.image = picture
        w, h  = self.conf['bord']
        self.canvas.place(x=w,y=h)
        cv2.destroyAllWindows()


class Control():
    def __init__(self):
        max_val = cap.get(cv2.CAP_PROP_FRAME_COUNT)
        var = DoubleVar()

        self.play = Button(win, text ="PLAY")
        self.play.place(x=100, y=0, width=w)
        self.play.bind("<ButtonPress-1>", lambda e: self.run())

        self.scale = Scale(win, from_=0, to=max_val - 1, orient=HORIZONTAL,variable=var,bg="gray17",fg="white", activebackground='#339999')
        self.scale.set(0)
        self.scale.place(x=100, y=h+50, width=w)
        
        #self.label = Label(win)
        self.counter = 0
        self.key = True
        # self.display()
        mltp.Process(target=self.display())
        self.scale.bind("<ButtonPress-1>", lambda e: self.active_scaler())
        self.scale.bind("<ButtonRelease-1>", lambda e: self.active_auto())

    def to_pil(self, img):
        #img = cv2.resize(img, (w,h))
        #img = cv2.cvtColor(img, cv2.COLOR_BGRA2RGB)
        #image = Image.fromarray(img)
        #pic = ImageTk.PhotoImage(image)
        #self.label.configure(image=pic)
        #self.label.image = pic
        #self.label.place(x=100, y=50)
        #cv2.destroyAllWindows()
        pass

    def active_auto(self):
        self.key = True

    def active_scaler(self):
        self.key = False
    
    def run(self):
        self.key = not self.key

    def display(self):
        if self.key == True:
            self.counter += 1
            if self.counter >= max_val:
                self.counter = max_val
                cap.set(cv2.CAP_PROP_POS_FRAMES, self.counter - 1)
            self.scale.set(self.counter)
        else:
            val = self.scale.get()
            self.counter = val
            cap.set(cv2.CAP_PROP_POS_FRAMES, self.counter)
        _, frame = cap.read()
        self.to_pil(frame)
        win.after(20, self.display)





Ui()

#cap.release()