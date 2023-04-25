import threading
import multiprocessing as mltp
import sys
import os
import time
from typing import List, Tuple
from ui.model.videoController import VideoController
from featureExtraction.poseModel import Pose, PosePoints
from featureExtraction.objectDetector import bar
from util.flag import Flag
from util.progress_bar import progress_bar


def preProcess(controller:VideoController):
    total = controller.getTotalFrame()
    controller.setFrame(0)
    #Carrega todos os frames no Controller
    for id in range(total):
        #printa a porcentagem ja feita 
        progress_bar( round(id*100/total) ,"pose Detection")
        frame = controller.getFrameId(id)
        controller.buffer.set_cell(id,process_frame(frame))


def process_frame(frame):
    barra = None
    points = None
    frame_cp = frame.copy()
    #Extrai a barra
    try:
        barra = bar(frame_cp)
    except:
        pass

    #Extrai pose do frame
    try:
        pose = PosePoints(frame_cp)
        points = pose.getPoints()   
    except:
        pass  
    #Retorno
    struct = {
        "pose":points,
        "barra":barra
    }
        
    return struct

