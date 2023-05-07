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

    def name(self):
        return self.name

    def run(self, arg = None):
        return self.function(arg) if arg is not None else self.function()
    
    