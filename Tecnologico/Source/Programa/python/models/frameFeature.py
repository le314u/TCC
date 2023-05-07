import json
from featureExtraction.lineModel import LineModel
from featureExtraction.poseModel import PoseModel


class FrameFeature:
    def __init__(self,barra:LineModel=None,pose:PoseModel=None) -> None:
        self.barra = barra
        self.pose = pose

    def setBarra(self,barra):
        self.barra = barra
    
    def setPose(self,pose):
        self.pose = pose
    
    def getBarra(self):
        return self.barra
    
    def getPose(self):
        return self.pose
        
    def get(self):
        return {
            "pose":self.pose,
            "barra":self.barra,
        }
        
    def __str__(self):
        ret = self.get()
        return f"Pose:{ret['pose']} Barra:{ret['barra']}"