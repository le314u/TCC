from enum import Enum
from model.featureExtraction.lineModel import LineModel

D = "Direito"
E = "Esquerdo"
_parte = lambda parteA, parteB, lado: (f"{parteA}{lado}", f"{parteB}{lado}")

class Segmento(Enum):
    CORPO = ('Ombro Esquerdo', 'Ombro Direito', 'Quadril Direito', 'Quadril Esquerdo')
    BRACO_DIR = _parte('Pulso ', 'Cotovelo ', D) + _parte('Cotovelo ', 'Ombro ', D)
    BRACO_ESQ = _parte('Pulso ', 'Cotovelo ', E) + _parte('Cotovelo ', 'Ombro ', E)
    PERNA_DIR = _parte('Calcanhar ', 'Joelho ', D) + _parte('Joelho ', 'Quadril ', D)
    PERNA_ESQ = _parte('Calcanhar ', 'Joelho ', E) + _parte('Joelho ', 'Quadril ', E)
    MAO_D = ['Mindinho Direito','Indicador Direito','Polegar Direito']
    MAO_E = ['Mindinho Esquerdo','Indicador Esquerdo','Polegar Esquerdo']

class PoseModel():
    def __init__(self,
        left_ankle = None,
        left_elbow = None,
        left_shoulder = None,
        left_heel = None,
        left_hip = None,
        left_knee = None,
        left_wrist = None,
        left_pinky = None,
        left_index = None,
        left_thumb = None,
        right_ankle = None,
        right_elbow = None,
        right_shoulder = None,
        right_heel = None,
        right_hip = None,
        right_knee = None,
        right_wrist = None,
        right_pinky = None,
        right_index = None,
        right_thumb = None,
    ) -> None:

        self.left_ankle = left_ankle 
        self.left_elbow = left_elbow 
        self.left_shoulder = left_shoulder 
        self.left_heel = left_heel 
        self.left_hip = left_hip 
        self.left_knee = left_knee 
        self.left_wrist = left_wrist 
        self.left_pinky = left_pinky
        self.left_index = left_index
        self.left_thumb = left_thumb
        self.right_ankle = right_ankle 
        self.right_elbow = right_elbow 
        self.right_shoulder = right_shoulder 
        self.right_heel = right_heel 
        self.right_hip = right_hip 
        self.right_knee = right_knee 
        self.right_wrist = right_wrist 
        self.right_pinky = right_pinky 
        self.right_index = right_index 
        self.right_thumb = right_thumb 

        self.ponto = {}
        self.ponto['Tornozelo Esquerdo'] = self.left_ankle
        self.ponto['Cotovelo Esquerdo'] = self.left_elbow
        self.ponto['Ombro Esquerdo'] = self.left_shoulder
        self.ponto['Calcanhar Esquerdo'] = self.left_heel
        self.ponto['Quadril Esquerdo'] = self.left_hip
        self.ponto['Joelho Esquerdo'] = self.left_knee
        self.ponto['Pulso Esquerdo'] = self.left_wrist
        self.ponto['Mindinho Esquerdo'] = self.left_pinky
        self.ponto['Indicador Esquerdo'] = self.left_index
        self.ponto['Polegar Esquerdo'] = self.left_thumb
        self.ponto['Tornozelo Direito'] = self.right_ankle
        self.ponto['Cotovelo Direito'] = self.right_elbow
        self.ponto['Ombro Direito'] = self.right_shoulder
        self.ponto['Calcanhar Direito'] = self.right_heel
        self.ponto['Quadril Direito'] = self.right_hip
        self.ponto['Joelho Direito'] = self.right_knee
        self.ponto['Pulso Direito'] = self.right_wrist
        self.ponto['Mindinho Direito'] = self.right_pinky
        self.ponto['Indicador Direito'] = self.right_index
        self.ponto['Polegar Direito'] = self.right_thumb

    def __str__(self):
        return str(self.ponto)
        
    def getPoints(self):
        return self.ponto

    def get_left_ankle(self):
        return self.left_ankle

    def get_left_elbow(self):
        return self.left_elbow

    def get_left_shoulder(self):
        return self.left_shoulder

    def get_left_heel(self):
        return self.left_heel

    def get_left_hip(self):
        return self.left_hip

    def get_left_knee(self):
        return self.left_knee

    def get_left_wrist(self):
        return self.left_wrist

    def get_left_pinky(self):
        return self.left_pinky
        
    def get_left_index(self):
        return self.left_index
        
    def get_left_thumb(self):
        return self.left_thumb
    
    def get_right_ankle(self):
        return self.right_ankle

    def get_right_elbow(self):
        return self.right_elbow

    def get_right_shoulder(self):
        return self.right_shoulder

    def get_right_heel(self):
        return self.right_heel

    def get_right_hip(self):
        return self.right_hip

    def get_right_knee(self):
        return self.right_knee

    def get_right_wrist(self):
        return self.right_wrist
    
    def get_right_pinky(self):
        return self.right_pinky

    def get_right_index(self):
        return self.right_index

    def get_right_thumb(self):
        return self.right_thumb

    #LINE
    def getSegmentLine(self, segment:Segmento)->LineModel:
        '''Dado um segmento retorna uma linha que o representa'''
        val = segment.value
        total = len(val)
        qtdParts = round(total/2)
        segmentLine = [None] * qtdParts
        for part in range(qtdParts):
            id = 2*(part)
            p1,p2 = self.segmentName2Point(val[id]), self.segmentName2Point(val[id+1])
            segmentLine[part] = LineModel(*p1,*p2)
        return segmentLine                                                                                                                                  
        
    def segmentName2Point(self, segmentName):
        return self.ponto[segmentName]
    
    def position_hand(self):
        x,y = (0,1)
        LEFT_HAND = "INCONSISTENTE"
        RIGHT_HAND = "INCONSISTENTE"
        if( self.get_left_pinky()[x] < self.get_left_thumb()[x] ):
            LEFT_HAND = "PRONADO"
        
        if( self.get_left_pinky()[x] > self.get_left_thumb()[x] ):
            LEFT_HAND = "SUPINADO"
        
        if( self.get_left_pinky()[x] == self.get_left_thumb()[x] ):
            LEFT_HAND = "INCONSISTENTE"


        if( self.get_right_thumb()[x] < self.get_right_pinky()[x] ):
            RIGHT_HAND = "PRONADO"
        
        if( self.get_right_thumb()[x] > self.get_right_pinky()[x] ):
            RIGHT_HAND = "SUPINADO"
        
        if( self.get_right_thumb()[x] == self.get_right_pinky()[x] ):
            RIGHT_HAND = "INCONSISTENTE"
        
        #print(LEFT_HAND, RIGHT_HAND)
