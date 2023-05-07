from typing import List
import cv2
from render.renderBar import renderBar
from render.renderPose import renderPose
from ui.ux import Ux
from ui.model.buttonSketch import ButtonSketch
from util.flag import Flag
from util.pipe import PipeLine

#Cria as flags
barra_flag = Flag("Barra")
barra_flag.setFx( lambda frame, cel : renderBar(frame,cel.getBarra() ) )

edh_flag = Flag("EDH")
edh_flag.setFx( lambda frame, cel : renderPose(frame,cel.getPose() ) )


#Cria um pipeLine de Renderização
pipe_render = PipeLine()
pipe_render.addFlag(edh_flag,1)
pipe_render.addFlag(barra_flag,1)



#Cria os buttons
btns:List[ButtonSketch] = [
    ButtonSketch("EDH",edh_flag),
    ButtonSketch("Barra",barra_flag)
]

Ux(btns=btns, preRender=pipe_render.exec)