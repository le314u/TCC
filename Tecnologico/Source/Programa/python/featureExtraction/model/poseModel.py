from enum import Enum
from featureExtraction.model.lineModel import LineModel

D = "Direito"
E = "Esquerdo"
_parte = lambda parteA, parteB, lado: (f"{parteA}{lado}", f"{parteB}{lado}")

class Segmento(Enum):
    CORPO = ('Ombro Esquerdo', 'Ombro Direito', 'Quadril Direito', 'Quadril Esquerdo')
    BRACO_DIR = _parte('Pulso ', 'Cotovelo ', D) + _parte('Cotovelo ', 'Ombro ', D)
    BRACO_ESQ = _parte('Pulso ', 'Cotovelo ', E) + _parte('Cotovelo ', 'Ombro ', E)
    PERNA_DIR = _parte('Calcanhar ', 'Joelho ', D) + _parte('Joelho ', 'Quadril ', D)
    PERNA_ESQ = _parte('Calcanhar ', 'Joelho ', E) + _parte('Joelho ', 'Quadril ', E)

class PoseModel():
    def __init__(self,
        left_ankle = None,
        left_elbow = None,
        left_shoulder = None,
        left_heel = None,
        left_hip = None,
        left_knee = None,
        left_wrist = None,
        right_ankle = None,
        right_elbow = None,
        right_shoulder = None,
        right_heel = None,
        right_hip = None,
        right_knee = None,
        right_wrist = None,
    ) -> None:

        self.left_ankle = left_ankle 
        self.left_elbow = left_elbow 
        self.left_shoulder = left_shoulder 
        self.left_heel = left_heel 
        self.left_hip = left_hip 
        self.left_knee = left_knee 
        self.left_wrist = left_wrist 
        self.right_ankle = right_ankle 
        self.right_elbow = right_elbow 
        self.right_shoulder = right_shoulder 
        self.right_heel = right_heel 
        self.right_hip = right_hip 
        self.right_knee = right_knee 
        self.right_wrist = right_wrist 

        self.ponto = {}
        self.ponto['Tornozelo Esquerdo'] = self.left_ankle
        self.ponto['Cotovelo Esquerdo'] = self.left_elbow
        self.ponto['Ombro Esquerdo'] = self.left_shoulder
        self.ponto['Calcanhar Esquerdo'] = self.left_heel
        self.ponto['Quadril Esquerdo'] = self.left_hip
        self.ponto['Joelho Esquerdo'] = self.left_knee
        self.ponto['Pulso Esquerdo'] = self.left_wrist
        self.ponto['Tornozelo Direito'] = self.right_ankle
        self.ponto['Cotovelo Direito'] = self.right_elbow
        self.ponto['Ombro Direito'] = self.right_shoulder
        self.ponto['Calcanhar Direito'] = self.right_heel
        self.ponto['Quadril Direito'] = self.right_hip
        self.ponto['Joelho Direito'] = self.right_knee
        self.ponto['Pulso Direito'] = self.right_wrist

    def __str__(self):
        return str(self.ponto)
        
    def getPoint(self):
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
        
    #LINE
    def getSegmentLine(self, segment:Segmento)->LineModel:
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