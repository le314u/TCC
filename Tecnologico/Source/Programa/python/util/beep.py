import os
import sys
import pygame

def beep():
    pygame.init()
    pygame.mixer.Sound.play(pygame.mixer.Sound('/home/guest/Área de Trabalho/TCC/Tecnologico/Source/Programa/python/midia/beep.mp3'))
