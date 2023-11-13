import sys
import os
from tkinter import *
from tkinter import filedialog

def getPath(title='Selecione o ARQUIVO'):
    '''Seta o Path do video'''
    aux = Tk()
    currdir = os.getcwd()
    path = filedialog.askopenfilename(parent=aux, initialdir=currdir, title=title)
    aux.destroy()
    return path