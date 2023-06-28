import pdb
import math
import cv2
import numpy as np
from typing import List
from util.beep import beep
from util.flag import Flag
from util.progress_bar import progress_bar
from ui.model.buffer import Buffer
from ui.model.celulaModel import CelulaModel
from ui.model.celulaModel import CelulaModel
from ui.controller.videoController import VideoController
from featureExtraction.model.lineModel import LineModel
from featureExtraction.objectDetector import PosePoints,detectBar
from featureExtraction.model.poseModel import PoseModel,Segmento
from featureExtraction.model.contracaoModel import ContracaoModel
from featureExtraction.geometria import angle_line,angle_point,intercept,segment
from featureExtraction.deltaCalculator import DeltaCalculator

def indice_not_process(buffer:Buffer):
    '''Retorna os indices que nao foi possivel fazer a extração da imagem'''
    not_allocated = {"line":[],"pose":[]}
    for i in range(buffer.size()):
        cel:CelulaModel = buffer.get_cell(i)
        #fix Barra
        if cel.getLine() == None:
            not_allocated['line'].append(i)
        #fix Pose
        if cel.getPose() == None:
            not_allocated['pose'].append(i)
    return not_allocated

def get_range_to_analyze(buffer:Buffer,index:int):
    '''Descobre qual o range a ser analisado'''
    capacity = math.floor(buffer.get_capacity())
    offset = round(capacity/2)
    start = 0
    end = 0
    if index > offset: #Se tem n celulas antes
        start = index - offset
    else: #Se tem apenas n-x celulas antes passa x celulas para o final
        start = 0
        end = offset - index
    if index < (buffer.size() - offset ): #Se tem n celulas depois
        end = end +index + offset - 1 
    else: #Se tem apenas n-x celulas depois passa x celulas para o inicio
        end = buffer.size() - 1
        variation = offset - ( buffer.size() - 1 - index ) 
        start = index - variation
    return ( round(start),round(end) )

def preProcess(controller:VideoController, flags:List[Flag]):
    controller.setFrame(0)
    total = controller.getTotalFrame()
    angulo = 0

    for i in range(2):
        #Pega a barra em todos os frames
        for id in range(total):
            #printa a porcentagem ja feita 
            percent = round(100*(id/total))
            progress_bar(percent ,"Get barra")
            frame = controller.getFrameId(id)
            barra = getBarra(frame)
            feature = CelulaModel(None,barra,None)
            controller.buffer.set_cell(id, feature)

        #Faz inferencia quando não consegue detectar a barra
        not_allocated = indice_not_process(controller.buffer)
        for i in not_allocated['line']:
            fix_barra(controller.buffer, i)

        #Apartir da posição da barra rotaciona o frame
        barra:LineModel = fix_barra_moda(controller.buffer)
        pt1,pt2 = barra.getPoints()

        pt1 = (0, pt1[1])
        angulo = angle_point(pt1,pt2)
        for id in range(total):
            percent = round(100*(id/total))
            progress_bar(percent ,"Rotate frame")
            frame = controller.getFrameId(id)
            new_frame = rotate(frame,angulo)
            controller.setNewFrame(id,new_frame)
    #Ativa a flag da Barra
    for flag in flags:
        if flag.getName() == "Barra":
            flag.activate()
   
    #Extrai dados do frame
    for id in range(total):
        #printa a porcentagem ja feita 
        percent = round(100*(id/total))
        progress_bar(percent ,"Get pose")
        frame = controller.getFrameId(id)
        feature = process_frame(frame)
        controller.buffer.set_cell(id, feature)
    #Ativa a flag EDH
    for flag in flags:
        if flag.getName() == "EDH":
            flag.activate()
    
    barra:LineModel = fix_barra_moda(controller.buffer)
    pt1,pt2 = barra.getPoints()
    pt1 = (0, pt1[1])
    angulo = angle_point(pt1,pt2)
    process(controller)
    beep()
    #Ativa a flag Dados
    for flag in flags:
        if flag.name == "Dados":
            flag.activate()
    #Apos o termino ativa a flag para desbloquear os buttons
    finished_flag = flags[0]
    finished_flag.activate()
    finished_flag.run()

def indice_not_process(buffer:Buffer):
    '''Retorna os indices que nao foi possivel fazer a extração da imagem'''
    not_allocated = {"line":[],"pose":[]}
    for i in range(buffer.size()):
        cel:CelulaModel = buffer.get_cell(i)
        #fix Barra
        if cel.getLine() == None:
            not_allocated['line'].append(i)
        #fix Pose
        if cel.getPose() == None:
            not_allocated['pose'].append(i)
    return not_allocated

def fix_barra(buffer:Buffer, index:int):
    '''Inferencia da posição da barra'''
    start,end = get_range_to_analyze(buffer,index)
    array = buffer.get_slice((start,end), lambda data: data.getLine() )    
    extract = lambda i,j : ( lambda line: line.getPoints()[i][j] )
    getMean = lambda i,j: round(DeltaCalculator.get_mean(array, extract(i,j)))
    x1,y1,x2,y2 = getMean(0,0), getMean(0,1), getMean(1,0), getMean(1,1)
    line = LineModel(x1,y1,x2,y2)
    pose = buffer.get_cell(index).getPose()
    data = buffer.get_cell(index).getData()
    cel = CelulaModel(line=line, pose=pose, data=data)
    buffer.set_cell(index, cel)

def fix_barra_moda(buffer:Buffer):
    '''Descobre a media e resignifica a barra'''
    start,end = 0, buffer.size()
    array = buffer.get_slice((start,end), lambda data: data.getLine() )    
    extract = lambda i,j : ( lambda line: line.getPoints()[i][j] )
    getMode = lambda i,j: round(DeltaCalculator.get_mode(array, extract(i,j)))
    x1,y1,x2,y2 = getMode(0,0), getMode(0,1), getMode(1,0), getMode(1,1)

    for index in range(end):
        line = LineModel(x1,y1,x2,y2)
        pose = buffer.get_cell(index).getPose()
        data = buffer.get_cell(index).getData()
        cel = CelulaModel(line=line, pose=pose, data=data)
        buffer.set_cell(index, cel)
    
    return LineModel(x1,y1,x2,y2)

def check(controller,fx, arg, name):
    total = controller.getTotalFrame()
    controller.setFrame(0)
    for id in range(total):
        #printa a porcentagem ja feita 
        percent = round(100*(id/total))
        progress_bar(percent, name)
        frame = controller.getFrameId(id)
        feature = fx(frame)
        controller.buffer.set_cell(id, feature)

def preProcessOLD(controller:VideoController, flag:Flag):
    total = controller.getTotalFrame()
    controller.setFrame(0)
    #Carrega todos os frames no Controller
    for id in range(total):
        #printa a porcentagem ja feita 
        percent = round(100*(id/total))
        progress_bar(percent ,"pose Detection")
        frame = controller.getFrameId(id)
        feature = process_frame(frame)
        controller.buffer.set_cell(id, feature)
    process(controller)
    beep()
    #Apos o termino ativa a flag para desbloquear os buttons
    flag.activate()
    flag.run()

def process(controller:VideoController):
    check_angle(controller)
    check_gradiente(controller)

def check_angle(controller:VideoController):
    total = controller.getTotalFrame()
    #Carrega todos os frames no Controller
    for id in range(total):
        angle = angleSegments(controller,id)
        data = ContracaoModel("","","","", angle)
        cel:CelulaModel = controller.buffer.get_cell(id)
        cel.setData(data)

def check_gradiente(controller:VideoController):
    total = controller.getTotalFrame()
    #Carrega todos os frames no Controller
    for id in range(total):
        cel:CelulaModel = controller.buffer.get_cell(id)

def rotate(frame, angulo):
    # Obtém a altura e a largura da imagem
    altura, largura = frame.shape[:2]
    # Calcula o ponto central da imagem
    centro = (largura // 2, altura // 2)
    # Cria a matriz de rotação usando o ângulo e o ponto central
    matriz_rotacao = cv2.getRotationMatrix2D(centro, angulo, 1.0)
    # Aplica a transformação de rotação na imagem
    imagem_rotacionada = cv2.warpAffine(frame, matriz_rotacao, (largura, altura))
    return imagem_rotacionada

def angleSegments( controller:VideoController, id:int):
    cel:CelulaModel = controller.buffer.get_cell(id)
    pose:PoseModel = cel.getPose()
    #braço esquerdo
    braco_dir = pose.getSegmentLine(Segmento.BRACO_DIR)
    braco_esq = pose.getSegmentLine(Segmento.BRACO_ESQ)
    perna_dir = pose.getSegmentLine(Segmento.PERNA_DIR)
    perna_esq = pose.getSegmentLine(Segmento.PERNA_ESQ)
    struct_ret = {
        "braco_dir":angle_line(braco_dir[0],braco_dir[1]),
        "braco_esq":angle_line(braco_esq[0],braco_esq[1]),
        "perna_dir":angle_line(perna_dir[0],perna_dir[1]),
        "perna_esq":angle_line(perna_esq[0],perna_esq[1])
    }
    return struct_ret   

def process_frame(frame) -> CelulaModel:
    #Inicia o Frame
    frame_cp, barra, points, data =  [None]*4
    try:
        frame_cp = frame.copy()
    except:
        return CelulaModel(line=barra, pose=points, data = data)

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
    return CelulaModel(line=barra, pose=points, data = data)

def getBarra(frame) -> CelulaModel:
    """Identifica a barra no frame"""
    #Inicia o Frame
    frame_cp, barra, points, data =  [None]*4
    try:
        frame_cp = frame.copy()
        barra:LineModel = detectBar(frame_cp)
        return barra
    except:
        barra = None
        return barra
    

    '''Descobre a media e resignifica a barra'''
    start,end = 0, buffer.size()
    array = buffer.get_slice((start,end), lambda data: data.getLine() )    
    extract = lambda i,j : ( lambda line: line.getPoints()[i][j] )
    getMode = lambda i,j: round(DeltaCalculator.get_mode(array, extract(i,j)))
    x1,y1,x2,y2 = getMode(0,0), getMode(0,1), getMode(1,0), getMode(1,1)

    for index in range(end):
        line = LineModel(x1,y1,x2,y2)
        pose = buffer.get_cell(index).getPose()
        data = buffer.get_cell(index).getData()
        cel = CelulaModel(line=line, pose=pose, data=data)
        buffer.set_cell(index, cel)

def fix_pose(buffer:Buffer, index:int):
    '''Inferencia da pose'''
    start,end = get_range_to_analyze(buffer,index)
    array = buffer.get_slice((start,end), lambda data: data.getPose() )
    extract_x = lambda part: ( lambda pose: getattr(pose, f"get_{part}")()[0] )
    extract_y = lambda part: ( lambda pose: getattr(pose, f"get_{part}")()[1] )
    point = lambda part: (
       round(DeltaCalculator.get_mean(array, extract_x(part))),
       round(DeltaCalculator.get_mean(array, extract_y(part)))
    )
    parts = ["left_ankle", "left_elbow", "left_shoulder", "left_heel", "left_hip", "left_knee", "left_wrist", "right_ankle", "right_elbow", "right_shoulder", "right_heel", "right_hip", "right_knee", "right_wrist"]
    points = []
    for part in parts:
        points.append( point(part) )
     
    cel = buffer.get_cell(index)
    line = cel.getLine()
    pose = PoseModel(*points)
    data = buffer.get_cell(index).getData()
    feature = CelulaModel(line=line, pose=pose, data=data)
    buffer.set_cell(index, feature)

#END