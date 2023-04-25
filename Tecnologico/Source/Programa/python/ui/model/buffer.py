from typing import List, Callable

class BufferAnalyzer:

    def __init__(self, fps: int, data: List[float] = []) -> None:
        self.buffer = data
        self.fps = fps
    
    def set_cell(self, index: int, value: float) -> None:
        '''Define o valor de uma celula do buffer'''
        self.buffer[index] = value

    def get_cell(self, index: int) -> object:
        '''Retorna o valor de uma celula do buffer'''
        return self.buffer[index]

    def position_fraction(self, n: int) -> int:
        '''Retorna o indice da celula que inicia a fração 'n' '''
        #Quantidade de frações do buffer
        max = len(self.buffer) // self.fps
        if n > max:
            raise ValueError("O buffer nao tem essa quantidade de frações")
        #Aritimetica para saber qual celula começa a fração
        init = n * self.fps
        return init
    
    def get_mean(self, fraction:int = 0, extractor: Callable[[int], float] = None) -> float:
        '''Retorna a media'''
        start = self.position_fraction(fraction)
        #Calcula a media 
        values = [extractor(i) for i in range(start, start+self.fps)]
        media = sum(values) / self.fps
        return media

    def get_derivative(self, fraction:int = 0, extractor: Callable[[int], float] = None) -> float:
        '''Retorna a derivada no segmento de reta'''
        start = self.position_fraction(fraction)
        values = [extractor(i) for i in range(start, start+self.fps)]
        #Variação de valor
        dV = lambda x : extractor(x+1) - extractor(x)
        #Variação de valor no Range
        sum = 0
        for i in range(self.fps-1):
            sum = sum + dV(i)
        #Calcula a derivada dividindo a variação de valor pela variação de tempo 
        derivada = sum / (self.fps-1)
        return derivada