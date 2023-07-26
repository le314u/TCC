from datetime import timedelta

def r2(numero):
    return round(numero, 2)

class DataModel:

    agregate = {"aux":0}
    def __init__(self, concentrica=None, excentrica=None, isometrica=None, quantidade_movimentos=None, angulo=None, meta=None):
        check = lambda variavel : timedelta(minutes=0,seconds=0,milliseconds=0) if variavel is None else variavel
        self.concentrica = check(concentrica)
        self.excentrica = check(excentrica)
        self.isometrica = check(isometrica)
        self.quantidade_movimentos = 0 if quantidade_movimentos is None else quantidade_movimentos
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
        self.meta = {} if meta is None else meta

    def __str__(self):
        time = lambda var: f"{int(var.total_seconds() // 60)} m {int(var.total_seconds() % 60)} s"

        string = str(
            f"ID: {self.meta.get('id')}\n"
            f"State: {self.meta.get('state')}\n"
        )+str(
            f"Quantidade Barras:{self.quantidade_movimentos}\n"
            f"Angulo braco:{r2(self.angulo_braco_dir)}, {r2(self.angulo_braco_esq)}\n"
            f"Angulo perna:{r2(self.angulo_perna_dir)}, {r2(self.angulo_perna_esq)}\n"
            # f"concentrica:{time(self.concentrica)}\n"
            # f"excentrica:{time(self.excentrica)}\n"
            # f"isometrica:{time(self.isometrica)}\n"
        )

        return string
    
    def __formatStr(self,dict_value):
        str_ret = ""
        for key in dict_value:
            str_ret = str_ret + f"{key}:{dict_value[key]}\n"
        return str_ret

    #     time = lambda var: f"{int(var.total_seconds() // 60)} m {int(var.total_seconds() % 60)} s"

    #     string = str(
    #         f"execucoes:{self.quantidade_movimentos}\n"
    #         f"concentrica:{time(self.concentrica)}\n"
    #         f"excentrica:{time(self.excentrica)}\n"
    #         f"isometrica:{time(self.isometrica)}\n"
    #         f"movimentos:{self.quantidade_movimentos}\n"
    #         f"angulo braco_dir:{self.angulo_braco_dir}\n"
    #         f"angulo braco_esq:{self.angulo_braco_esq}\n"
    #         f"angulo perna_dir:{self.angulo_perna_dir}\n"
    #         f"angulo perna_esq:{self.angulo_perna_esq}\n"
    #     )+str( self.meta )

    #     pares = string.split("\n")

    #     maior_string = ""
    #     for par in pares:
    #         try:
    #             chave, valor = par.split(":")
    #             if len(chave) > len(maior_string):
    #                 maior_string = chave
    #         except:
    #             break;
    #     # Reformatar os pares com ":" alinhados
    #     size = len(maior_string)
    #     saida = ""
    #     for par in pares:
    #         try:
    #             chave, valor = par.split(":")
    #             offset = size - len(chave)
    #             newChave = chave + " "*offset
    #             linha_formatada = f"{newChave}:{valor}\n"
    #             saida += linha_formatada
    #         except:
    #             break;

    #     return saida
        

    def get(self, key):
        if key in self.meta.keys() :
            return self.meta[key]
        else:
            return None

    def set(self,key,data):
        self.meta[key] = data

    def getConcentrica(self):
        return self.concentrica

    def getExcentrica(self):
        return self.excentrica
    
    def getIsometrica(self):
        return self.isometrica

    def getQtdMovimentos(self):
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

    def setQtdMovimentos(self, quantidade_movimentos):
        self.quantidade_movimentos = quantidade_movimentos

    def setAngulo(self,angulo_braco_dir=None ,angulo_braco_esq=None ,angulo_perna_dir=None ,angulo_perna_esq=None ):
        self.angulo_braco_dir = self.angulo_braco_dir if angulo_braco_dir is None else angulo_braco_dir
        self.angulo_braco_esq = self.angulo_braco_esq if angulo_braco_esq is None else angulo_braco_esq
        self.angulo_perna_dir = self.angulo_perna_dir if angulo_perna_dir is None else angulo_perna_dir
        self.angulo_perna_esq = self.angulo_perna_esq if angulo_perna_esq is None else angulo_perna_esq

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