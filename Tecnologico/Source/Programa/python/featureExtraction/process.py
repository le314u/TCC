import pdb
import math
from typing import List
from featureExtraction.lineModel import LineModel
from featureExtraction.poseModel import PoseModel
from models.buffer import Buffer
from models.celulaModel import CelulaModel
from featureExtraction.deltaCalculator import DeltaCalculator


def indice_not_process(buffer:Buffer):
    '''Retorna os indices que nao foi possivel fazer a extração da imagem'''
    not_allocated = {"line":[],"pose":[]}
    for i in range(buffer.size()):
        cel:CelulaModel = buffer.get_cell(i)
        if cel.getLine() == None:
            not_allocated['line'].append(i)
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

def fix_barra(buffer:Buffer, index:int):
    '''Inferencia da posição da barra'''
    start,end = get_range_to_analyze(buffer,index)
    array = buffer.get_slice((start,end), lambda data: data.getBarra() )    
    extract = lambda i,j : ( lambda line: line.getPoints()[i][j] )
    getMean = lambda i,j: round(DeltaCalculator.get_mean(array, extract(i,j)))
    x1 = getMean(0,0)
    y1 = getMean(0,1)
    x2 = getMean(1,0)
    y2 = getMean(1,1)
    line = LineModel(x1,y1,x2,y2)
    pose = buffer.get_cell(index).getPose()
    cel = CelulaModel(line=line,pose=pose)
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
    feature = CelulaModel(line=line,pose=pose)
    buffer.set_cell(index, feature)

    # Passa pelo buffer
    # Analisa as celulas que estao faltando
    # Verifica o gradiente de  variação

# def DEBUG(data):
#     ret = ""
#     if isinstance(data,PoseModel):
#         ret = "Pose" 
#     if isinstance(data,CelulaModel):
#         ret = "Frame" 
#     if data is None:
#         ret = "None" 
#     print(ret)