from model.featureExtraction.poseModel import PoseModel
from controller.featureExtraction.geometria import distance_point_line, distance_points

def r2(numero):
    return round(numero, 2)

class MetaPoseModel():
    def __init__(self,poseModel) -> None:
        self.pose:PoseModel=poseModel
        self.parts = ["left_arm","left_forearm","right_arm","right_forearm"]
        self.sizes = {}
        self.size_parts()

    def __str__(self):
        ret = ""
        for part in self.parts:
            ret = ret + f"size_{part}:{self.sizes[part]}\n"
        return str(ret)
    
    def size_parts(self):
        self.size_part("left_arm",
            self.pose.get_left_shoulder(),
            self.pose.get_left_elbow()
        )

        self.size_part("left_forearm",
            self.pose.get_left_elbow(),
            self.pose.get_left_wrist(),
        )

        self.size_part("right_arm",
            self.pose.get_right_shoulder(),
            self.pose.get_right_elbow()
        )

        self.size_part("right_forearm",
            self.pose.get_right_elbow(),
            self.pose.get_right_wrist(),
        )
        
    def size_part(self, partName, point1, point2):
        size = distance_points(point1, point2)
        self.sizes[partName] =  r2(size)
        


    
        