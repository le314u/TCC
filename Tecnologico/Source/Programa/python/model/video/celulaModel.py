import json
from typing import Optional
from model.featureExtraction.lineModel import LineModel
from model.featureExtraction.poseModel import PoseModel
from model.featureExtraction.metaPoseModel import MetaPoseModel
from model.featureExtraction.dataModel import DataModel

class CelulaModel:
    def __init__(self,pose=None, line=None, data=None, metaPose=None, frame=None) -> None:
        self.pose:PoseModel = pose
        self.line:LineModel = line
        self.data:DataModel = data
        self.metaPose:MetaPoseModel = metaPose
        self.frame = frame

    def __str__(self) -> str:
        return ""+\
            f"Pose:{not self.pose is None}"+\
            f"Line:{not self.line is None}"+\
            f"Data:{not self.data is None}"+\
            f"MetaPose:{not self.metaPose is None}"+\
            f"Frame:{not self.frame is None}";

    def getFrame(self):
        return None if self.frame is None else self.frame.copy()
    
    def setFrame(self, frame):
        self.frame = frame
                
    def getPose(self) -> Optional[PoseModel]:
        return self.pose
    
    def setPose(self, pose:PoseModel):
        self.pose = pose
    
    def getLine(self) -> Optional[LineModel]:
        return self.line
    
    def setLine(self, line:LineModel):
        self.line = line
    
    def getData(self) -> Optional[DataModel]:
        return self.data
    
    def setData(self, data:DataModel):
        self.data = data
    
    def getMetaPose(self) -> Optional[MetaPoseModel]:
        return self.metaPose
    
    def setMetaPose(self, metaPose:MetaPoseModel):
        self.metaPose = metaPose

    def get(self):
        return {
            "pose" : self.getPose(),
            "line" : self.getLine(),
            "data" : self.getData(),
            "metaPose" : self.getMetaPose(),
            "frame" : self.getFrame()
        }