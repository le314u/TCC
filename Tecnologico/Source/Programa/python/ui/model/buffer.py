from typing import Any, List, Callable, Tuple
from ui.model.celulaModel import CelulaModel

class Buffer:

    def __init__(self, capacity:int=24, data: List[CelulaModel] = []) -> None:
        self.buffer:List[CelulaModel] = data #Uma lsita de Celulas
        self.capacity:int = capacity #Inteiro que representa a quantidade de frames faz um segmento por padrão é igual ao fps
      
    def size(self):
        return len(self.buffer)
    
    def set_cell(self, index:int, value:Any) -> None:
        '''Define o valor de uma celula do buffer'''
        self.buffer[index] = value

    def get_cell(self, index: int) -> CelulaModel:
        '''Retorna o valor de uma celula do buffer'''
        return self.buffer[index]

    def get_capacity(self):
        return self.capacity

    def position_fraction(self, n: int) -> int:
        '''Retorna o indice da celula que inicia a fração 'n' '''
        #Quantidade de frações do buffer
        max = len(self.buffer) // self.capacity
        if n > max:
            raise ValueError("O buffer nao tem essa quantidade de frações")
        #Aritimetica para saber qual celula começa a fração
        init = n * self.capacity
        return init
    
    def get_slice(self, interval:Tuple[int,int], extractor:Callable[[Any],Any]=lambda x:x) -> List:
        '''retorna uma parte do buffer'''
        start , end = interval
        def e (data):
            try:
                return extractor(data)
            except:
                return None
        values = [ extractor( self.buffer[i] )  for i in range(start, end, 1) ]
        ret = [ x for x in values if x != None ]
        return values
  