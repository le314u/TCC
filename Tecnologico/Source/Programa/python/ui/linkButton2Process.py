import sys
import os
from functools import partial

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from ui.player.buttonsModel import newButton
from processImg.process import Process




class ButtonsPlayer():
    def __init__(self, process:Process = None) -> None:
        self.btns = [
            newButton(process,"EDH","poseDetection"),
            newButton(process,"Barra","barra"),
        ]
    def get(self):
        return self.btns