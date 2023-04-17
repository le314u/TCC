from functools import partial
from typing import Callable
from processImg.process import Process


class Buttons():
    def __init__(self, name:str, f:Callable):
        self.name = name
        self.f = f

    def get(self):
        return (self.name,self.f)

def newButton(process:Process, name, flag) -> Buttons: 
    '''Cria um botao com uma função que altera a Flag'''
    process.addFlag(flag)
    #função que altera a Flag
    def toggle(flag):
        process.flags[flag] = not process.flags[flag]
    #cria um parcial  ou seja:        f = lambda : toggle(flag)
    f = partial(toggle, flag)
    return Buttons(name, f)