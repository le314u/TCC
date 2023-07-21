from model.video.celulaModel import CelulaModel
from controller.featureExtraction.geometria import distance_point_line
from controller.featureExtraction.objectDetector import verify_maoBarra,verify_extensaoCotovelo,verify_ultrapassarBarra,verify_movimentoQuadrilPerna

class charAFD:
    def __init__(self, cel_meta:CelulaModel = None, mao_barra=None ,concentrica=None ,excentrica=None ,extensao_cotovelo=None ,ultrapassar_barra=None ,movimento_quadrilPerna=None ) -> None:
        self.mao_barra = mao_barra                              #Mao na Barra  
        self.concentrica = concentrica                          #Gradiente positivo     Concentrica  
        self.excentrica = excentrica                            #Gradiente negativo     Excentrica  
        self.extensao_cotovelo = extensao_cotovelo              #Extensão de Cotovelo  
        self.ultrapassar_barra = ultrapassar_barra              #Ultrapassar a barra  
        self.movimento_quadrilPerna = movimento_quadrilPerna    #Movimento de Quadril ou Perna  
        self.processMetaFrame(cel_meta)
    
    def __str__(self) -> str:
        return str(self.getChar())

    def processMetaFrame(self, cel_meta:CelulaModel):
        """Apartir dos meta-dados do frame preenche o "vetor caracter" """ 
        self.process_mao_barra(cel_meta)
        self.process_extensao_cotovelo(cel_meta)
        self.process_ultrapassar_barra(cel_meta)
        self.process_movimento_quadrilPerna(cel_meta)
        self.process_concentrica(cel_meta)
        self.process_excentrica(cel_meta)
        pass

    def process_mao_barra(self, cel_meta:CelulaModel):
        """Processa mao_barra apartir dos meta-dados do frame"""
        self.mao_barra = verify_maoBarra(cel_meta)
        
    def process_concentrica(self,cel_meta):
        """Processa concentrica apartir dos meta-dados do frame"""
        #pega os dados 
        pass

    def process_excentrica(self,cel_meta):
        """Processa excentrica apartir dos meta-dados do frame"""
        pass

    def process_extensao_cotovelo(self,cel_meta:CelulaModel):
        """Processa extensao_cotovelo apartir dos meta-dados do frame ou seja se so braços estão ou não esticados"""
        self.extensao_cotovelo = verify_extensaoCotovelo(cel_meta)

    def process_ultrapassar_barra(self,cel_meta:CelulaModel):
        """Processa ultrapassar_barra apartir dos meta-dados do frame"""
        self.ultrapassar_barra = verify_ultrapassarBarra(cel_meta)

    def process_movimento_quadrilPerna(self,cel_meta):
        """Processa movimento_quadrilPerna apartir dos meta-dados do frame"""
        self.movimento_quadrilPerna = verify_movimentoQuadrilPerna(cel_meta)
        pass

    def get(self):
        return self.getChar

    def getChar(self):
        return [ self.mao_barra, self.concentrica, self.excentrica, self.extensao_cotovelo, self.ultrapassar_barra, self.movimento_quadrilPerna ]
    
    def __str__(self) -> str:
        attributes = [str(attr) if not isinstance(attr, str) else f'"{attr}"' for attr in [self.mao_barra, self.concentrica, self.excentrica, self.extensao_cotovelo, self.ultrapassar_barra, self.movimento_quadrilPerna]]
        return f"[{', '.join(attributes)}]"