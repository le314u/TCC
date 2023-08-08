import threading
from typing import List
from tkinter import *

from controller.preProcess import preProcess
from controller.processImg.debug import save_img, save_video
from controller.processImg.others import createVideo
from controller.render.pipe import PipeLine
from controller.render.renderBar import renderBar
from controller.render.renderPose import renderPose
from controller.render.renderTxt import renderTxt
from controller.util.coloredMsg import msg
from controller.util.flag import Flag
from util.path import fixPath
from controller.util.progress_bar import progress_bar
from controller.video.videoController import VideoController
from view.ui.components.buttonSketch import ButtonSketch
from view.ui.screen.getPath import getPath
from view.ui.screen.playerWin import PlayerWin




class MainWindow():
	controller_thread = {"run":True}
	def __init__(self, flags:List[Flag] = [None]):
		#TODO verificar o clocal correto de TESTE
		DATA = self.TESTE()
		pipeRender = DATA['pipeRender']
		btns = DATA['btns']
		list_flags = DATA['flags']
		path = "./midia/lazy_white.mp4" 
		

		#Inicia a parte grafica'''
		path = getPath()
		self.controller = VideoController(path=path)

		#Pre processamento ocorre em paralelo
		thread_controller = {"thread_controller":True}
		thread_args = (self.controller, list_flags, thread_controller)
		thread_func = preProcess
		self.thread_process = threading.Thread(target=thread_func, args=thread_args)
		self.thread_process.daemon = True
		self.thread_process.start()
		self.player = PlayerWin(self.controller, btns, list_flags, pipeRender, controller_thread= MainWindow.controller_thread)

		#Persiste o Player
		self.player.run()

		#Encerra a Thread e evita Erros
		thread_controller["thread_controller"]=False
		self.thread_process.join()

	def TESTE(self):
		#Cria as flags
		finished = Flag("Processed",state=False,triguer=True)
		saveFrame_flag = Flag("SaveF",state=True,triguer=True)
		saveVideo_flag = Flag("SaveV",state=True,triguer=True)
		barra_flag = Flag("Barra")
		dados_flag = Flag("Dados")
		eph_flag = Flag("EPH")
		all_flags = [finished,saveFrame_flag, saveVideo_flag,barra_flag, dados_flag,eph_flag]

		#Seta uma Função para cada Flag
		barra_flag.setFx( lambda frame, cel : renderBar(frame,cel.getLine() ) )
		dados_flag.setFx( lambda frame, cel : renderTxt(frame,cel.getData() ) )
		eph_flag.setFx( lambda frame, cel : renderPose(frame,cel.getPose() ) )

		#Cria um pipeLine de Renderização
		pipe_render = PipeLine()
		pipe_render.addFlag(barra_flag,1)
		pipe_render.addFlag(dados_flag,1)
		pipe_render.addFlag(eph_flag,1)

		def saveFrame(frame=None, cel=None):
			id = 0
			if frame is None:
				frame = self.controller.getFrame()
			if cel is None:
				id = self.controller.getIdCurrentFrame()
				cel = self.controller.getCel(id)
				path = "./midia/dist/"
				fixPath(path)

			save_img( 
				pipe_render.processImg(frame,cel),
				f"{path}/{id}_processed"
			)
			print(f"Save:{id}_processed")

		def saveVideo(frame=None, cel=None):
			path = "./midia/dist/"
			name = f"{path}video_processed"
			fixPath(path)
			
			controller = self.controller
			metaVideo = controller.getMetaVideo()
			frames = []

			#Processamento dos frames
			for id in range(controller.getTotalFrame()):
				cel = controller.getCel(id)
				frame = cel.getFrame()
				frame_processed = pipe_render.processImg(frame, cel)
				frames.append(frame_processed)
			
			save_video(metaVideo, frames, name)
			print(f"Save:video_processed")

						
		saveFrame_flag.setFx(saveFrame)
		saveVideo_flag.setFx(saveVideo)

		#Cria os buttons
		createListButtons = lambda flags: [ButtonSketch(flag.getName(),flag) for flag in flags  ]
		btns:List[ButtonSketch] =  createListButtons(all_flags[1:])
		initial_state = {
		  "frame":0,
		  "velocidade":1.0,
		  "flags":all_flags[1:]
		}		
		
		def fx():
			self.player.setState(initial_state)

		finished.setFx(lambda : (fx())) 
			
		return {
			'flags':all_flags,
			'btns':btns,
			'pipeRender':pipe_render
		}
	