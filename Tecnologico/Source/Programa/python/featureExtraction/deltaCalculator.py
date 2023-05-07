import statistics
from typing import Any, List, Callable, Tuple

class DeltaCalculator:

    def __init__(self, data:List[Any] = []) -> None:
        self.data = data

    @staticmethod
    def get_mean(
        data:List[Any],
        extractor: Callable[[Any], float] = lambda data: data,
     ) -> float:
        '''Retorna a media'''
        values = [extractor(x) for x in data if x is not None]
        mean = statistics.mean(values)
        return mean

    @staticmethod
    def get_median(
        data:List[Any],
        extractor: Callable[[Any], float] = lambda data: data,
     ) -> float:
        '''Retorna a mediana'''
        values = [extractor(x) for x in data if x is not None]
        median = statistics.median(values)
        return median    

    @staticmethod
    def get_deviation(
            data:List[Any],
            extractor: Callable[[Any], float] = lambda data: data,
        ) -> float:
        '''Retorna o desvio padrao da amostra'''
        values = [extractor(x) for x in data if x is not None]
        standart_deviation = statistics.pstdev(values)
        return standart_deviation    