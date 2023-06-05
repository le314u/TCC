from copyreg import constructor
from typing import List, Tuple
from ui.model.buffer import Buffer
from ui.controller.videoController import VideoController
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
                    frame_cp = flag.run(frame_cp, controller.getMeta(id))
                except:
                    frame_cp = controller.getFrame()
        return frame_cp
