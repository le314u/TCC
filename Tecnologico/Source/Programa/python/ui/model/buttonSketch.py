from functools import partial
from typing import Callable
from util.flag import Flag
from util.pipe import PipeLine

class ButtonSketch():
    def __init__(self, text:str, flag:Flag, pipeLine:PipeLine=None):
        if pipeLine is not None:
            pipeLine.addFlag(flag)
        self.text = text
        self.f = lambda:flag.alternate()

    def get(self):
        return (self.text,self.f)