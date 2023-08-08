import traceback
from model.featureExtraction.dataModel import DataModel
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


def create_AFD():
    '''Processa o Frame'''
    try:  
        # Definir o alfabeto do AFD (caracteres válidos para a entrada)
        alfabeto = [
            "[False, False, False, False]",
            "[False, False, False, True]",
            "[False, False, True, False]",
            "[False, False, True, True]",
            "[False, True, False, False]",
            "[False, True, False, True]",
            "[False, True, True, False]",
            "[False, True, True, True]",
            "[True, False, False, False]",
            "[True, False, False, True]",
            "[True, False, True, False]",
            "[True, False, True, True]",
            "[True, True, False, False]",
            "[True, True, False, True]",
            "[True, True, True, False]",
            "[True, True, True, True]",
        ]
        # Definir os estados do AFD
        estados = ['preparando','inicio', 'extensao,' 'meta','concentrica','excentrica','erro', 'fim']
        # Definir o estado inicial do AFD
        estado_inicial = 'preparando'
        # Definir os estados finais do AFD
        estados_finais = ['fim']
        # Definir as transições de estado do AFD
        transicoes = {}
        #Função que facilita Multi transiçoes de state->end_point com uma lista de chars
        transition = lambda state, chars, end_point, fx: [transicoes.update({f"{state},{str(char)}": (end_point, fx)}) for char in chars]
        # def transition(state,chars,end_point,fx):
        #     for char in chars:
        #         s = f"{state},{str(char)}"
        #         transicoes[s]=(end_point,fx)


        # preparando -> inicio
        char = [True, True, False, False]
        transition(state="preparando",end_point="inicio",fx=lambda x:None,chars=[char] )

        # inicio -> inicio
        vets = []
        possibleChar(vets=vets,vet=[False, False, None, None])
        possibleChar(vets=vets,vet=[True, False, None, None])
        possibleChar(vets=vets,vet=[False, True, None, None])
        transition(state="inicio",end_point="inicio",fx=lambda x:None,chars=vets )

        # inicio -> concentrica
        char = [True, False, False, False]
        transition(state="inicio",end_point="concentrica",fx=lambda x:None,chars=[char] )

        # concentrica -> meta
        def fx(cel:CelulaModel):
           qtd = cel.getData().getQtdMovimentos()
           cel.getData().setQtdMovimentos(int(qtd)+1)
           DataModel.agregate["aux"] = DataModel.agregate["aux"] +1
        char = [True,False,True,False]
        transition(state="concentrica",end_point="meta",fx=fx,chars=[char] )

        # meta -> excentrica
        char = [True,False,False,False]
        transition(state="meta",end_point="excentrica",fx=lambda x:None,chars=[char] )

        # Ação Invalida  -> erro
        vets = []
        possibleChar(vets=vets,vet=[True,None,None,True])
        transition(state="inicio",end_point="erro",fx=lambda x:None,chars=vets )
        transition(state="concentrica",end_point="erro",fx=lambda x:None,chars=vets )
        transition(state="meta",end_point="erro",fx=lambda x:None,chars=vets )
        transition(state="excentrica",end_point="erro",fx=lambda x:None,chars=vets )

        # erro -> inicio
        char = [True,True,False,False]
        transition(state="erro",end_point="inicio",fx=lambda x:None,chars=[char] )

        # anyway -> fim
        vets = []
        possibleChar(vets=vets,vet=[False,None,None,None])
        transition(state="inicio",end_point="fim",fx=lambda x:None,chars=vets )
        transition(state="concentrica",end_point="fim",fx=lambda x:None,chars=vets )
        transition(state="meta",end_point="fim",fx=lambda x:None,chars=vets )
        transition(state="excentrica",end_point="fim",fx=lambda x:None,chars=vets )

        return Machine(alfabeto,estados,estado_inicial,estados_finais,transicoes)
    except:
        return None


