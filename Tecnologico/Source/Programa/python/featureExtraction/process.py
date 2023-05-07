import math
from typing import List
from featureExtraction.lineModel import LineModel
from models.buffer import Buffer
from models.frameFeature import FrameFeature
from featureExtraction.deltaCalculator import DeltaCalculator


def indice_not_process(buffer:Buffer):
    '''Retorna os indices que nao foi possivel fazer a extração da imagem'''
    not_allocated = {"barra":[],"pose":[]}
    for i in range(buffer.size()):
        cel:FrameFeature = buffer.get_cell(i)
        if cel.getBarra() == None:
            not_allocated['barra'].append(i)
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
    extractBar = lambda i,j : ( lambda line: line.getPoints()[i][j] )
    getMean = lambda i,j: round(DeltaCalculator.get_mean(array, extractBar(i,j)))
    x1 = getMean(0,0)
    y1 = getMean(0,1)
    x2 = getMean(1,0)
    y2 = getMean(1,1)
    line = LineModel(x1,y1,x2,y2)
    pose = buffer.get_cell(index)
    feature = FrameFeature(barra=line,pose=pose)
    buffer.set_cell(index, feature)


    #Passa pelo buffer
    #Analisa as celulas que estao faltando
    #Verifica o gradiente de  variação