from typing import List
import cv2
from ui.ux import Ux
from ui.model.buttonSketch import ButtonSketch
from util.flag import Flag

#Cria as flags
edh_flag = Flag("EDH",lambda : None)
barra_flag = Flag("Barra",lambda : None)

#Cria os buttons
btns:List[ButtonSketch] = [
    ButtonSketch("EDH",edh_flag),
    ButtonSketch("Barra",barra_flag)
]

Ux(btns=btns)