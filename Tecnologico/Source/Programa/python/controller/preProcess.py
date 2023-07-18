import cv2
import math
import numpy as np
import traceback
from typing import List
from controller.featureExtraction.deltaCalculator import DeltaCalculator
from controller.featureExtraction.geometria import angle_line, angle_point, intercept, segment, inclinacao_reta, rotate_segment
from controller.featureExtraction.objectDetector import PosePoints, detectBar
from controller.util.beep import beep
from controller.util.flag import Flag
from controller.util.progress_bar import progress_bar
from controller.util.coloredMsg import msg
from controller.video.buffer import Buffer
from controller.video.videoController import VideoController
from model.AFD.charAFD import charAFD
from model.featureExtraction.dataModel import DataModel
from model.featureExtraction.lineModel import LineModel
from model.featureExtraction.poseModel import PoseModel, Segmento
from model.featureExtraction.metaPoseModel import MetaPoseModel
from model.video.celulaModel import CelulaModel

from controller.processImg.filter import limiarizacao, pixelizacao, imagem_cinza, suavizacao, rotacao
from controller.processImg.debug import save_img, display_img, display_imgs
from controller.processImg.mask import Mask

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

        
        #Rotaciona o frame de acordo com a Barra
        check(controller,check_inclination_frame,"rotaciona frame")
        check(controller,check_inclination_barra,"rotaciona barra")
        att_frames(controller)
        msg("\r"+"Rotação")

        enable_flag(flags,"Barra")

        #Estimativa de pose Humana
        check(controller,check_edh,"Estimativa de pose")
        msg("\r"+"Pose")
        enable_flag(flags,"EDH")    
        
        check(controller,check_metaData,"meta Dados")
        msg("\r"+"meta data and display data")

        # check_gradiente(controller)
        
        # check(controller,verify_maoBarra,"Mão na Barra")
        # msg("AFD-Mão na Barra")

        #enable_flag(flags,"Dados")





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
    celData = buffer.get_cell(index).get()
    celData["line"]=line    
    cel = CelulaModel(**celData)
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
    
    celData = buffer.get_cell(index).get()
    celData["pose"]=PoseModel(*points)    
    cel = CelulaModel(**celData)
    buffer.set_cell(index, cel)

def tendency_barra_moda(buffer:Buffer):
    '''Descobre a media e resignifica a barra'''
    start,end = 0, buffer.size()
    array = buffer.get_slice((start,end), lambda data: data.getLine() )    
    extract = lambda i,j : ( lambda line: line.getPoints()[i][j] )
    getMode = lambda i,j: round(DeltaCalculator.get_mode(array, extract(i,j)))
    x1,y1,x2,y2 = getMode(0,0), getMode(0,1), getMode(1,0), getMode(1,1)

    for index in range(end):
        line = LineModel(x1,y1,x2,y2)
        celData = buffer.get_cell(index).get()
        celData["line"]=line    
        cel = CelulaModel(**celData)
        buffer.set_cell(index, cel)
    
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
            cel = CelulaModel()
            frame = controller.getFrameId(id)
            cel.setFrame(frame)
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

def check_inclination_frame(cel:CelulaModel):
    '''Apartir da posição da barra rotaciona o frame'''

    #Apartir da posição da barra rotaciona o frame
    barra:LineModel = cel.getLine()
    #barra:LineModel = fix_barra_moda(controller.buffer)
    pt1,pt2 = barra.getPoints()
    angulo = inclinacao_reta(pt1,pt2)
    frame = cel.getFrame()
    new_frame = rotacao(frame,angulo)
    cel.setFrame(new_frame)

def check_inclination_barra(cel:CelulaModel):
    '''Apartir da rotação do frame rotaciona a barra'''
    #Apartir da posição da barra rotaciona o frame
    barra:LineModel = cel.getLine()
    #barra:LineModel = fix_barra_moda(controller.buffer)
    pt1,pt2 = barra.getPoints()
    angulo = inclinacao_reta(pt1,pt2)
    p1,p2 = rotate_segment(pt1,pt2,-angulo)
    newBarra:LineModel = LineModel(*p1,*p2)
    cel.setLine(newBarra)

def check_edh(cel:CelulaModel):
    frame = cel.getFrame()
    posePoints:PosePoints = PosePoints(frame)
    pose:PoseModel = posePoints.getPose()   
    cel.setPose(pose)

def check_gradiente(controller:VideoController):
    total = controller.getTotalFrame()
    #Carrega todos os frames no Controller
    for id in range(total):
        cel:CelulaModel = controller.buffer.get_cell(id)
        m = charAFD(cel_meta=cel)
        print(m.getChar())
        
def check_metaData(cel:CelulaModel):
    #TODO Lembrar pq fiz 'MetaPoseModel' isso e ver o que isso esta fazendo
    meta = MetaPoseModel(cel.getPose())
    cel.setMetaPose(meta)
    
    angle = angleSegments(cel)
    data = DataModel("0","0","0","0", meta, angle)
    #set cel
    cel.setData(data)
        


def verify_maoBarra(cel:CelulaModel):
    size = 10    # Tamanho do kernel de Blur e Pixelização
    limiar = 100    # Definir um limiar para identificar a descontinuidade

    #Start
    frame = cel.getFrame()
    barra = cel.getLine()
    mask_barra = MASK.createLineMask(frame,barra.getStart(),barra.getEnd(),50)
    mask_frame = MASK.getMask()
    newFrame = MASK.putMask(frame, mask_frame)
    
    # Converter a imagem para o espaço de cores HSV
    imagem_hsv = cv2.cvtColor(newFrame, cv2.COLOR_BGR2HSV)

    #Definir os intervalos de cor da pele
    lower_skin = np.array([0, 25, 0], dtype=np.uint8)
    upper_skin = np.array([20, 255, 255], dtype=np.uint8)

    # Aplicar uma máscara para obter apenas a parte da cor da imagem
    mascara = cv2.inRange(imagem_hsv, lower_skin, upper_skin)
    canal_x = cv2.bitwise_and(frame, frame, mask=mascara)

    # Converter a imagem apenas para P&B
    gray = imagem_cinza(canal_x)
    limited = limiarizacao(gray,100)
    # Aplcia um desfoque
    blur = suavizacao(limited,size)
    limited = limiarizacao(blur,100)
    # Aplica a pixelização
    pixel = pixelizacao(limited,size)
    #Aplica a Mascara da area de interesse
    only_hand = cv2.bitwise_and(mask_barra, pixel)


    # Aplicar o operador de Sobel
    gradient_x = cv2.Sobel(only_hand, cv2.CV_64F, 1, 0, ksize=3)
    gradient_y = cv2.Sobel(only_hand, cv2.CV_64F, 0, 1, ksize=3)

    # Calcular o módulo do gradiente
    gradient = np.sqrt(gradient_x ** 2 + gradient_y ** 2)

    # Verificar a descontinuidade em cada pixel
    descontinuidade = gradient > limiar

    # Verificar se houve ou não descontinuidade na imagem ou seja se a mão esta ou não na barra
    if np.any(descontinuidade):
        # Houve descontinuidade do preto logo a mão estava na barra 
        # Em caso de erro a cabeça estava na barra mas isso so é possivel se:
        #   caso a mão esteja na barra
        #   ele tenha pulado 
        #   subido em um banco 
        #   entre outros casos
        return True
    else:
        return False
        





    
def gradiente(frame,barra):
    mask_barra = createLineMask(frame,barra.getStart(),barra.getEnd(),50)
    path_mask = "/home/guest/Área de Trabalho/TCC/Tecnologico/Source/Programa/python/midia/mascara/mask.png" 
    mask = cv2.imread(path_mask)
    newFrame = cv2.bitwise_and(frame, mask)
    
    # Definir o kernel
    kernel = np.array([
        [1, 0, -1],
        [2, 0, -2],
        [1, 0, -1]])

    # Converter a imagem para o espaço de cores HSV
    imagem_hsv = cv2.cvtColor(newFrame, cv2.COLOR_BGR2HSV)

    #Definir os intervalos de cor da pele
    lower_skin = np.array([0, 25, 0], dtype=np.uint8)
    upper_skin = np.array([20, 255, 255], dtype=np.uint8)

    # Aplicar uma máscara para obter apenas a parte da cor da imagem
    mascara = cv2.inRange(imagem_hsv, lower_skin, upper_skin)
    canal_x = cv2.bitwise_and(frame, frame, mask=mascara)

    # Converter a imagem para escala de cinza
    gray = imagem_cinza(canal_x)
    limited = limiarizacao(gray,100)
    
    size = 10
    blur = suavizacao(limited,size)
    limited = limiarizacao(blur,100)
    pixel = pixelizacao(limited,size)

    end = cv2.bitwise_and(mask_barra, pixel)


    gray = end

    # Aplicar o operador de Sobel
    gradient_x = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
    gradient_y = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)

    # Calcular o módulo do gradiente
    gradient = np.sqrt(gradient_x ** 2 + gradient_y ** 2)

    # Definir um limiar para identificar a descontinuidade
    limiar = 100

    # Verificar a descontinuidade em cada pixel
    descontinuidade = gradient > limiar

    # Verificar se houve ou não descontinuidade na imagem
    if np.any(descontinuidade):
        print("Houve descontinuidade na imagem.")
    else:
        print("Não houve descontinuidade na imagem.")
        
    display_imgs(mask_barra,end)

    # # Aplicar o filtro
    # end = cv2.filter2D(limited, -1, kernel)# Aplicar o filtro

def gradiente_BKP(frame):

    path_mask = "/home/guest/Área de Trabalho/TCC/Tecnologico/Source/Programa/python/midia/mascara/mask.png" 
    mask = cv2.imread(path_mask)
    newFrame = cv2.bitwise_and(frame, mask)
    
    # Definir o kernel
    kernel = np.array([
        [1, 0, -1],
        [2, 0, -2],
        [1, 0, -1]])

    # Converter a imagem para o espaço de cores HSV
    imagem_hsv = cv2.cvtColor(newFrame, cv2.COLOR_BGR2HSV)

    #Definir os intervalos de cor da pele
    lower_skin = np.array([0, 25, 0], dtype=np.uint8)
    upper_skin = np.array([20, 255, 255], dtype=np.uint8)

    # Aplicar uma máscara para obter apenas a parte da cor da imagem
    mascara = cv2.inRange(imagem_hsv, lower_skin, upper_skin)
    canal_x = cv2.bitwise_and(frame, frame, mask=mascara)

    # Converter a imagem para escala de cinza
    gray = imagem_cinza(canal_x)
    limited = limiarizacao(gray,100)
    blur = suavizacao(limited,5)
    limited = limiarizacao(blur,100)

    # Aplicar o filtro
    end = cv2.filter2D(limited, -1, kernel)# Aplicar o filtro


    display_img(end)

    




    
def angleSegments(cel:CelulaModel):
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
    celData = CelulaModel().get()
    frame_cp=None

    try:
        frame_cp = frame.copy()
    except:
        return CelulaModel(**celData)

    #Extrai a barra
    try:
        celData["line"]:LineModel = detectBar(frame_cp)
    except:
        celData["line"] = None

    #Extrai pose do frame
    try:
        posePoints:PosePoints = PosePoints(frame_cp)
        celData["pose"]:PoseModel = posePoints.getPose()   
    except:
        celData["pose"] = None

    #retorno
    return CelulaModel(**celData)

    
def enable_flag(flags, flag_name):
    for flag in flags:
        if flag.getName() == flag_name:
            flag.activate()
            break;







def getBarra(frame) -> CelulaModel:
    """Identifica a barra no frame"""
    #Inicia o Frame
    frame_cp, barra =  [None]*2
    try:
        frame_cp = frame.copy()
        barra:LineModel = detectBar(frame_cp)
        return barra
    except:
        barra = None
        return barra
    


#END