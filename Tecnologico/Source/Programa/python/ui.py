#from asyncio import windows_events
from turtle import title
import cv2
from tkinter import *
from tkinter import filedialog
import multiprocessing as mltp
from PIL import ImageTk, Image
import os


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
        #Meta dados do video openCv
        self.video = {
            "play":True,
            "size":(0,0),
            "total_frame":0,
            "id_frame":0
        }

        #Carrega o video
        video = self.open()
        #Cria a Janela baseada nas configurações do video
        self.window = Tk()
        self.window.title( self.conf["title"] )
        self.window.configure( bg=self.conf["color"] )
        self.window.resizable( False, False )
        self.resize()
        self.canvas = Label( self.window )
        #Executa
        print(self.video)
        self.play(video)
        self.run()

    
    def play(self,video):
        #Se o video estiver em play
        if self.video['play'] :
            self.video['id_frame'] += 1
            if self.video['id_frame'] >= self.video['total_frame']:
                self.video['id_frame'] = self.video['total_frame']
                video.set(cv2.CAP_PROP_POS_FRAMES, self.video['id_frame'] - 1)
            #Altera a timeline
            #self.scale.set(self.video['id_frame'])
        #Se o video estiver pausado
        else:
            #val = self.scale.get()
            #self.video['id_frame'] = val
            #video.set(cv2.CAP_PROP_POS_FRAMES, self.video['id_frame'])
            pass

        frame = self.getFrame(video,self.video['id_frame'])
        #Desenha na janela
        self.draw(frame)

        #Vai para o proximo frame
        next = lambda : self.play(video) 
        self.window.after(20, next)





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

    def run(self):
        '''Main Loop'''
        self.window.mainloop();
        
    def pathFile(self):
        '''Seta o Path do video'''
        aux = Tk()
        currdir = os.getcwd()
        tempdir = filedialog.askopenfilename(parent=aux, initialdir=currdir, title='Selecione o Video')
        aux.destroy()
        return tempdir
    
    def open(self):
        '''Carrega o video'''
        path = self.pathFile()
        video = cv2.VideoCapture( path )
        #Seta as configurações
        self.conf['path'] = path
        self.video['size'] = (
            round(video.get(cv2.CAP_PROP_FRAME_WIDTH)),
            round(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
        )
        self.video['total_frame'] = round(video.get(cv2.CAP_PROP_FRAME_COUNT))
        return video

    def resize(self):
        w, h = self.getSizeFrame()
        self.window.geometry( str(w)+"x"+str(h) )
    
    def getSizeFrame(self):
        a = self.conf["scale"]
        bw = self.conf['bord'][0]
        bh = self.conf['bord'][1]
        w = self.video['size'][0]
        h = self.video['size'][1]
        new_w = round( (w*a)+bw*2 )
        new_h = round( (h*a)+bh*2 )
        return (new_w,new_h)

    def draw(self, img_cv):
        img_cv = cv2.resize(img_cv, self.getSizeFrame() )
        img_cv = cv2.cvtColor(img_cv, cv2.COLOR_BGRA2RGB)
        img = Image.fromarray(img_cv)
        picture = ImageTk.PhotoImage(img)
        self.canvas.configure(image=picture)
        self.canvas.image = picture
        w = self.conf['bord'][0]
        h = self.conf['bord'][1]
        self.canvas.place(x=w,y=h)
        cv2.destroyAllWindows()

    def getFrame(self, video, id):
        video.set(cv2.CAP_PROP_POS_FRAMES, id-1)
        _, frame = video.read()
        return frame





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
        
        self.label = Label(win)
        self.counter = 0
        self.key = True
        # self.display()
        mltp.Process(target=self.display())
        self.scale.bind("<ButtonPress-1>", lambda e: self.active_scaler())
        self.scale.bind("<ButtonRelease-1>", lambda e: self.active_auto())

    def to_pil(self, img):
        img = cv2.resize(img, (w,h))
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2RGB)
        image = Image.fromarray(img)
        pic = ImageTk.PhotoImage(image)
        self.label.configure(image=pic)
        self.label.image = pic
        self.label.place(x=100, y=50)
        cv2.destroyAllWindows()

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