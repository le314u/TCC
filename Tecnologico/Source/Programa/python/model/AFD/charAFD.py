from model.video.celulaModel import CelulaModel
from controller.featureExtraction.geometria import distance_point_line

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
        pass

    def process_mao_barra(self, cel_meta:CelulaModel):
        """Processa mao_barra apartir dos meta-dados do frame"""

        #define um valor de tolerancia
        tolerancia = 150
        pose = cel_meta.getPose()
        pos_d=pose.get_right_wrist()
        pos_e=pose.get_left_wrist()
        barra = cel_meta.getLine()
        dis_d = distance_point_line(pos_d,barra)
        dis_e = distance_point_line(pos_e,barra)
        #checa se pos_d e pos_e esta proximo o suficiente de posiBar
        if( dis_d <= tolerancia and dis_e <= tolerancia):
            self.mao_barra = 1
        else:
            self.mao_barra = 0
            
        #verifica o tamanho do membro: ombro ate punho
        #Se diminuir significa uma anomalia e tem que ter uma tolerancia maior  em relação a barra
        pass

    def process_concentrica(self,meta):
        """Processa concentrica apartir dos meta-dados do frame"""
        #pega os dados 
        pass

    def process_excentrica(self,meta):
        """Processa excentrica apartir dos meta-dados do frame"""
        pass

    def process_extensao_cotovelo(self,meta):
        """Processa extensao_cotovelo apartir dos meta-dados do frame"""
        pass

    def process_ultrapassar_barra(self,meta):
        """Processa ultrapassar_barra apartir dos meta-dados do frame"""
        pass

    def process_movimento_quadrilPerna(self,meta):
        """Processa movimento_quadrilPerna apartir dos meta-dados do frame"""
        pass

    def get(self):
        return self.getChar

    def getChar(self):
        return [ self.mao_barra, self.concentrica, self.excentrica, self.extensao_cotovelo, self.ultrapassar_barra, self.movimento_quadrilPerna ]
    
    def __str__(self) -> str:
        attributes = [str(attr) if not isinstance(attr, str) else f'"{attr}"' for attr in [self.mao_barra, self.concentrica, self.excentrica, self.extensao_cotovelo, self.ultrapassar_barra, self.movimento_quadrilPerna]]
        return f"[{', '.join(attributes)}]"