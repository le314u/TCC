import sys
import os
from typing import List, Tuple

from util.flag import Flag
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from ui.model.buttonSketch import ButtonSketch

class ButtonsPlayer():
    def __init__(self, name_flag:List[Tuple[str,Flag]]):
        self.sketchs:List[ButtonSketch]
        for name,flag in name_flag:
            self.sketchs.append(name,flag)

    def get(self):
        return self.sketchs