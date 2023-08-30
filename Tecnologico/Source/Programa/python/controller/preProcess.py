import cv2
import math
import sys
import numpy as np
import traceback
from typing import List
from controller.featureExtraction.deltaCalculator import DeltaCalculator
from controller.featureExtraction.geometria import angle_line, angle_point, intercept, segment, inclinacao_reta, rotate_segment
from controller.featureExtraction.objectDetector import PosePoints,detectBar,verify_maoBarra,verify_extensaoCotovelo,verify_ultrapassarBarra
from controller.processImg.debug import display_img,resize
from controller.processImg.filter import limiarizacao, pixelizacao, imagem_cinza, suavizacao, rotacao
from controller.processImg.mask import Mask
from controller.util.beep import beep
from controller.util.coloredMsg import msg
from controller.util.flag import Flag, enable_flag, disable_flag
from controller.util.progress_bar import progress_bar
from controller.video.buffer import Buffer
from controller.video.videoController import VideoController
from model.AFD.AFD import Cel2Char, Char, Machine, create_AFD, possibleChar
from model.featureExtraction.dataModel import DataModel
from model.featureExtraction.lineModel import LineModel
from model.featureExtraction.poseModel import PoseModel, Segmento
from model.video.celulaModel import CelulaModel
from util.decorators import memory_usage, timed

from controller.render.renderBar import renderBar


MASK = Mask()
THREAD = {"thread_controller":True}
AFD = create_AFD()

def enable_button(flags,flag_name):
        try:
            enable_flag(flags,flag_name)
            #Triga a Flag Processed para Atualizar os buttons ativos e inativos
            disable_flag(flags,"Processed")
            enable_flag(flags,"Processed")
        except:
            pass

def preProcess(controller:VideoController, flags:List[Flag], thread_controller):
    global THREAD 
    THREAD = thread_controller
    total = controller.getTotalFrame()
    controller.restart()

    if(True):
        for id in range(total):
            #printa a porcentagem ja feita 
            percent = round(100*(id/total))
            progress_bar(percent, "process")
            if(THREAD['thread_controller']):
                cel:CelulaModel = controller.buffer.get_cell(id)
                try:
                    process_cel(cel)
                except:
                    print(f"erro no frame {id}")

            else:
                print(f"erro no frame {id}")
                return
        enable_button(flags,"Dados")
        enable_button(flags,"Barra")
        enable_button(flags,"EPH")    
        enable_button(flags,"SaveF")
    else:
        stepBystep(controller, flags, thread_controller)

def process_cel(cel:CelulaModel):
    verify_barra(cel)
    fix_barra(cel) #Garante uma barra mais suave sem mudançar bruscas
    verify_inclination(cel) #
    verify_eph(cel)    
    verify_angle_member(cel)    
    verify_mao_barra(cel)    
    verify_meta_extensao(cel)    
    verify_char_AFD(cel)    
    verify_AFD(cel)
    

def stepBystep(controller:VideoController, flags:List[Flag], thread_controller):
    global THREAD 
    THREAD = thread_controller

    def enable_button(flag_name):
        try:
            enable_flag(flags,flag_name)
            #Triga a Flag Processed para Atualizar os buttons ativos e inativos
            disable_flag(flags,"Processed")
            enable_flag(flags,"Processed")
        except:
            pass

    try:
        init_tab = ""
        enable_button("Dados")

        
        #Detecção da Barra
        check(controller,verify_barra,"get Barra")
        msg(f"{init_tab} detecção da Barra")
        #Faz inferencia quando não consegue detectar a barra
        not_allocated = indice_not_process(controller.buffer)
        for i in not_allocated['line']:
            fix_barras(controller.buffer, i)
        msg(f"{init_tab} Inferencia da Barra")
        #Pega a predominancia da posição da barra
        tendency_barra_moda(controller.buffer)
        msg(f"{init_tab} Predominancia da Barra")
        #Rotaciona o frame de acordo com a Barra
        check(controller,verify_inclination,"rotaciona")
        msg(f"{init_tab} Rotação")
        enable_button("Barra")

    
        # Estimativa de pose Humana
        check(controller,verify_eph,"Estimativa de pose")
        msg(f"{init_tab} Pose")
        enable_button("EPH")    

       
        # Meta Dado para Transpilação do Alfabeto
        check(controller,verify_angle_member,"meta Dados")
        check(controller,verify_mao_barra,"mão na barra")
        check(controller,verify_meta_extensao,"extensao cotovelo")
        # Transpilação Alfabeto AFD
        check(controller,verify_char_AFD,"char AFD")
        msg(f"{init_tab} Transpilação alfabeto AFD")
        # Processamento Alfabeto AFD
        check(controller,verify_AFD,"char AFD")
        msg(f"{init_tab} Processamento AFD")


        enable_button("SaveF")
        beep()


    except Exception as e:
        print(f"\n{e}")


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

def fix_barras(buffer:Buffer, index:int):
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

def start_check(controller:VideoController):
    try:
        controller.rebobina
        total = controller.getTotalFrame()
        #Pega a barra em todos os frames
        for id in range(total):
            #printa a porcentagem ja feita 
            percent = round(100*(id/total))
            progress_bar(percent ,"Iniciando Buffer")
            data = DataModel()
            data.set("id",id)
            frame = controller.getFrameById(id)
            cel = CelulaModel(data=data,frame=frame)
            controller.buffer.set_cell(id, cel)                
    except Exception as e:
        traceback_msg = traceback.format_exc()
        print(f"Erro: {e}")
        print(f"Traceback: {traceback_msg}")

@timed
@memory_usage
def check(controller:VideoController,verify_fx:callable, name:str):
    """Roda os verify em todos os frames do buffer"""
    total = controller.getTotalFrame()
    controller.restart()
    for id in range(total):
        #printa a porcentagem ja feita 
        percent = round(100*(id/total))
        progress_bar(percent, name)
        cel:CelulaModel = controller.buffer.get_cell(id)
        verify_fx(cel)
        if(not THREAD["thread_controller"]):
            raise Exception(
                f"thread_controller : False.... thread desligada\n"
                f"pre processamento {name} incompleto\n"
            )
    print("\n")

def verify_barra(cel:CelulaModel):
    '''Para cada frame Extrai a barra'''
    barra = None
    try:
        frame = MASK.putMask(cel.getFrame(), MASK.getMask())
        barra:LineModel = detectBar(frame)
        cel.setAggregate("last_bar",barra)
    except:
        barra = cel.getAggregate("last_bar")
    cel.setLine(barra)

def verify_inclination(cel:CelulaModel):
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

def verify_eph(cel:CelulaModel):
    '''Para cada frame Extrai a pose EPH - Estimativa de pose Humana'''
    try:
        frame = cel.getFrame()
        posePoints:PosePoints = PosePoints(frame)
        pose:PoseModel = posePoints.getPose()  
        pose.position_hand()
        cel.setPose(pose)
    except:
        cel.setPose(None)

def verify_angle_member(cel: CelulaModel):
    '''Define angulo pernas e braço'''
    try:
        pose: PoseModel = cel.getPose()  # Obtém o objeto de pose da célula

        # Obtém as linhas dos segmentos do corpo (braços e pernas) da pose
        braco_dir = pose.getSegmentLine(Segmento.BRACO_DIR)
        braco_esq = pose.getSegmentLine(Segmento.BRACO_ESQ)
        perna_dir = pose.getSegmentLine(Segmento.PERNA_DIR)
        perna_esq = pose.getSegmentLine(Segmento.PERNA_ESQ)

        # Calcula os ângulos das linhas dos segmentos do corpo
        struct_angulo = {
            "angulo_braco_dir": round(angle_line(braco_dir[0], braco_dir[1]),2) ,
            "angulo_braco_esq": round(angle_line(braco_esq[0], braco_esq[1]),2) ,
            "angulo_perna_dir": round(angle_line(perna_dir[0], perna_dir[1]),2) ,
            "angulo_perna_esq": round(angle_line(perna_esq[0], perna_esq[1]),2) 
        }

        # Cria um objeto DataModel com os ângulos e outras informações
        data = cel.getData()
        data.setAngulo(**struct_angulo)
    except:
        struct_angulo = {
            "angulo_braco_dir": 0 ,
            "angulo_braco_esq": 0 ,
            "angulo_perna_dir": 0 ,
            "angulo_perna_esq": 0 
        }

def verify_mao_barra(cel:CelulaModel):
    '''Para cada frame verifica se a mão esta encostada na barra'''
    try:
        mao_barra = verify_maoBarra(cel)
        cel.getData().set("mao_barra",mao_barra)
    except:
        cel.getData().set("mao_barra",False)

def verify_meta_extensao(cel: CelulaModel):
    '''Verifica o menor ponto que o peito atinge quando esta quando a mao na barra'''
    try:
        #So analisa caso a mão esteja na barra
        mao_barra = cel.getData().get("mao_barra")
        if(not mao_barra):
            return None
        
        #Alias
        x,y = (0,1)

        #Data Classe
        menor_ombro_esq = CelulaModel.getAggregate("menor_ombro_esq")
        menor_ombro_dir = CelulaModel.getAggregate("menor_ombro_dir")

        #Data da celula
        ombro_esq = cel.getPose().get_left_elbow()
        ombro_dir = cel.getPose().get_right_elbow()

        #Inicializando a classe
        if(menor_ombro_esq is None):
            CelulaModel.setAggregate("menor_ombro_esq",ombro_esq)
        if(menor_ombro_dir is None):
            CelulaModel.setAggregate("menor_ombro_dir",ombro_dir)
        if(menor_ombro_esq is None and menor_ombro_dir is None ):
            return
        
        #OBS: esta '>' pq  o eixo 'Y' em openCv é invertido
        if ombro_esq[y] > menor_ombro_esq[y]:
            CelulaModel.setAggregate("menor_ombro_esq",ombro_esq)
        if ombro_dir[y] > menor_ombro_dir[y]:
            CelulaModel.setAggregate("menor_ombro_dir",ombro_dir)
    except:
        pass

def verify_extensao_cotovelo(cel: CelulaModel):
    '''Para cada frame verifica se o cotovelo esta extendido'''
    try:
        extensao_cotovelo = verify_extensaoCotovelo(cel)
        cel.getData().set("extensao_cotovelo",extensao_cotovelo)
    except:
        cel.getData().set("extensao_cotovelo",False)

def verify_ultrapassar_barra(cel: CelulaModel):
    try:
        ultrapassar_barra = verify_ultrapassarBarra(cel)
        cel.getData().set("ultrapassar_barra",ultrapassar_barra)
    except:
        cel.getData().set("ultrapassar_barra",False)
    
def verify_char_AFD(cel:CelulaModel):
    '''Transforma o frame em uma letra do alfabeto para o AFD'''
    try:
        char_AFD:Char = Cel2Char(cel_meta=cel)
        cel.getData().set("AFD",char_AFD)
    except:
        pass

def verify_AFD(cel:CelulaModel):
    '''Transforma o frame em uma letra do alfabeto para o AFD'''
    try:
        char = cel.getData().get("AFD")
        char_str = str(char)
        qtd = cel.getData().getQtdMovimentos()
        qtd_offset = DataModel.agregate["aux"]
        cel.getData().setQtdMovimentos(int(qtd)+qtd_offset)
        AFD.process_char(char_str,cel)

        cel.getData().set("state",AFD.getState())
    except:
        pass

def fix_barra(cel:CelulaModel):
    '''Inferencia da posição da barra de acordo com os valores acumulados e a ideia de votação majoritaria'''
    #alias
    x,y = 0,1
    start,end = 0,1
    x1 = lambda line: line.getPoints()[start][x]
    y1 = lambda line: line.getPoints()[start][y]
    x2 = lambda line: line.getPoints()[end][x]
    y2 = lambda line: line.getPoints()[end][y]
    
    #barra atual
    data = cel.getAggregate("acumulate_barra")
    current_bar = cel.getLine()

    if data is None:
        new_data = {
            "x1_ac": x1(current_bar),
            "x2_ac": x2(current_bar),
            "y1_ac": y1(current_bar),
            "y2_ac": y2(current_bar),
            "n": 1
        }
    else:
        new_data = {
            "x1_ac": data["x1_ac"] + x1(current_bar),
            "x2_ac": data["x2_ac"] + x2(current_bar),
            "y1_ac": data["y1_ac"] + y1(current_bar),
            "y2_ac": data["y2_ac"] + y2(current_bar),
            "n": data["n"] + 1
        }
    
    cel.setAggregate("acumulate_barra",new_data)
    total = new_data["n"]

    new_bar = LineModel(new_data["x1_ac"]/total,new_data["y1_ac"]/total,new_data["x2_ac"]/total,new_data["y2_ac"]/total)
    cel.setLine(new_bar)