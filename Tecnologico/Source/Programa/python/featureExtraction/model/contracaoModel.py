class ContracaoModel:

    def __init__(self, concentrica=None, excentrica=None, isometrica=None, quantidade_movimentos=None, angulo=None):
        self.concentrica = concentrica
        self.excentrica = excentrica
        self.isometrica = isometrica
        self.quantidade_movimentos = quantidade_movimentos
        if angulo is None:
            self.angulo_braco_dir = None
            self.angulo_braco_esq = None
            self.angulo_perna_dir = None
            self.angulo_perna_esq = None
        else:
            self.angulo_braco_dir = angulo.get("braco_dir")
            self.angulo_braco_esq = angulo.get("braco_esq")
            self.angulo_perna_dir = angulo.get("perna_dir")
            self.angulo_perna_esq = angulo.get("perna_esq")

    
    def __str__(self):
        return (
            f"execucoes:{self.quantidade_movimentos}\n"
            f"concentrica:{self.concentrica}\n"
            f"excentrica:{self.excentrica}\n"
            f"isometrica:{self.isometrica}\n"
            f"movimentos:{self.quantidade_movimentos}\n"
            f"angulo braco_dir: {self.angulo_braco_dir}\n"
            f"angulo braco_esq: {self.angulo_braco_esq}\n"
            f"angulo perna_dir: {self.angulo_perna_dir}\n"
            f"angulo perna_esq: {self.angulo_perna_esq}\n"
        )

    def getConcentrica(self):
        return self.concentrica

    def getExcentrica(self):
        return self.excentrica
    
    def getIsometrica(self):
        return self.isometrica

    def getQtd(self):
        return self.quantidade_movimentos

    def getAnguloBracoDir(self):
        return self.angulo_braco_dir

    def getAnguloBracoEsq(self):
        return self.angulo_braco_esq

    def getAnguloPernaDir(self):
        return self.angulo_perna_dir

    def getAnguloPernaEsq(self):
        return self.angulo_perna_esq
    
    def setConcentrica(self, concentrica):
        self.concentrica = concentrica

    def setExcentrica(self, excentrica):
        self.excentrica = excentrica

    def setIsometrica(self, isometrica):
        self.isometrica = isometrica

    def setQtd(self, quantidade_movimentos):
        self.quantidade_movimentos = quantidade_movimentos

    def setAnguloBracoDir(self, angulo):
        self.angulo_braco_dir = angulo

    def setAnguloBracoEsq(self, angulo):
        self.angulo_braco_esq = angulo

    def setAnguloPernaDir(self, angulo):
        self.angulo_perna_dir = angulo

    def setAnguloPernaEsq(self, angulo):
        self.angulo_perna_esq = angulo