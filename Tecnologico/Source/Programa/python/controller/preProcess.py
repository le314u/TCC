import cv2
import math
import numpy as np
import traceback
from typing import List
from controller.featureExtraction.deltaCalculator import DeltaCalculator
from controller.featureExtraction.geometria import angle_line, angle_point, intercept, segment, inclinacao_reta, rotate_segment
from controller.featureExtraction.objectDetector import PosePoints, detectBar
from controller.processImg.debug import save_img, display_img, display_imgs
from controller.processImg.filter import limiarizacao, pixelizacao, imagem_cinza, suavizacao, rotacao
from controller.processImg.mask import Mask
from controller.util.beep import beep
from controller.util.coloredMsg import msg
from controller.util.flag import Flag, enable_flag, disable_flag
from controller.util.progress_bar import progress_bar
from controller.video.buffer import Buffer
from controller.video.videoController import VideoController
from model.AFD.charAFD import charAFD
from model.featureExtraction.dataModel import DataModel
from model.featureExtraction.lineModel import LineModel
from model.featureExtraction.poseModel import PoseModel, Segmento
from model.video.celulaModel import CelulaModel


MASK = Mask()



def preProcess(controller:VideoController, flags:List[Flag]):
        #Inicia o Buffer para que possa usar a função check
        start_check(controller)
        msg("\r"+"Buffer inicializado")

        #Detecção da Barra
        check(controller,check_barra,"get Barra")
        msg("\r"+"detecção da Barra")

        #Faz inferencia quando não consegue detectar a barra
        not_allocated = indice_not_process(controller.buffer)
        for i in not_allocated['line']:
            fix_barra(controller.buffer, i)
        msg("\r"+"Inferencia da Barra")
        #Pega a predominancia da posição da barra
        tendency_barra_moda(controller.buffer)
        msg("\r"+"Predominancia da Barra")

        
        # #Rotaciona o frame de acordo com a Barra
        # check(controller,check_inclination,"rotaciona")
        # att_frames(controller)
        # msg("\r"+"Rotação")

        # enable_flag(flags,"Barra")

        # #Estimativa de pose Humana
        # check(controller,check_edh,"Estimativa de pose")
        # msg("\r"+"Pose")
        # enable_flag(flags,"EDH")    
        
        # check(controller,check_data,"meta Dados")
        # msg("\r"+"meta data and display data")

        beep()


        # check(controller,check_AFD,"char AFD")
        # msg("\r"+"Transpilação alfabeto AFD")
        

        enable_flag(flags,"Dados")

def indice_not_process(buffer:Buffer):
    '''Retorna os indices que nao foi possivel fazer a extração da imagem'''
    not_allocated = {"line":[],"pose":[]}
    print("Indices que nao foi possivel fazer a extração da imagem")
    print(not_allocated)
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
    cel:CelulaModel = buffer.get_cell(index)
    cel.setLine(line)


    
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
    
    cel = buffer.get_cell(index).get()
    cel.setPose( PoseModel(*points) )

def tendency_barra_moda(buffer:Buffer):
    '''Descobre a media e resignifica a barra'''
    start,end = 0, buffer.size()
    array = buffer.get_slice((start,end), lambda data: data.getLine() )    
    extract = lambda i,j : ( lambda line: line.getPoints()[i][j] )
    getMode = lambda i,j: round(DeltaCalculator.get_mode(array, extract(i,j)))
    x1,y1,x2,y2 = getMode(0,0), getMode(0,1), getMode(1,0), getMode(1,1)

    for index in range(end):
        line = LineModel(x1,y1,x2,y2)
        cel:CelulaModel = buffer.get_cell(index)
        cel.setLine(line)
    
    return LineModel(x1,y1,x2,y2)

def att_frames(controller:VideoController):
    '''Transfere os frames de cada celula para controller'''
    try:
        controller.gotoFrame(0)
        total = controller.getTotalFrame()
        #Pega a barra em todos os frames
        for id in range(total):
            #printa a porcentagem ja feita 
            percent = round(100*(id/total))
            progress_bar(percent ,"Att Frames")
            cel = controller.buffer.get_cell(id)
            frame = cel.getFrame()
            controller.setFrame(id,frame)
    except Exception as e:
        traceback_msg = traceback.format_exc()
        print(f"Erro: {e}")
        print(f"Traceback: {traceback_msg}")

def start_check(controller:VideoController):
    try:
        controller.gotoFrame(0)
        total = controller.getTotalFrame()
        #Pega a barra em todos os frames
        for id in range(total):
            #printa a porcentagem ja feita 
            percent = round(100*(id/total))
            progress_bar(percent ,"Iniciando Buffer")
            data = DataModel()
            data.set("id",id)
            frame = controller.getFrameId(id)
            cel = CelulaModel(data=data,frame=frame)
            controller.buffer.set_cell(id, cel)                
    except Exception as e:
        traceback_msg = traceback.format_exc()
        print(f"Erro: {e}")
        print(f"Traceback: {traceback_msg}")

def check(controller:VideoController,verify_fx:callable, name:str):
    """Roda os verify em todos os frames do buffer"""
    total = controller.getTotalFrame()
    controller.gotoFrame(0)
    for id in range(total):
        #printa a porcentagem ja feita 
        percent = round(100*(id/total))
        progress_bar(percent, name)
        cel:CelulaModel = controller.buffer.get_cell(id)
        verify_fx(cel)

def check_barra(cel:CelulaModel):
    '''Para cada frame Extrai a barra'''
    frame = MASK.putMask(cel.getFrame(), MASK.getMask())
    try:
        barra:LineModel = detectBar(frame)
    except:
        barra = None
    cel.setLine(barra)

def check_inclination(cel:CelulaModel):
    '''Apartir da inclinação da barra rotaciona o frame'''

    #Calcula a inclinação
    barra:LineModel = cel.getLine()
    pt1_origin,pt2_origin = barra.getPoints()
    angulo = inclinacao_reta(pt1_origin,pt2_origin)

    #Salva o grau de inclinação
    data = cel.getData()
    data.set("angulo",angulo)

    #Rotaciona o Frame
    new_frame = rotacao(cel.getFrame(),angulo)
    cel.setFrame(new_frame)

    #Rotaciona a Barra
    p1,p2 = rotate_segment(pt1_origin,pt2_origin,-angulo)
    newBarra:LineModel = LineModel(*p1,*p2)
    cel.setLine(newBarra)

def check_edh(cel:CelulaModel):
    frame = cel.getFrame()
    posePoints:PosePoints = PosePoints(frame)
    pose:PoseModel = posePoints.getPose()   
    cel.setPose(pose)

def check_AFD(cel:CelulaModel):
    m = charAFD(cel_meta=cel)

def check_data(cel: CelulaModel):
    pose: PoseModel = cel.getPose()  # Obtém o objeto de pose da célula

    # Obtém as linhas dos segmentos do corpo (braços e pernas) da pose
    braco_dir = pose.getSegmentLine(Segmento.BRACO_DIR)
    braco_esq = pose.getSegmentLine(Segmento.BRACO_ESQ)
    perna_dir = pose.getSegmentLine(Segmento.PERNA_DIR)
    perna_esq = pose.getSegmentLine(Segmento.PERNA_ESQ)

    # Calcula os ângulos das linhas dos segmentos do corpo
    struct_angulo = {
        "angulo_braco_dir": angle_line(braco_dir[0], braco_dir[1]),
        "angulo_braco_esq": angle_line(braco_esq[0], braco_esq[1]),
        "angulo_perna_dir": angle_line(perna_dir[0], perna_dir[1]),
        "angulo_perna_esq": angle_line(perna_esq[0], perna_esq[1])
    }

    # Cria um objeto DataModel com os ângulos e outras informações
    data = cel.getData()
    data.setAngulo(**struct_angulo)

#END