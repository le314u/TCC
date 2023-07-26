from graphviz import Digraph
import re

class char:
    def __init__(self,mao_barra,extensao_cotovelo,ultrapassar_barra,movimento_quadrilPerna) -> None:
        self.mao_barra = mao_barra         #Mao na Barra  
        self.extensao_cotovelo = extensao_cotovelo         #Extensão de Cotovelo  
        self.ultrapassar_barra = ultrapassar_barra         #Ultrapassar a barra  
        self.movimento_quadrilPerna = movimento_quadrilPerna         #Movimento de Quadril ou Perna  

    def get(self):
        return [ self.mao_barra, self.extensao_cotovelo, self.ultrapassar_barra, self.movimento_quadrilPerna ]

    def __str__(self) -> str:
        attributes = [str(attr) if not isinstance(attr, str) else f'"{attr}"' for attr in self.get()]
        return f"[{', '.join(attributes)}]"

def gen(lst):
    if isinstance(lst,char):
        lst = lst.get()
    if "?" not in lst:
        return str([lst.copy()])[1:-1]
    index = lst.index("?")
    lst[index] = 0
    possibilities_0 = gen(lst)  # Chamada recursiva com "0"
    lst[index] = 1
    possibilities_1 = gen(lst)  # Chamada recursiva com "1"
    lst[index] = "?"  # Restaura o caractere "?"
    return possibilities_0 +", "+ possibilities_1  # Retorna a combinação das possibilidades com "0" e "1"

def AlessB(A,B):
    A = str(A)
    B = str(B)
    # Remove os colchetes no início e no final da string
    B = re.sub(r'^\[|\]$', '', B)
    # Separa a string em listas usando vírgulas e colchetes como separadores
    B = re.split(r'\],\s*\[', B)
    for vet in B:
        A = A.replace(f"[{str(vet)}]","")
    return A

def states(A,B):
    return AlessB( gen(A), gen(B) )

# Cria um objeto Digraph
dot = Digraph()

# Define os estados
dot.node('Start', shape='point')
dot.node('Inicio', shape='doublecircle')
dot.node('Concentrica', shape='doublecircle')
dot.node('Excentrica', shape='doublecircle')
dot.node('Meta', shape='doublecircle')
dot.node('Fim', shape='doublecircle')
dot.node('Erro', shape='doublecircle')

#Preparando
label = gen([0, 0, "?", "?"]) + gen([1, 0, "?", "?"]) + gen([0, 1, "?", "?"])
dot.edge('Start', 'Start', label=label) #Não Houve a posição Inicial

#Passo a Passo
label = gen([1, 1, 0, 0])
dot.edge('Start', 'Inicio', label=label) #começou o exame

label = gen([1, 0, 0, 0])
dot.edge('Inicio', 'Concentrica', label=label) #iniciou a barra

label = gen([1, 0, 1, 0])
dot.edge('Concentrica', 'Meta', label=label) #objetivo parcialmente atingido 

label = gen([1, 0, 0, 0])
dot.edge('Meta', 'Excentrica', label=label) #retornando para a posição inicial 

label = gen([1, 1, 0, 0])
dot.edge('Excentrica', 'Inicio', label=label) #retornando para a posição inicial 


#Erro
label = gen([1, "?", "?", 1])
dot.edge('Inicio', 'Erro', label=label) #retornando para a posição inicial 
dot.edge('Concentrica', 'Erro', label=label) #retornando para a posição inicial 
dot.edge('Meta', 'Erro', label=label) #retornando para a posição inicial 
dot.edge('Excentrica', 'Erro', label=label) #retornando para a posição inicial 

#Erro -> Inicio
label = gen([1, 0, 0, 1])
dot.edge('Erro','Inicio',label=label) #retornando para a posição inicial      

#anyway -> fim
label = gen([0, "?", "?", "?"])
dot.edge('Inicio', 'Fim', label=label) #retornando para a posição inicial 
dot.edge('Concentrica', 'Fim', label=label) #retornando para a posição inicial 
dot.edge('Meta', 'Fim', label=label) #retornando para a posição inicial 
dot.edge('Excentrica', 'Fim', label=label) #retornando para a posição inicial 

# Renderiza o diagrama em um arquivo de imagem
dot.render('midia/afd_barra', format='png')