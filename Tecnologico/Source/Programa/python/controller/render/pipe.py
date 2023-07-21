from copyreg import constructor
from typing import List, Tuple

from controller.util.flag import Flag
from controller.video.buffer import Buffer
from controller.video.videoController import VideoController
from model.video.celulaModel import CelulaModel
from copyreg import constructor
from typing import List, Tuple
from model.video.celulaModel import CelulaModel
from controller.video.videoController import VideoController
from util.flag import Flag

class PipeLine():
    
    def __init__(self):
        #Cada flag é associada a um numero que define a ordem de prioridade
        self.conf:List[Tuple[Flag,float]] = []
        

    def addFlag(self, flag:Flag , num:float=1):
        '''Adiciona a flag ao pipeLine com seu numero de prioridade'''
        if flag not in self.conf:
            self.conf.append((flag,num))

    def exec(self,controller:VideoController):
        '''Executa cada função do pipeline sobre o frame atual de acordo com a ordem '''
        #Pega as variaveis de controle
        id,frame = controller.getIdFrame(), controller.getFrame()
        if id <= controller.getTotalFrame()-1:
            frame_cp = frame.copy()
        else:
            return frame
        getState = lambda flag: flag.getState()
        activeFlags = list( filter(getState, [flag for flag,_ in self.conf] ) ) 
        orderPipe:List[Tuple[Flag,float]] = sorted(self.conf, key=lambda x: x[1])
        #Faz o processamento
        for flag,_ in orderPipe:
            if flag.getState():
                try:
                    #Executa a função com o frame e celula com os meta Dados
                    frame_cp = flag.run(frame_cp, controller.getCel(id))
                except:
                    frame_cp = controller.getFrame()
        return frame_cp
    

    def processImg(self,frame, cel:CelulaModel):
        '''Executa cada função do pipeline sobre o frame atual de acordo com a ordem '''
        frame_cp = frame.copy()
        orderPipe:List[Tuple[Flag,float]] = sorted(self.conf, key=lambda x: x[1])
        #Faz o processamento
        for flag,_ in orderPipe:
            if flag.getState():
                try:
                    #Executa a função com o frame e celula com os meta Dados
                    frame_cp = flag.run(frame_cp, cel)
                    frame_cp = frame_cp.copy()
                except:
                    frame_cp = frame_cp

        return frame_cp
