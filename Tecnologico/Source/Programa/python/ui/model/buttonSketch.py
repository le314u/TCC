from functools import partial
from typing import Callable
from util.flag import Flag
from util.pipe import PipeLine

class ButtonSketch():
    def __init__(self, text:str, flag:Flag, pipeLine:PipeLine=None):
        #Add ao processamento
        if pipeLine is not None:
            pipeLine.addFlag(flag)
        #associa uma função ao button
        self.fx = lambda:flag.alternate()
        self.text = text
        self.flag = flag
    def get(self):
        return (self.text,self.fx,self.flag)