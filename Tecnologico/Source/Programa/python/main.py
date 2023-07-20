import traceback
from typing import List
from controller.render.pipe             import PipeLine
from controller.render.renderBar        import renderBar
from controller.render.renderPose       import renderPose
from controller.render.renderTxt        import renderTxt
from controller.util.flag               import Flag
from controller.util.coloredMsg         import msg
from controller.util.progress_bar       import progress_bar
from view.ui.components.buttonSketch    import ButtonSketch
from view.ui.mainWindow                 import MainWindow

#Cria as flags
barra_flag = Flag("Barra")
eph_flag = Flag("EPH")
dados_flag = Flag("Dados")

#Seta uma Função para cada Flag
barra_flag.setFx( lambda frame, cel : renderBar(frame,cel.getLine() ) )
eph_flag.setFx( lambda frame, cel : renderPose(frame,cel.getPose() ) )
dados_flag.setFx( lambda frame, cel : renderTxt(frame,cel.getData() ) )

flags = [barra_flag, eph_flag, dados_flag]

#Cria os buttons
btns:List[ButtonSketch] = [
    ButtonSketch("EPH",eph_flag),
    ButtonSketch("Barra",barra_flag),
    ButtonSketch("Dados",dados_flag)
]

#Cria um pipeLine de Renderização
pipe_render = PipeLine()
pipe_render.addFlag(eph_flag,1)
pipe_render.addFlag(barra_flag,1)
pipe_render.addFlag(dados_flag,1)

try:
    MainWindow(btns=btns, flags=flags, preRender=pipe_render.exec)
except Exception as e:
    traceback_msg = traceback.format_exc()
    print(f"Erro: {e}")
    print(f"Traceback: {traceback_msg}")
    exit()