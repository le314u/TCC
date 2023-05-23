class ContracaoModel:

    def __init__(self, concentrica, excentrica, isometrica, quantidade_movimentos, angulo):
        self.concentrica = concentrica
        self.excentrica = excentrica
        self.isometrica = isometrica
        self.quantidade_movimentos = quantidade_movimentos
        self.angulo = angulo
    
    def __str__(self):
        return (
            f"execucoes:{self.quantidade_movimentos}\n"
            f"concentrica:{self.concentrica}\n"
            f"excentrica:{self.excentrica}\n"
            f"isometrica:{self.isometrica}\n"
        )

    def getConcentrica(self):
        return self.concentrica

    def getExcentrica(self):
        return self.excentrica
    
    def getIsometrica(self):
        return self.isometrica

    def getQtd(self):
        return self.quantidade_movimentos

    def getAngulo(self):
        return self.angulo
    
    def setConcentrica(self, concentrica):
        self.concentrica = concentrica

    def setExcentrica(self, excentrica):
        self.excentrica = excentrica

    def setIsometrica(self, isometrica):
        self.isometrica = isometrica

    def setQtd(self, quantidade_movimentos):
        self.quantidade_movimentos = quantidade_movimentos

    def setAngulo(self, angulo):
        self.angulo = angulo