#from asyncio import windows_events
import math
import sys
import time
import cv2
import numpy as np
from io import BytesIO
from controller.video.buffer import Buffer

    
class VideoController():

    def __init__(self, path=None, video=None ):
        #Função de pre processamentoi
        self.conf = {
            "video":None,
            "fps":0,
            "frame":None,
            "frames":[],
            "play":False,
            "size":(0,0),
            "total_frame":0,
            "id_frame":0,
        }
        
        #Carrega o video com openCv
        if path is not None:
            video = cv2.VideoCapture( path )
        self._loadVideo(video)

        #Instancia o Buffer de acordo com  o video e Carrega um vetor de frames
        self.buffer = Buffer(self.conf['fps'], [{}] * self.getTotalFrame() )
        self._video2frames()
        #Rebobina o video
        self.gotoFrame(0)
        

    def _loadVideo(self, video):
        '''Carrega o video'''
        #Seta as configurações / metaDados
        self.conf['video'] = video
        self.conf['play'] = False
        self.conf['total_frame'] = round(video.get(cv2.CAP_PROP_FRAME_COUNT))
        self.conf['fps'] = math.floor(video.get(cv2.CAP_PROP_FPS))
        self.conf['size'] = (
            round(video.get(cv2.CAP_PROP_FRAME_WIDTH)),
            round(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
        )
        return video
    
    def _video2frames(self):
        #Rebobina o video para o primeiro frame
        self.rebobina()
        #Pega o primeiro frame
        if(not self.isFinished()):
            self.nextInVideo()
        #Rebobina o video para o primeiro frame
        self.rebobina()
        #Começa a copiar frame por frame
        for i in range(self.getTotalFrame()):
            frame = self.getFrame()
            if frame is not None:
                self.conf['frames'].append(frame)
            if(not self.isFinished()):
                self.nextInVideo()

    def next(self):
        '''Passa para o proximo frame e aplica o pre processamento'''
        if(not self.isFinished()):
            id = self.conf['id_frame']+1
            self.conf['id_frame'] = id
            self.conf['frame']  = self.conf['frames'][id]
            
    def nextInVideo(self):
        '''Passa para o proximo frame e aplica o pre processamento'''
        if(not self.isFinished()):
            _, frame= self.conf['video'].read()
            self.conf['frame']  = frame
            self.conf['id_frame'] = self.conf['id_frame']+1
    
    def getFrame(self):
        '''Pega o frame atual ou ultimo frame'''
        return self.conf['frame']

    def getFrameId(self,id):
        '''Pega o frame[id] de acordo com o range'''
        max_frame = self.getTotalFrame()
        id = min( max(id, 0), max_frame)
        return self.conf['frames'][id] 
        
    def rebobina(self):
        '''Volta o video para o id 0'''
        id_frame = 0
        id_next_frame = id_frame  if id_frame < self.getTotalFrame() else self.getTotalFrame()
        self.conf['id_frame'] = id_next_frame
        self.conf['video'].set(cv2.CAP_PROP_POS_FRAMES, id_next_frame-1)
        _, frame = self.conf['video'].read()
        self.conf['frame']  = frame

    def gotoFrame(self, id_frame):
        '''Vai para o frame idFrame'''
        self.conf["id_frame"] = id_frame
        self.conf["frame"] = self.getFrameId(id_frame)

    def setFrame(self, id_frame, frame):
        '''Define um frame especifico no ID'''
        if id_frame > self.getTotalFrame() or id_frame < 0:
            print("Id Invalido")
        else:
            self.conf['frame']  = frame
            self.conf['frames'][id_frame] = frame
                
    def getIdFrame(self):
        '''retorna o id no frame que o video está'''
        return self.conf['id_frame']

    def getTotalFrame(self):
        '''retorna a quantidade maxima de frames'''
        return self.conf['total_frame']
        
    def getSize(self):
        '''Retorna as dimensoes do video'''
        return self.conf['size']
    
    def getCel(self,id):
        '''Retorna metaDados do frame ID '''
        return self.buffer.buffer[id]

    def restart(self):
        '''Move o video para o frame 1'''
        self.gotoFrame(1)
    
    def play(self):
        '''Define que o video esta em execução'''
        self.conf['play'] = True
    
    def pause(self):
        '''Define que o video esta pausado'''
        self.conf['play'] = False

    def isFinished(self):
        '''Verifica se o video chegou ao fim'''
        self.conf['play'] = self.getIdFrame() < self.getTotalFrame()-1
        return not self.conf['play']

    def isRunning(self):
        '''Retorna se o video esta rodando ou pausado'''
        return self.conf['play']


def Video(video_original, frames):
    '''Pega um conjunto de frames e cria um video'''
    #Quantidade de fps
    fps = int(video_original.get(cv2.CAP_PROP_FPS))
    #dimensão do video
    frame_size = (int(video_original.get(cv2.CAP_PROP_FRAME_WIDTH)), int(video_original.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    #codex
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # ou outro codec
    #Salva na memoria
    buffer = BytesIO()
    writer = cv2.VideoWriter(buffer, fourcc, fps, frame_size)
    #Passa frame a frame
    for f in frames:
        writer.write(f)
    #Encerra o video
    writer.release()
    #retorna o novo video
    video_data = buffer.getvalue()
    return video_data