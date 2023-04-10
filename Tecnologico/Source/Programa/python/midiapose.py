import cv2
import numpy as np
import mediapipe as mp
import tensor

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose

def loadVideo(path):
	'''Dado um Path carrega um arquivo de video'''
	#Faz a verificação do caminho
	video = cv2.VideoCapture(path)
	return video


def show(img,autoRun=1):
	'''Mostra a imagem'''
	#Mostra a imagem  até que a tecla 'Q' seja pressionada
	cv2.imshow("Display window", img)
	key = cv2.waitKey(autoRun) != ord('q')
	return key

def main():
	'''Main run'''
	video = loadVideo('midia/c.mp4')
	continuar = True
	pose = mp_pose.Pose(
		static_image_mode=True,
		enable_segmentation=True,
		model_complexity=2,
		min_detection_confidence=0.5,
		min_tracking_confidence=0.5
	)

	while continuar:
		continuar, img = video.read()

		#Redimensiona a imagem
		image = img
		image = cv2.resize(img, (0,0), fx=0.25, fy=0.25) 
		try:

			# Força uma passagem por referência
			image.flags.writeable = False

			#Faz o processamento da imagem
			results = pose.process(image)

			#Pontos utilizaveis
			points = tensor.point_scale(image,results.pose_landmarks.landmark)

			#Desenha os traços
			image = tensor.draw(image, tensor.Pose.BRACO_DIR,(255,0,0),points)
			image = tensor.draw(image, tensor.Pose.BRACO_ESQ,(255,0,0),points)
			image = tensor.draw(image, tensor.Pose.PERNA_DIR,(0,255,0),points)
			image = tensor.draw(image, tensor.Pose.PERNA_ESQ,(0,255,0),points)
			image = tensor.draw(image, tensor.Pose.CORPO,(0,0,255),points)
				
			continuar = show(image)
		except Exception:
			continuar = show(image)



main()