
class char:
    def __init__(self,mao_barra=None ,concentrica=None ,excentrica=None ,extensao_cotovelo=None ,ultrapassar_barra=None ,movimento_quadrilPerna=None ) -> None:
        self.mao_barra = mao_barra                              #Mao na Barra  
        self.concentrica = concentrica                          #Gradiente positivo     Concentrica  
        self.excentrica = excentrica                            #Gradiente negativo     Excentrica  
        self.extensao_cotovelo = extensao_cotovelo              #Extensão de Cotovelo  
        self.ultrapassar_barra = ultrapassar_barra              #Ultrapassar a barra  
        self.movimento_quadrilPerna = movimento_quadrilPerna    #Movimento de Quadril ou Perna  

    def processMetaFrame(sel):
        """Apartir dos meta-dados do frame preenche o "vetor caracter" """ 
        pass

    def process_mao_barra(self,meta):
        """Processa mao_barra apartir dos meta-dados do frame"""
        #pega os dados pos_d=get_right_wrist()
        #pega os dados pos_e=get_left_wrist()
        #define um valor de tolerancia
        #pega pos_bar
        #checa se pos_d e pos_e esta proximo o suficiente de posiBar
        #altera o valor de self.mao_barra

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