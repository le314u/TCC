import sys
import os
import cv2
import numpy as np
import mediapipe as mp

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from processImg.processPose import processPose




class Process():
    
    def __init__(self):
        #Flags
        self.flags = {}
        
    def addFlag(self, flag, value = False):
        if not flag in self.flags:
            self.flags[flag] = value

    def bar(self, frame):
        '''Dado um frame desenha sobre a pose'''
        return frame
    
    def pose(self, frame):
        return processPose(frame) if self.flags["poseDetection"] else frame

    def data(self, frame):
        return frame
    
    def processIMG(self,frame):
        '''Executa cada função do pipeline sobre o frame atual'''
        pipeline = [self.bar, self.pose, self.data]
        for function in pipeline:
            frame = function(frame)
        return frame