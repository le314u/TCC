import cv2
import numpy as np
import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose

def loadVideo(path):
	'''Dado um Path carrega um arquivo de video'''
	#Faz a verificação do caminho
	video = cv2.VideoCapture(path)
	return video

def loadimg(path):
	'''Dado um Path carrega um arquivo de video'''
	#Faz a verificação do caminho
	img = cv2.imread(path)
	return img

def show(img):
	'''Mostra a imagem'''
	#Mostra a imagem 
	cv2.imshow("Display window", img)
	key = cv2.waitKey(0)

def point_scale(image,pose):
	'''Dado uma pose extrai apenas os dados que serão usados'''
	pose_enum = mp.solutions.pose.PoseLandmark
	hight, width, _ = image.shape
	return [
		{
			'x':pose[pose_enum.LEFT_ANKLE].x * width,
			'y':pose[pose_enum.LEFT_ANKLE].y * hight,
			'point':'Tornozelo Esquerdo'
		},
		{
			'x':pose[pose_enum.LEFT_ELBOW].x * width,
			'y':pose[pose_enum.LEFT_ELBOW].y * hight,
			'point':'Cotovelo Esquerdo'
		},
		{
			'x':pose[pose_enum.LEFT_SHOULDER].x * width,
			'y':pose[pose_enum.LEFT_SHOULDER].y * hight,
			'point':'Ombro Esquerdo'
		},
		{
			'x':pose[pose_enum.LEFT_HEEL].x * width,
			'y':pose[pose_enum.LEFT_HEEL].y * hight,
			'point':'Calcanhar Esquerdo'
		},
		{
			'x':pose[pose_enum.LEFT_HIP].x * width,
			'y':pose[pose_enum.LEFT_HIP].y * hight,
			'point':'Quadril Esquerdo'
		},
		{
			'x':pose[pose_enum.LEFT_KNEE].x * width,
			'y':pose[pose_enum.LEFT_KNEE].y * hight,
			'point':'Joelho Esquerdo'
		},
		{
			'x':pose[pose_enum.LEFT_WRIST].x * width,
			'y':pose[pose_enum.LEFT_WRIST].y * hight,
			'point':'Pulso Esquerdo'
		},
		{
			'x':pose[pose_enum.RIGHT_ANKLE].x * width,
			'y':pose[pose_enum.RIGHT_ANKLE].y * hight,
			'point':'Tornozelo Direito'
		},
		{
			'x':pose[pose_enum.RIGHT_ELBOW].x * width,
			'y':pose[pose_enum.RIGHT_ELBOW].y * hight,
			'point':'Cotovelo Direito'
		},
		{
			'x':pose[pose_enum.RIGHT_SHOULDER].x * width,
			'y':pose[pose_enum.RIGHT_SHOULDER].y * hight,
			'point':'Ombro Direito'
		},
		{
			'x':pose[pose_enum.RIGHT_HEEL].x * width,
			'y':pose[pose_enum.RIGHT_HEEL].y * hight,
			'point':'Calcanhar Direito'
		},
		{
			'x':pose[pose_enum.RIGHT_HIP].x * width,
			'y':pose[pose_enum.RIGHT_HIP].y * hight,
			'point':'Quadril Direito'
		},
		{
			'x':pose[pose_enum.RIGHT_KNEE].x * width,
			'y':pose[pose_enum.RIGHT_KNEE].y * hight,
			'point':'Joelho Direito'
		},
		{
			'x':pose[pose_enum.RIGHT_WRIST].x * width,
			'y':pose[pose_enum.RIGHT_WRIST].y * hight,
			'point':'Pulso Direito'
		}
	]


# Argumentos para mp_pose.Pose()
# STATIC_IMAGE_MODE  ->  Se definido como false, a solução trata as imagens de entrada como um fluxo de vídeo. Ele tentará detectar a pessoa mais proeminente nas primeiras imagens e, após uma detecção bem-sucedida, localiza ainda mais os marcos da pose. Em imagens subsequentes, ele simplesmente rastreia esses pontos de referência sem invocar outra detecção até que perca o rastreamento, reduzindo a computação e a latência. Se definido como true, a detecção de pessoas executa cada imagem de entrada, ideal para processar um lote de imagens estáticas, possivelmente não relacionadas. Padrão para false.
# MODEL_COMPLEXITY  ->  Complexidade do modelo marco postura: 0, 1ou 2. A precisão do ponto de referência, bem como a latência de inferência, geralmente aumentam com a complexidade do modelo. Padrão para 1.
# SMOOTH_LANDMARKS  ->  Se definido como true, os filtros de solução representam pontos de referência em diferentes imagens de entrada para reduzir o jitter, mas são ignorados se static_image_mode também estiver definido como true. Padrão para true.
# ENABLE_SEGMENTATION  ->  Se definido como true, além dos marcos de pose, a solução também gera a máscara de segmentação. Padrão para false.
# SMOOTH_SEGMENTATION  ->  Se definido como true, a solução filtra as máscaras de segmentação em diferentes imagens de entrada para reduzir o jitter. Ignorado se enable_segmentation for false ou static_image_mode for true. Padrão para true.
# MIN_DETECTION_CONFIDENCE  ->  Valor de confiança mínimo ( [0.0, 1.0]) do modelo de detecção de pessoa para que a detecção seja considerada bem-sucedida. Padrão para 0.5.
# MIN_TRACKING_CONFIDENCE  ->  Valor de confiança mínimo ( [0.0, 1.0]) do modelo de rastreamento de pontos de referência para os pontos de referência de pose a serem considerados rastreados com sucesso, caso contrário, a detecção de pessoa será chamada automaticamente na próxima imagem de entrada. Configurá-lo com um valor mais alto pode aumentar a robustez da solução, às custas de uma latência mais alta. Ignorado se static_image_mode for true, em que a detecção de pessoas simplesmente é executada em todas as imagens. Padrão para 0.5.

pose = mp_pose.Pose(
	static_image_mode=True,
	enable_segmentation=True,
	model_complexity=2,
	min_detection_confidence=0.5,
	min_tracking_confidence=0.5
)

#Carrega a imagem
image = loadimg('t.jpg')

# Força uma passagem por referência
image.flags.writeable = False

#Faz o processamento da imagem
results = pose.process(image)

#Pontos utilizaveis
points = point_scale(image,results.pose_landmarks.landmark)

#DEBUG
print(points)

#Desenha os traços
mp_drawing.draw_landmarks(
	image,
	results.pose_landmarks,
	mp_pose.POSE_CONNECTIONS,
	landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())
	
show(image)