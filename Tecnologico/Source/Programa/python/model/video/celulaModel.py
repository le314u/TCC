import json
from typing import Optional
from model.featureExtraction.lineModel import LineModel
from model.featureExtraction.poseModel import PoseModel
from model.featureExtraction.contracaoModel import ContracaoModel

class CelulaModel:
    def __init__(self,pose=None, line=None, data=None) -> None:
        self.pose:PoseModel = pose
        self.line:LineModel = line
        self.data:ContracaoModel = data
    
    def __str__(self) -> str:
        return ""+\
            f"Pose:{not self.pose is None}"+\
            f"Line:{not self.line is None}"+\
            f"Data:{not self.data is None}";
                
    def getPose(self) -> Optional[PoseModel]:
        return self.pose
    
    def setPose(self, pose:PoseModel):
        self.pose = pose
    
    def getLine(self) -> Optional[LineModel]:
        return self.line
    
    def setLine(self, line:LineModel):
        self.line = line
    
    def getData(self) -> Optional[ContracaoModel]:
        return self.data
    
    def setData(self, data:ContracaoModel):
        self.data = data
    
    def get(self):
        pass