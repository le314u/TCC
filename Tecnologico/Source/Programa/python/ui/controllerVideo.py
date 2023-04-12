#from asyncio import windows_events
import cv2

class ControllerVideo():

    def __init__(self, path):
        self.conf = {
            "video":None,
            "frame":None,
            "play":False,
            "size":(0,0),
            "total_frame":0,
            "id_frame":0,
        }
        self._openVideo(path)

    def _openVideo(self, path):
        '''Carrega o video'''
        video = cv2.VideoCapture( path )
        #Seta as configurações / metaDados
        self.conf['video'] = video
        self.conf['total_frame'] = round(video.get(cv2.CAP_PROP_FRAME_COUNT))
        self.conf['size'] = (
            round(video.get(cv2.CAP_PROP_FRAME_WIDTH)),
            round(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
        )
        return video
    
    def next(self):
        '''Passa para o proximo frame'''
        if(not self.isFinished()):
            _, self.conf['frame'] = self.conf['video'].read()
            self.conf['id_frame'] = self.conf['id_frame']+1

    
    def getFrame(self):
        '''Pega o frame atual ou ultimo frame'''
        return self.conf['frame']
        

    def setFrame(self, id_frame):
        '''Define um frame especifico aparttir do ID'''
        id_next_frame = id_frame  if id_frame <= self.getTotalFrame() else self.getTotalFrame()
        self.conf['id_frame'] = id_next_frame
        self.conf['video'].set(cv2.CAP_PROP_POS_FRAMES, id_next_frame-1)
        _, self.conf['frame'] = self.conf['video'].read()

               
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
        self.conf['play'] = self.getIdFrame() <= self.getTotalFrame()
        return not self.conf['play']

    def isRunning(self):
        '''Retorna se o video esta rodando ou pausado'''
        return self.conf['play']