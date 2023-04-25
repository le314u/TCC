from typing import Callable

class Flag:
    def __init__(self, name:str, function:Callable):
        self.name = name
        self.function = function
        self.active = False

    def activate(self):
        self.active = True

    def deactivate(self):
        self.active = False
    
    def alternate(self):
        self.active = not self.active
    
    def state(self):
        return self.active

    def run(self, arg = None):
        return self.function(arg) if arg is not None else self.function()

