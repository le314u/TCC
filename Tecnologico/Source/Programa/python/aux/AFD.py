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
    return possibilities_0 +"\n"+ possibilities_1  # Retorna a combinação das possibilidades com "0" e "1"

def AlessB(A, B):  
    A_itens = str(A).split("\n")
    B_itens = str(B).split("\n")
    new_items = A_itens.copy()
    for item in B_itens:
        try:
            new_items.remove(item)
        except ValueError:
            pass
    return "\n".join(new_items)



def states(A,B):
    return AlessB( gen(A), gen(B) )

# Cria um objeto Digraph
dot = Digraph()



# Define os estados
dot.node('Preparacao', shape='circle')
dot.node('Inicio', shape='circle')
dot.node('Concentrica', shape='circle')
dot.node('Excentrica', shape='circle')
dot.node('Meta', shape='circle')
dot.node('Fim', shape='doublecircle')
dot.node('Erro', shape='circle')



#Não Houve a posição Inicial
label = gen([0, 0, "?", "?"])+"\n"
label += gen([1, 0, "?", "?"])+"\n"
label += gen([0, 1, "?", "?"])+"\n"
label += gen([1, 1, 0, 1])+"\n"
label += gen([1, 1, 1, 0])+"\n"
label += gen([1, 1, 1, 1])
dot.edge('Preparacao', 'Preparacao', label=label,  labelloc='t',fontsize="10") 
#Começou o exame
label = gen([1, 1, 0, 0])
dot.edge('Preparacao', 'Inicio', label=label,  labelloc='t',fontsize="10") 




#Iniciou a barra
label = gen([1, 0, 0, 0])
dot.edge('Inicio', 'Concentrica', label=label,  labelloc='t',fontsize="10")



#Movimento Concentrico
label = gen([1, 0, 0, 0])
dot.edge('Concentrica','Concentrica', label=label,  labelloc='t',fontsize="10") 
label = gen([1, 0, 1, 0])
dot.edge('Concentrica', 'Meta', label=label,  labelloc='t',fontsize="10") 



#Objetivo parcialmente atingido 
label = gen([1, 0, 1, 0])
dot.edge('Meta', 'Meta', label=label,  labelloc='t',fontsize="10") 
#Retornando para a posição inicial 
label = gen([1, 0, 0, 0])
dot.edge('Meta', 'Excentrica', label=label,  labelloc='t',fontsize="10") 
label = gen([1, 0, 0, 0])
dot.edge('Excentrica', 'Excentrica', label=label,  labelloc='t',fontsize="10") 
label = gen([1, 1, 0, 0])
dot.edge('Excentrica', 'Inicio', label=label,  labelloc='t',fontsize="10")


#Erro
label = AlessB(gen([1, "?", "?", 1]) , gen(["?", 1, 1, "?"]))
dot.edge('Inicio', 'Erro', label=label,  labelloc='t',fontsize="10") #retornando para a posição inicial 
dot.edge('Concentrica', 'Erro', label=label,  labelloc='t',fontsize="10") #retornando para a posição inicial 
dot.edge('Meta', 'Erro', label=label,  labelloc='t',fontsize="10") #retornando para a posição inicial 
dot.edge('Excentrica', 'Erro', label=label,  labelloc='t',fontsize="10") #retornando para a posição inicial 


#Erro -> Inicio
label = gen([1, 0, 0, 1])
dot.edge('Erro','Inicio',label=label,  labelloc='t',fontsize="10") #retornando para a posição inicial      

#anyway -> fim
label = AlessB(gen([0, "?", "?", "?"]) , gen(["?", 1, 1, "?"]))
dot.edge('Inicio', 'Fim', label=label,  labelloc='t',fontsize="10") #Encerra a avalicação
dot.edge('Concentrica', 'Fim', label=label,  labelloc='t',fontsize="10") #Encerra a avalicação
dot.edge('Meta', 'Fim', label=label,  labelloc='t',fontsize="10") #Encerra a avalicação
dot.edge('Excentrica', 'Fim', label=label,  labelloc='t',fontsize="10") #Encerra a avalicação
dot.edge('Erro','Fim',label=label,  labelloc='t',fontsize="10") #Encerra a avalicação     


# Renderiza o diagrama em um arquivo de imagem
dot.render('midia/afd_barra', format='png')