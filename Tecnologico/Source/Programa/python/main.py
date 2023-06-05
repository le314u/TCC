from typing import List
import cv2
from render.renderBar import renderBar
from render.renderPose import renderPose
from render.renderTxt import renderTxt
from ui.view.mainWindow import MainWindow
from ui.model.buttonSketch import ButtonSketch
from util.flag import Flag
from util.pipe import PipeLine

#Cria as flags
barra_flag = Flag("Barra")
barra_flag.setFx( lambda frame, cel : renderBar(frame,cel.getLine() ) )

edh_flag = Flag("EDH")
edh_flag.setFx( lambda frame, cel : renderPose(frame,cel.getPose() ) )

dados_flag = Flag("Dados")
dados_flag.setFx( lambda frame, cel : renderTxt(frame,cel.getData() ) )


#Cria um pipeLine de Renderização
pipe_render = PipeLine()
pipe_render.addFlag(edh_flag,1)
pipe_render.addFlag(barra_flag,1)
pipe_render.addFlag(dados_flag,1)



#Cria os buttons
btns:List[ButtonSketch] = [
    ButtonSketch("EDH",edh_flag),
    ButtonSketch("Barra",barra_flag),
    ButtonSketch("Dados",dados_flag)
]

MainWindow(btns=btns, preRender=pipe_render.exec)