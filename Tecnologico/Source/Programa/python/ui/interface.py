from player import PlayerWin
from controllerVideo import ControllerVideo


def getPath():
    '''Seta o Path do video'''
    aux = Tk()
    currdir = os.getcwd()
    path = filedialog.askopenfilename(parent=aux, initialdir=currdir, title='Selecione o Video')
    aux.destroy()
    return path


class UI():
    
    def __init__(self):
        self.path = "/home/guest/Área de Trabalho/TCC/Tecnologico/Source/Programa/python/midia/c.mp4" #getPath()
        self.controller = ControllerVideo(path=self.path)
        self.player = PlayerWin(self.controller)

        self.player.switchController(ControllerVideo(path=getPath()))
        self.player.switchController(ControllerVideo(path=getPath()))
        
        #Persiste o Player
        self.player.run()
        