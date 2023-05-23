from models.celulaModel import CelulaModel
from featureExtraction.objectDetector import PosePoints,detectBar
from featureExtraction.poseModel import PoseModel
from featureExtraction.lineModel import LineModel
from util.beep import beep
from util.flag import Flag
from util.progress_bar import progress_bar
from ui.model.videoController import VideoController
import cv2
import numpy as np

def preProcess(controller:VideoController, flag:Flag):
    total = controller.getTotalFrame()
    controller.setFrame(0)
    #Carrega todos os frames no Controller
    for id in range(total):
        #printa a porcentagem ja feita 
        progress_bar( round(100*id/total) ,"pose Detection")
        frame = controller.getFrameId(id)
        feature = process_frame(frame)
        controller.buffer.set_cell(id, feature )
    beep()
    #Apos o termino ativa a flag para desbloquear os buttons
    flag.activate()
    flag.run()


def process_frame(frame) -> CelulaModel:
    #Inicia o Frame
    frame_cp, barra, points =  [None]*3
    try:
        frame_cp = frame.copy()
    except:
        return CelulaModel(line=barra, pose=points)

    #Extrai a barra
    try:
        barra:LineModel = detectBar(frame_cp)
    except:
        barra = None

    #Extrai pose do frame
    try:
        pose:PosePoints = PosePoints(frame_cp)
        points:PoseModel = pose.getPose()   
    except:
        points = None

    #retorno
    return CelulaModel(line=barra, pose=points)


