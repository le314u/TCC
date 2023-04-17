#from asyncio import windows_events
from io import BytesIO
import cv2

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
    
class ControllerVideo():

    def __init__(self, path=None, video=None , process_frame = lambda x:x):
        #Função de pre processamentoi
        self.process_frame = process_frame
        self.conf = {
            "video":None,
            "frame":None,
            "frames":[],
            "play":False,
            "size":(0,0),
            "total_frame":0,
            "id_frame":0,
        }
        
        if path is not None:
            self._openVideo(path)
        elif video is not None:
            self._loadVideo(video)

    def _loadVideo(self, video):
        '''Carrega o video'''
        #Seta as configurações / metaDados
        self.conf['video'] = video
        self.conf['play'] = True
        self.conf['total_frame'] = round(video.get(cv2.CAP_PROP_FRAME_COUNT))
        self.conf['size'] = (
            round(video.get(cv2.CAP_PROP_FRAME_WIDTH)),
            round(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
        )
        return video
    
    def _openVideo(self, path):
        '''Carrega o video a partir de um path'''
        video = cv2.VideoCapture( path )
        #Seta as configurações / metaDados
        self.conf['video'] = video
        self.conf['play'] = True
        self.conf['total_frame'] = round(video.get(cv2.CAP_PROP_FRAME_COUNT))
        self.conf['size'] = (
            round(video.get(cv2.CAP_PROP_FRAME_WIDTH)),
            round(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
        )
        return video
    
    def next(self):
        '''Passa para o proximo frame e aplcia o pre processamento'''
        if(not self.isFinished()):
            _, frame= self.conf['video'].read()
            self.conf['frame']  = self.process_frame(frame)
            self.conf['id_frame'] = self.conf['id_frame']+1

    
    def getFrame(self):
        '''Pega o frame atual ou ultimo frame'''
        return self.conf['frame']
        

    def setFrame(self, id_frame):
        '''Define um frame especifico aparttir do ID'''
        id_next_frame = id_frame  if id_frame < self.getTotalFrame() else self.getTotalFrame()
        self.conf['id_frame'] = id_next_frame
        self.conf['video'].set(cv2.CAP_PROP_POS_FRAMES, id_next_frame-1)
        _, frame = self.conf['video'].read()
        self.conf['frame']  = self.process_frame(frame)


               
    def getIdFrame(self):
        '''retorna o id no frame que o video está'''
        return self.conf['id_frame']

    def getTotalFrame(self):
        '''retorna a quantidade maxima de frames'''
        return self.conf['total_frame']
        
    def getSize(self):
        '''Retorna as dimensoes do video'''
        return self.conf['size']
    
    def restart(self):
        '''Move o video para o frame 1'''
        self.setFrame(1)
    
    def play(self):
        '''Define que o video esta em execução'''
        self.conf['play'] = True
    
    def pause(self):
        '''Define que o video esta pausado'''
        self.conf['play'] = False

    def isFinished(self):
        '''Verifica se o video chegou ao fim'''
        self.conf['play'] = self.getIdFrame() < self.getTotalFrame()
        return not self.conf['play']

    def isRunning(self):
        '''Retorna se o video esta rodando ou pausado'''
        return self.conf['play']
