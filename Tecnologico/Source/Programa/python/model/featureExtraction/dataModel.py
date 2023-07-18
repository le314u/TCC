def r2(numero):
    return round(numero, 2)

class DataModel:

    def __init__(self, concentrica=None, excentrica=None, isometrica=None, quantidade_movimentos=None, meta=None, angulo=None,):
        self.concentrica = concentrica
        self.excentrica = excentrica
        self.isometrica = isometrica
        self.quantidade_movimentos = quantidade_movimentos
        self.meta = meta
        if angulo is None:
            self.angulo_braco_dir = None
            self.angulo_braco_esq = None
            self.angulo_perna_dir = None
            self.angulo_perna_esq = None
        else:
            self.angulo_braco_dir = r2(angulo.get("braco_dir"))
            self.angulo_braco_esq = r2(angulo.get("braco_esq"))
            self.angulo_perna_dir = r2(angulo.get("perna_dir"))
            self.angulo_perna_esq = r2(angulo.get("perna_esq"))

    
    def __str__(self):
        return str(self.formatStr())
    
    def string(self):
        return str(
            f"execucoes:{self.quantidade_movimentos}\n"
            f"concentrica:{self.concentrica}\n"
            f"excentrica:{self.excentrica}\n"
            f"isometrica:{self.isometrica}\n"
            f"movimentos:{self.quantidade_movimentos}\n"
            f"angulo braco_dir:{self.angulo_braco_dir}\n"
            f"angulo braco_esq:{self.angulo_braco_esq}\n"
            f"angulo perna_dir:{self.angulo_perna_dir}\n"
            f"angulo perna_esq:{self.angulo_perna_esq}\n"
        )+str(self.meta)
    
    def formatStr(self):
        string = self.string()
        pares = string.split("\n")

        maior_string = ""
        for par in pares:
            try:
                chave, valor = par.split(":")
                if len(chave) > len(maior_string):
                    maior_string = chave
            except:
                break;
        # Reformatar os pares com ":" alinhados
        size = len(maior_string)
        saida = ""
        for par in pares:
            try:
                chave, valor = par.split(":")
                offset = size - len(chave)
                newChave = chave + " "*offset
                linha_formatada = f"{newChave}:{valor}\n"
                saida += linha_formatada
            except:
                break;

        print(saida)
        return saida


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
    
    def getMeta(self):
        return self.meta
    
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

    def setMeta(self, meta):
        self.meta = meta