
import cv2
import numpy as np
import mediapipe as mp
from controller.featureExtraction.geometria import angle_point,segment
from controller.processImg.debug import save_img, display_img, display_imgs
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
# MODEL_COMPLEXITY  ->  Complexidade do modelo marco postura: 0, 1ou 2. A precisão do ponto de referência, bem como a latência de inferência, geralmente aumentam com a complexidade do modelo. Padrão para 1.
# SMOOTH_LANDMARKS  ->  Se definido como true, os filtros de solução representam pontos de referência em diferentes imagens de entrada para reduzir o jitter, mas são ignorados se static_image_mode também estiver definido como true. Padrão para true.
# ENABLE_SEGMENTATION  ->  Se definido como true, além dos marcos de pose, a solução também gera a máscara de segmentação. Padrão para false.
# SMOOTH_SEGMENTATION  ->  Se definido como true, a solução filtra as máscaras de segmentação em diferentes imagens de entrada para reduzir o jitter. Ignorado se enable_segmentation for false ou static_image_mode for true. Padrão para true.
# MIN_DETECTION_CONFIDENCE  ->  Valor de confiança mínimo ( [0.0, 1.0]) do modelo de detecção de pessoa para que a detecção seja considerada bem-sucedida. Padrão para 0.5.
# MIN_TRACKING_CONFIDENCE  ->  Valor de confiança mínimo ( [0.0, 1.0]) do modelo de rastreamento de pontos de referência para os pontos de referência de pose a serem considerados rastreados com sucesso, caso contrário, a detecção de pessoa será chamada automaticamente na próxima imagem de entrada. Configurá-lo com um valor mais alto pode aumentar a robustez da solução, às custas de uma latência mais alta. Ignorado se static_image_mode for true, em que a detecção de pessoas simplesmente é executada em todas as imagens. Padrão para 0.5.
pose_midia_pipe = mp_pose.Pose(
		static_image_mode=True,
		enable_segmentation=True,
		model_complexity=2,
		min_detection_confidence=0.5,
		min_tracking_confidence=0.5
	)


MASK = Mask()

class PosePoints():
    #Variavel de classe
    midia_pipe_ENUM = mp.solutions.pose.PoseLandmark
    pose_midia_pipe = pose_midia_pipe #Midia Pipe
    

    @staticmethod
    def extractPose(image):
        '''Retorna a Pose de acordo com tensor Flow'''
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
            access("RIGHT_ANKLE"),
            access("RIGHT_ELBOW"),
            access("RIGHT_SHOULDER"),
            access("RIGHT_HEEL"),
            access("RIGHT_HIP"),
            access("RIGHT_KNEE"),
            access("RIGHT_WRIST"),
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
    lines = cv2.HoughLines(edges,1,np.pi/180, 100)

    tolerance = 8
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
    limit_sup = round(0.03 * altura) #round(0.07 * altura)
    limit_inf = round(0.18 * altura) #round(0.14 * altura)
    for line in horizontal_lines:
        rho,theta = line[0]
        points = segment(rho,theta,largura) 
        x1,y1 = points[0]
        x2,y2 = points[1]
        if all(y < limit_inf for y in [y1, y2]) and all(y > limit_sup for y in [y1, y2]):
            section_line.append(line)
    
    #Verifica a maior linha
    real_line = section_line[0][0]
    for line in section_line:
        rho,theta = line[0]
        points = segment(rho,theta,largura) 
        x1,y1 = points[0]
        x2,y2 = points[1]
        val1 = y2

        rho,theta = real_line
        points = segment(rho,theta,largura) 
        x1,y1 = points[0]
        x2,y2 = points[1]
        val2 = y2

        
        if(val2 > val1 ):
            real_line = line[0]
            
    #     # Exibindo a imagem
    
    real_line = real_line
    #Preparando o retorno
    rho,theta = real_line
    points = segment(rho,theta,largura) 
    x1,y1 = points[0]
    x2,y2 = points[1]
    return LineModel(x1,y1,x2,y2)

def verify_maoBarra(cel:CelulaModel):
    size = 10*3    # Tamanho do kernel de Blur e Pixelização
    limiar = 100    # Definir um limiar para identificar a descontinuidade

    #Start
    frame = cel.getFrame()
    barra = cel.getLine()
    mask_barra = MASK.createLineMask(frame,barra.getStart(),barra.getEnd(),round(size/2))
    mask_frame = MASK.getMask()
    newFrame = MASK.putMask(frame, mask_frame)
    
    # Converter a imagem para o espaço de cores HSV
    imagem_hsv = cv2.cvtColor(newFrame, cv2.COLOR_BGR2HSV)

    #Definir os intervalos de cor da pele
    lower_skin = np.array([0, 25, 0], dtype=np.uint8)
    upper_skin = np.array([20, 255, 255], dtype=np.uint8)

    # Aplicar uma máscara para obter apenas a parte da cor da imagem
    mascara = cv2.inRange(imagem_hsv, lower_skin, upper_skin)
    canal_x = cv2.bitwise_and(frame, frame, mask=mascara)

    # Converter a imagem apenas para P&B
    gray = imagem_cinza(canal_x)
    limited = limiarizacao(gray,limiar)
    # Aplcia um desfoque
    blur = suavizacao(limited,size)
    limited = limiarizacao(blur,limiar)

    #Aplica a pixelização
    pixel = pixelizacao(limited,size)

    #Aplica a Mascara da area de interesse
    only_hand = cv2.bitwise_and(mask_barra, pixel)

    # Aplicar o operador de Sobel
    gradient_x = cv2.Sobel(only_hand, cv2.CV_64F, 1, 0, ksize=3)
    gradient_y = cv2.Sobel(only_hand, cv2.CV_64F, 0, 1, ksize=3)

    # Calcular o módulo do gradiente
    gradient = np.sqrt(gradient_x ** 2 + gradient_y ** 2)
    
    # Verificar a descontinuidade em cada pixel
    descontinuidade = gradient > limiar

    # Aplicar um limiar para obter uma imagem binária
    gradient_binary = np.uint8(only_hand)
    limited = limiarizacao(gradient_binary,limiar)

    # Encontrar contornos na imagem binária
    contornos, hier = cv2.findContours(limited, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # if(cel.getData().get("id")==131):
    #     print(len(contornos))
    #     display_img(limited )


    if(len(contornos) != 2):
        print(f"   {cel.getData().get('id')} {len(contornos)}")
        display_img(limited )


    # Verificar se houve ou não descontinuidade na imagem ou seja se a mão esta ou não na barra
    # Se houve descontinuidade do preto logo algo estava na barra 
    # So valida se encontrar 2 contornos ou mais ou seja as 2 mãos
  
    
    return len(contornos) >=2

