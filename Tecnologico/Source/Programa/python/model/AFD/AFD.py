import traceback
from model.video.celulaModel import CelulaModel
from controller.featureExtraction.geometria import distance_point_line
from controller.featureExtraction.objectDetector import verify_maoBarra,verify_extensaoCotovelo,verify_ultrapassarBarra,verify_movimentoQuadrilPerna

class Char:
    def __init__(self, mao_barra=None,extensao_cotovelo=None ,ultrapassar_barra=None ,movimento_quadrilPerna=None ) -> None:
        self.mao_barra = mao_barra                              #Mao na Barra  
        # self.concentrica = concentrica                          #Gradiente positivo     Concentrica  
        # self.excentrica = excentrica                            #Gradiente negativo     Excentrica  
        self.extensao_cotovelo = extensao_cotovelo              #Extensão de Cotovelo  
        self.ultrapassar_barra = ultrapassar_barra              #Ultrapassar a barra  
        self.movimento_quadrilPerna = movimento_quadrilPerna    #Movimento de Quadril ou Perna  
    
    def __str__(self) -> str:
        attributes = [ str(attr) if not isinstance(attr, str) else f'"{attr}"' for attr in self.get()]
        return f"[{', '.join(attributes)}]"

    def get(self):
        return [ self.mao_barra, self.extensao_cotovelo, self.ultrapassar_barra, self.movimento_quadrilPerna ]

    def get_mao_barra(self):
        return self.self.mao_barra

    def set_mao_barra(self, mao_barra):
        self.mao_barra = mao_barra

    def get_extensao_cotovelo(self):
        return self.self.extensao_cotovelo

    def set_extensao_cotovelo(self, extensao_cotovelo):
        self.extensao_cotovelo = extensao_cotovelo

    def get_ultrapassar_barra(self):
        return self.self.ultrapassar_barra

    def set_ultrapassar_barra(self, ultrapassar_barra):
        self.ultrapassar_barra = ultrapassar_barra

    def get_movimento_quadrilPerna(self):
        return self.self.movimento_quadrilPerna

    def set_movimento_quadrilPerna(self, movimento_quadrilPerna):
        self.movimento_quadrilPerna = movimento_quadrilPerna


    # def get_concentrica(self):
    #     return self.self.concentrica

    # def set_concentrica(self, concentrica):
    #     self.concentrica = concentrica

    # def get_excentrica(self):
    #     return self.self.excentrica

    # def set_excentrica(self, excentrica):
    #     self.excentrica = excentrica
 
class Machine:
    def __init__(self, alfabeto, estados, estado_inicial, estados_finais, transicoes) -> None:
        self.alfabeto = alfabeto
        self.estados = estados
        self.estado_inicial = estado_inicial
        self.estados_finais = estados_finais
        self.transicoes = transicoes
        self.estado_atual = estado_inicial

    def getState(self):
        return self.estado_atual
    
    def process_char(self, char, arg=None):
        if char not in self.alfabeto:
            print(f"Caractere inválido: '{char}'")
            return False
        
        try:
            key = f"{self.estado_atual},{char}"
            proximo_estado = self.transicoes.get(key)
            if proximo_estado is not None:
                self.estado_atual, fx = proximo_estado
                #Process
                if fx is not None:
                    if arg is not None:
                        fx(arg)
                    else:
                        fx()
            else:
                pass
        except Exception as e:
            traceback_msg = traceback.format_exc()
            print(f"Erro: {e}")
            print(f"Traceback: {traceback_msg}")
        
            


    def reset(self):
        self.estado_atual = self.estado_inicial

def Cel2Char(cel_meta:CelulaModel)->Char:
    mao_barra = verify_maoBarra(cel_meta)
    extensao_cotovelo = verify_extensaoCotovelo(cel_meta)
    ultrapassar_barra = verify_ultrapassarBarra(cel_meta)
    movimento_quadrilPerna = verify_movimentoQuadrilPerna(cel_meta)
    char = Char(mao_barra=mao_barra, extensao_cotovelo=extensao_cotovelo, ultrapassar_barra=ultrapassar_barra, movimento_quadrilPerna=movimento_quadrilPerna)
    return char

def possibleChar(vets=None,vet=None,i=None):
    if i == None :
        i = len(vet)-1
    if i == 0:
        vets.append(vet)
        return vets
    else:
        if vet[i] == None:
            #
            vet[i] = True        
            vet1 = list(vet)
            possibleChar(vets=vets, vet=vet1, i=i-1)
            #
            vet[i] = False
            vet2 = list(vet)
            possibleChar(vets=vets, vet=vet2, i=i-1)
        else:
            possibleChar(vets=vets, vet=vet, i=i-1)
    return vets

