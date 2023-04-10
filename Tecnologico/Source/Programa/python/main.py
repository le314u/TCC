import cv2
import midia_pipe


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
	startUI()
	video = loadVideo('midia/c.mp4')
	continuar = True

	while continuar:
		continuar, img = video.read()

		#Redimensiona a imagem
		image = img
		image = cv2.resize(img, (0,0), fx=0.25, fy=0.25) 
		print(image[0],image[1])
		try:

			# Força uma passagem por referência
			image.flags.writeable = False

			#Faz o processamento da imagem
			points = midia_pipe.process_img(image)

			#Desenha os traços
			image = midia_pipe.draw(image, midia_pipe.Pose.BRACO_DIR,(255,0,0),points)
			image = midia_pipe.draw(image, midia_pipe.Pose.BRACO_ESQ,(255,0,0),points)
			image = midia_pipe.draw(image, midia_pipe.Pose.PERNA_DIR,(0,255,0),points)
			image = midia_pipe.draw(image, midia_pipe.Pose.PERNA_ESQ,(0,255,0),points)
			image = midia_pipe.draw(image, midia_pipe.Pose.CORPO,(0,0,255),points)
				
			continuar = show(image)
		except Exception:
			continuar = show(image)



def nothing(x):
    pass

def getMeta(window_name):
    return cv2.getTrackbarPos('size',window_name)

def startUI(window_name=""):
    '''Cria uma UI'''

    window_name = "UI"
    #Altera o nome da janela
    cv2.namedWindow(window_name)
    cv2.createTrackbar('size',window_name,0,100,nothing)



main()