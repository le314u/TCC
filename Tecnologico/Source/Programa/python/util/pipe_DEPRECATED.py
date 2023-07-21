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
            cel_meta = controller.getMeta(id)
            self.processImg(frame_cp,cel_meta)
        else:
            return frame
        

   
