class LineModel:
    def __init__(self,x1,y1,x2,y2) -> None:
        #point 1
        self.x1 = x1
        self.y1 = y1
        #point 2
        self.x2 = x2
        self.y2 = y2

    def __str__(self):
        return f"Start:{self.getStart()} End:{self.getEnd()}"

    def getStart(self):
        return (self.x1,self.y1)

    def getEnd(self):
        return (self.x2,self.y2)

    def getPoints(self):
        return ((self.x1,self.y1),(self.x2,self.y2))