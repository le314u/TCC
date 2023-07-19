from typing import Callable

class Flag:
    def __init__(self, name:str, function:Callable=(lambda :None), state:bool=False):
        self.name = name
        self.state = state
        self.function = function

    def __str__(self):
        state =  "ativa" if self.state else "inativa"
        return f"{self.name} : {state}"

    def activate(self):
        self.state = True

    def deactivate(self):
        self.state = False
    
    def alternate(self):
        self.state = not self.state
       
    def setFx(self,fx:Callable):
        self.function = fx
    
    def getState(self):
        return self.state

    def getName(self):
        return self.name

    def run(self, *args):
        if len(args) > 0:
            return self.function(*args)
        else:
            return self.function()    
        
def enable_flag(flags:Flag, flag_name):
    '''Passa por uma lista de Flags e ativa a flag que der match com name'''
    for flag in flags:
        if flag.getName() == flag_name:
            flag.activate()

def disable_flag(flags:Flag, flag_name):
    '''Passa por uma lista de Flags e desativa a flag que der match com name'''
    for flag in flags:
        if flag.getName() == flag_name:
            flag.deactivate()
