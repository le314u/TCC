
import traceback
import cv2
import numpy as np
import mediapipe as mp
from controller.featureExtraction.geometria import angle_point,segment,ponto_medio,rotate_segment,distance_line_line
from controller.processImg.debug import save_img, display_img, join_imgs,resize, matchGeral
from controller.processImg.filter import limiarizacao, pixelizacao, imagem_cinza, suavizacao, rotacao
from controller.processImg.mask import Mask
from model.featureExtraction.lineModel import LineModel 
from model.featureExtraction.poseModel import PoseModel,Segmento
from model.video.celulaModel import CelulaModel
from controller.processImg.others import count_white_pixels, count_discontinuities

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose

# Argumentos para mp_pose.Pose()
# STATIC_IMAGE_MODE  ->  Se definido como false, a solução trata as imagens de entrada como um fluxo de vídeo. Ele tentará detectar a pessoa mais proeminente nas primeiras imagens e, após uma detecção bem-sucedida, localiza ainda mais os marcos da pose. Em imagens subsequentes, ele simplesmente rastreia esses pontos de referência sem invocar outra detecção até que perca o rastreamento, reduzindo a computação e a latência. Se definido como true, a detecção de pessoas executa cada imagem de entrada, ideal para processar um lote de imagens estáticas, possivelmente não relacionadas. Padrão para false.
# MODEL_COMPLEXITY  ->  Complexidade do modelo marco postura: 0, 1 ou 2. A precisão do ponto de referência, bem como a latência de inferência, geralmente aumentam com a complexidade do modelo. Padrão para 1.
# SMOOTH_LANDMARKS  ->  Se definido como true, os filtros de solução representam pontos de referência em diferentes imagens de entrada para reduzir o jitter, mas são ignorados se static_image_mode também estiver definido como true. Padrão para true.
# ENABLE_SEGMENTATION  ->  Se definido como true, além dos marcos de pose, a solução também gera a máscara de segmentação. Padrão para false.
# SMOOTH_SEGMENTATION  ->  Se definido como true, a solução filtra as máscaras de segmentação em diferentes imagens de entrada para reduzir o jitter. Ignorado se enable_segmentation for false ou static_image_mode for true. Padrão para true.
# MIN_DETECTION_CONFIDENCE  ->  Valor de confiança mínimo ( [0.0, 1.0]) do modelo de detecção de pessoa para que a detecção seja considerada bem-sucedida. Padrão para 0.5.
# MIN_TRACKING_CONFIDENCE  ->  Valor de confiança mínimo ( [0.0, 1.0]) do modelo de rastreamento de pontos de referência para os pontos de referência de pose a serem considerados rastreados com sucesso, caso contrário, a detecção de pessoa será chamada automaticamente na próxima imagem de entrada. Configurá-lo com um valor mais alto pode aumentar a robustez da solução, às custas de uma latência mais alta. Ignorado se static_image_mode for true, em que a detecção de pessoas simplesmente é executada em todas as imagens. Padrão para 0.5.
pose_midia_pipe = mp_pose.Pose(
		static_image_mode=False,
		model_complexity=2,
		min_detection_confidence=0.3,
		min_tracking_confidence=0.75
	)


MASK = Mask()

class PosePoints():
    #Variavel de classe
    midia_pipe_ENUM = mp.solutions.pose.PoseLandmark
    pose_midia_pipe = pose_midia_pipe #Midia Pipe
    

    @staticmethod
    def extractPose(image):
        '''Retorna a Pose de acordo com midia Pipe'''
        return PosePoints.pose_midia_pipe.process(image)

    def __init__(self,frame) -> None:
        
        hight, width, _ = frame.shape
        poseTensor = PosePoints.extractPose(frame)

        rPoint = lambda point:(round(point.x*width) , round(point.y*hight) )
        access = lambda key: rPoint(poseTensor.pose_landmarks.landmark[PosePoints.midia_pipe_ENUM[key]])

        self.pose = PoseModel(
            access("LEFT_ANKLE"),
            access("LEFT_ELBOW"),
            access("LEFT_SHOULDER"),
            access("LEFT_HEEL"),
            access("LEFT_HIP"),
            access("LEFT_KNEE"),
            access("LEFT_WRIST"),
            access("LEFT_PINKY"),
            access("LEFT_INDEX"),
            access("LEFT_THUMB"),
            access("RIGHT_ANKLE"),
            access("RIGHT_ELBOW"),
            access("RIGHT_SHOULDER"),
            access("RIGHT_HEEL"),
            access("RIGHT_HIP"),
            access("RIGHT_KNEE"),
            access("RIGHT_WRIST"),
            access("RIGHT_PINKY"),
            access("RIGHT_INDEX"),
            access("RIGHT_THUMB")
        )


    def getPose(self)->PoseModel:
        return self.pose

def detectBar(frame) -> LineModel:
    '''Dado um frame retorna a barra'''
    img = frame.copy()
    altura, largura, _  = img.shape
    #converte em preto e branco
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY) 
    #Detecção de borda
    edges = cv2.Canny(gray,50,150,apertureSize = 3) 
    lines = cv2.HoughLines(edges,1,np.pi/180, 150)


    #Verifica a Orientação da reta
    tolerance = 10
    horizontal_lines = []
    for line in lines:
        rho, theta = line[0]
        pt1,pt2 = segment(rho,theta)
        pt1 = (0, pt1[1])
        angle = angle_point(pt1,pt2)
        # Verificar se é horizontal
        if abs(angle) < tolerance or abs(180-tolerance) < abs(angle):
            horizontal_lines.append(line)
    

    #Verifica a região de interesse
    section_line = []
    
    limit_sup = round(0.0 * altura) #round(0.07 * altura)
    limit_inf = round(0.3 * altura) #round(0.14 * altura)

    for line in horizontal_lines:
        rho,theta = line[0]
        points = segment(rho,theta,largura) 
        y1,y2 = (points[0][1],points[1][1])
        if all(y < limit_inf for y in [y1, y2]) and all(y > limit_sup for y in [y1, y2]):
            section_line.append(line)
    
    thickness = 1
   
    #Pega as duas linhas mais votadas
    #Esparasse que essas sejam as linhas delimitadores sup e inf
    def process_line(line):
        p1, p2 = segment(line[0][0], line[0][1], largura)
        return LineModel(*p1, *p2)

    first_line = process_line(section_line[0])
    second_line = process_line(section_line[1])

   
    
    thickness = distance_line_line(first_line, second_line)
    
    # #Verifica a linha mais alta
    real_line = section_line[0][0]
    for line in section_line:
        rho,theta = line[0]
        points = segment(rho,theta,largura) 
        x1,y1 = points[0]
        x2,y2 = points[1]
        val1 = y1

        rho,theta = real_line
        points = segment(rho,theta,largura) 
        x1,y1 = points[0]
        x2,y2 = points[1]
        val2 = y1

        if( val1 < val2  ):
            real_line = line[0]
    
    
    #Preparando o retorno
    rho,theta = real_line
    points = segment(rho,theta,largura) 
    x1,y1 = points[0]
    x2,y2 = points[1]
    offSet = int(thickness/2)

    return LineModel(x1,y1+offSet, x2,y2+offSet, thickness=int(thickness))

def verify_maoBarra(cel:CelulaModel):
    #Constante
    # size = 30    # Tamanho do kernel de Blur e Pixelização
    limiar = 50    # Definir um limiar para identificar a descontinuidade
    x,y=(0,1)

    #Data
    frame = cel.getFrame()
    barra = cel.getLine()
    pose = cel.getPose()
    altura, largura  = frame.shape[:2]

    center_point = ponto_medio(*pose.get_left_elbow(),*pose.get_right_elbow())
    center_start = (round(center_point[0]), round(center_point[1]-largura))
    center_end = (round(center_point[0]), round(center_point[1]+largura))

    #Mascaras
    size = barra.getThickness()
    mask_frame = MASK.getMask()
    mask_barra = MASK.createLineMask(frame,barra.getStart(),barra.getEnd(), thickness=size)
    mask_center = MASK.createLineMask(frame,center_start,center_end, size*1.5)
    mask_center = cv2.bitwise_not(mask_center)


    newFrame = MASK.putMask(frame, mask_frame)
   
    #Destaca a pele
    skin = MASK.highLight_skin(newFrame)

    # Converter a imagem apenas para P&B
    gray = imagem_cinza(skin)
    limited = limiarizacao(gray,limiar)
    
    # Aplica o desfoque
    blur = suavizacao(limited, size/2 )
    limited2 = limiarizacao(blur,limiar)

    #Aplica a pixelização
    pixel = pixelizacao(limited2,size)
    limited3 = limiarizacao(pixel,limiar)

    #Aplica as Mascaras da area de interesse
    only_bar_region = cv2.bitwise_and(mask_barra, limited3)
    only_hands = MASK.putMask(only_bar_region, mask_center)

    # Aplicar o operador de Sobel
    gradient_x = cv2.Sobel(only_hands, cv2.CV_64F, 1, 0, ksize=3)
    gradient_y = cv2.Sobel(only_hands, cv2.CV_64F, 0, 1, ksize=3)

    # Calcular o módulo do gradiente
    gradient = np.sqrt(gradient_x ** 2 + gradient_y ** 2)
    
    # Verificar a descontinuidade em cada pixel
    descontinuidade = gradient > limiar

    # Aplicar um limiar para obter uma imagem binária
    gradient_binary = np.uint8(gradient)


    # Encontrar contornos na metade esquerda da imagem
    imagem_resultante_esquerda = only_hands.copy()
    imagem_resultante_esquerda[:, :center_start[x]] = 0
    contornos_esquerda, _ = cv2.findContours(imagem_resultante_esquerda, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Encontrar contornos na metade esquerda da imagem
    imagem_resultante_direita = only_hands.copy()
    imagem_resultante_direita[:, center_end[x]:] = 0
    contornos_direita, _ = cv2.findContours(imagem_resultante_direita, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    ret = len(contornos_esquerda) >= 1 and len(contornos_direita) >= 1
    return ret

def verify_extensaoCotovelo(cel: CelulaModel):
    '''Verifica quando o cotovelo esta esticado'''
    
    #Alias
    x,y = (0,1)
    limite=100
    limiar_angulo = 13    # Definir um limiar para identificar a descontinuidade

    #So analisa a extensão caso a mão esteja na barra
    mao_barra = cel.getData().get("mao_barra")
    if( not mao_barra):
        return False
    
    #Pego o valor minimo do peito quando a mão esta na barra necessita de 'verify_meta_extensao'
    menor_ombro_esq = CelulaModel.getAggregate("menor_ombro_esq")
    menor_ombro_dir = CelulaModel.getAggregate("menor_ombro_dir")

    #Pega o valor atual do peito na celula
    ombro_esq = cel.getPose().get_left_shoulder()
    ombro_dir = cel.getPose().get_right_shoulder()

    #Inicializando a classe 
    if(menor_ombro_esq is None):
        CelulaModel.setAggregate("menor_ombro_esq",ombro_esq)
        menor_ombro_esq = ombro_esq
    if(menor_ombro_dir is None):
        CelulaModel.setAggregate("menor_ombro_dir",ombro_dir)
        menor_ombro_dir = ombro_dir
    
    anguloBracoEsq = cel.getData().getAnguloBracoEsq()
    anguloBracoDir = cel.getData().getAnguloBracoDir()

    offset_braco = abs(anguloBracoEsq - anguloBracoDir)
    limiar_aceitavel = limiar_angulo+offset_braco

    check_1 = anguloBracoEsq < limiar_aceitavel and anguloBracoDir < limiar_aceitavel
    check_2 = (abs(ombro_esq[y] - menor_ombro_esq[y]) < limite) or (abs(ombro_dir[y] - menor_ombro_dir[y]) < limite)
    check = check_1 and check_2
    cel.getData().set("extensao_cotovelo",check)
    return check

def verify_ultrapassarBarra(cel: CelulaModel):
    #Verifica se encontrou algo acima da barra (cabeça)
    
    #So analisa a extensão caso a mão esteja na barra
    mao_barra = cel.getData().get("mao_barra")
    if( not mao_barra):
        return False
    
    #Alias
    x,y = (0,1)

    #Data
    frame = cel.getFrame()
    barra = cel.getLine()
    pose = cel.getPose()

    #Constante
    size = cel.getLine().getThickness()
    limiar = 50    # Definir um limiar para identificar a descontinuidade
    limiar_angulo = 5    # Definir um limiar para identificar a flexão total de cotovelo
    limiar_barra = round(size*1.5)   # Distancia maxima entre a barra e o ombro

    barra_start = barra.getStart()
    ombro_start = pose.get_left_shoulder()
    ombro_end = pose.get_right_shoulder()
    anguloBracoEsq = cel.getData().getAnguloBracoEsq()
    anguloBracoDir = cel.getData().getAnguloBracoDir()

    extract_height = lambda ponto: ponto[y]
    extract_width = lambda ponto: ponto[x]

    offset_esq = abs(extract_height(barra_start) - extract_height(ombro_start))
    offset_dir = abs(extract_height(barra_start) - extract_height(ombro_end))
    
    #So continua a analise caso o peito esteja proximo da barra
    peito_na_barra = (offset_esq < limiar_barra) or (offset_dir < limiar_barra)
    if( not peito_na_barra):
        return False
    
    #So continua a analise caso o braço esteja dobrado
    braco_dobrado = (anguloBracoEsq > (180-limiar_angulo)) or (anguloBracoDir > (180-limiar_angulo))
    if( not braco_dobrado):
        return False

    #Cria a mascara para a cabeça acima da barra
    center_point = ponto_medio(*ombro_start,*ombro_end)   
    size_block = abs(round( (ombro_end[0]-ombro_start[0])/3))
    mask_head = MASK.createBlockMask(frame, 
        ( 
            round(center_point[0]-(size_block/2)),
            round(barra_start[1]-(size_block*2))), 
        (
            round(center_point[0]+size_block/2),
            round(barra_start[1]-(size/2)-(size_block*1.5)))
    )

    #Destaca a pele
    skin = MASK.highLight_skin(frame)
   
    # Converter a imagem apenas para P&B
    gray = imagem_cinza(skin)
    limited = limiarizacao(gray,limiar)

    #Pixeliza a imagem
    #pixel = pixelizacao(limited, round(size_block/2))
    #limited2 = limiarizacao(pixel,limiar)    

    #pixel2 = pixelizacao(limited, round(size_block))
    #limited3 = limiarizacao(pixel2,limiar)    

    
    #Aplica as Mascaras da area de interesse
    only_interesse = cv2.bitwise_and(mask_head, limited)
    only_interesse_pix = pixelizacao(only_interesse, round(size_block/4))

    # Verifique se há pixels brancos na imagem
    pixels_brancos = cv2.countNonZero(only_interesse_pix)

    has_head = pixels_brancos > 0

    cel.getData().set("offSet_Peito_Barra",(offset_esq, offset_dir))
    cel.getData().set("peito_na_barra",(peito_na_barra))
    cel.getData().set("braco_dobrado",(braco_dobrado))
    cel.getData().set("has_head",(has_head))
    
    return (peito_na_barra and braco_dobrado and has_head)

def verify_movimentoQuadrilPerna(cel: CelulaModel):
    limiar_angulo = 15    # Definir um limiar para identificar a descontinuidade

    anguloPernaEsq = cel.getData().getAnguloPernaEsq()
    anguloPernaDir = cel.getData().getAnguloPernaDir()
    pernaDobrada = (anguloPernaEsq > limiar_angulo) or (anguloPernaDir > limiar_angulo)
    cel.getData().set("pernaDobrada",pernaDobrada)
    return pernaDobrada