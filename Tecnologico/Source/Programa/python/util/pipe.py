import sys
import os
from typing import List, Tuple
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from dec_time import TIME
from util.flag import Flag


class PipeLine():
    
    def __init__(self):
        #Cada flag é associada a um numero que define a ordem de prioridade
        self.conf:List[(Flag,float)]
        

    def addFlag(self, flag:Flag , num:float=1):
        '''Adiciona a flag ao pipeLine com seu numero de prioridade'''
        if flag not in self.conf:
            self.conf.append((flag,num))

    def exec(self,frame):
        '''Executa cada função do pipeline sobre o frame atual de acordo com a ordem '''
        active = lambda x: x.state()
        activeFlags = list( filter(active, self.conf) )
        orderPipe:List[Tuple[Flag,float]] = sorted(activeFlags, key=lambda x: x[1])
        for flag,_ in orderPipe:
            if flag.state():
                frame = flag.run(frame)
        return frame