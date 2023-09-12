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
    possibleChar_Rec(vets,vet,i)
    remove_duplicate_sublists(vets)

def possibleChar_Rec(vets=None,vet=None,i=None):
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
            possibleChar_Rec(vets=vets, vet=vet1, i=i-1)
            #
            vet[i] = False
            vet2 = list(vet)
            possibleChar_Rec(vets=vets, vet=vet2, i=i-1)
        else:
            possibleChar_Rec(vets=vets, vet=vet, i=i-1)
    return vets

def remove_duplicate_sublists(lst):
    unique_lst = []
    for sublist in lst:
        if sublist not in unique_lst:
            unique_lst.append(sublist)
    #Sobreescreve a lista
    lst.clear()  # Clear the original list
    lst.extend(unique_lst)  # Add the unique sublists back to the original list

def remove_possibleChar(vets=None, char=None):
    try:
        vets.remove(char)
    except ValueError:
        pass  # char não encontrado, nenhum erro é lançado

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
            "[True, False, False, False]",
            "[True, False, False, True]",
            "[True, False, True, False]",
            "[True, False, True, True]",
            "[True, True, False, False]",
            "[True, True, False, True]",
            # Impossivel extender o cotovelo e ultrapassar a barra
            #"[True, True, True, False]",
            #"[True, True, True, True]",
            #"[False, True, True, False]", 
            #"[False, True, True, True]",
        ]
        # Definir os estados do AFD
        estados = ['preparacao','inicio', 'extensao,' 'meta','concentrica','excentrica','erro', 'fim']
        # Definir o estado inicial do AFD
        estado_inicial = 'preparacao'
        # Definir os estados finais do AFD
        estados_finais = ['fim']
        # Definir as transições de estado do AFD
        transicoes = {}
        #Função que facilita Multi transiçoes de state->end_point com uma lista de chars
        transition = lambda state, chars, end_point, fx: [transicoes.update({f"{state},{str(char)}": (end_point, fx)}) for char in chars]

        # preparacao -> preparacao
        preparacao2preparacao = []
        possibleChar(vets=preparacao2preparacao,vet=[False, False, None, None])
        possibleChar(vets=preparacao2preparacao,vet=[True, False, None, None])
        possibleChar(vets=preparacao2preparacao,vet=[False, True, None, None])
        possibleChar(vets=preparacao2preparacao,vet=[True, True, None, True])
        possibleChar(vets=preparacao2preparacao,vet=[True, True, True, None])
        transition(state="preparacao",end_point="preparacao",fx=lambda x:None,chars=preparacao2preparacao )

        # preparacao -> inicio
        preparacao2inicio = [True, True, False, False]
        transition(state="preparacao",end_point="inicio",fx=lambda x:None,chars=[preparacao2inicio] )

        # inicio -> inicio
        inicio2inicio = [True, True, False, False]
        transition(state="inicio",end_point="inicio",fx=lambda x:None,chars=[inicio2inicio] )

        # inicio -> concentrica
        inicio2concentrica = [True, False, False, False]
        transition(state="inicio",end_point="concentrica",fx=lambda x:None,chars=[inicio2concentrica] )

        # concentrica -> meta
        def fx(cel:CelulaModel):
           qtd = cel.getData().getQtdMovimentos()
           cel.getData().setQtdMovimentos(int(qtd)+1)
           DataModel.agregate["aux"] = DataModel.agregate["aux"] +1
        
        concentrica2meta = [True,False,True,False]
        transition(state="concentrica",end_point="meta",fx=fx,chars=[concentrica2meta] )

        # meta -> excentrica
        meta2excentrica = [True,False,False,False]
        transition(state="meta",end_point="excentrica",fx=lambda x:None,chars=[meta2excentrica] )

        # Ação Invalida  -> erro
        erro = []
        possibleChar(vets=erro,vet=[True,None,None,True])
        remove_possibleChar(vets=erro,char=[True,True,True,True])
        transition(state="inicio",end_point="erro",fx=lambda x:None,chars=erro )
        transition(state="concentrica",end_point="erro",fx=lambda x:None,chars=erro )
        transition(state="meta",end_point="erro",fx=lambda x:None,chars=erro )
        transition(state="excentrica",end_point="erro",fx=lambda x:None,chars=erro )
        transition(state="erro",end_point="erro",fx=lambda x:None,chars=erro )

        # erro -> inicio
        erro2inicio = [True,True,False,False]
        transition(state="erro",end_point="inicio",fx=lambda x:None,chars=[erro2inicio] )

        # anyway -> fim
        fim = []
        possibleChar(vets=fim,vet=[False,None,None,None])
        remove_possibleChar(vets=fim,char=[False,True,True,True])
        remove_possibleChar(vets=fim,char=[False,True,True,False])

        transition(state="inicio",end_point="fim",fx=lambda x:None,chars=fim )
        transition(state="concentrica",end_point="fim",fx=lambda x:None,chars=fim )
        transition(state="meta",end_point="fim",fx=lambda x:None,chars=fim )
        transition(state="excentrica",end_point="fim",fx=lambda x:None,chars=fim )

        return Machine(alfabeto,estados,estado_inicial,estados_finais,transicoes)
    except:
        return None


