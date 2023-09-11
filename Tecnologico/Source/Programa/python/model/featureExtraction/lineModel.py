class LineModel:
    def __init__(self,x1,y1, x2,y2, thickness = 1) -> None:
        #point 1
        self.x1 = round(x1)
        self.y1 = round(y1)
        #point 2
        self.x2 = round(x2)
        self.y2 = round(y2)

        self.thickness = thickness

    def __str__(self):
        return f"Start:{self.getStart()} End:{self.getEnd()}"

    def getStart(self):
        return (self.x1,self.y1)

    def getEnd(self):
        return (self.x2,self.y2)

    def getPoints(self):
        return ((self.x1,self.y1),(self.x2,self.y2))
        
    def getThickness(self):
        return self.thickness
    
    def setThickness(self, thickness):
        self.thickness = thickness
    