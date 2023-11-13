import tkinter as tk


        
class Input():

    def __init__(self,janela, fx ,label="",placeholder="",size=0) -> None:
        def validar_input(input):
            checks = []
            if (size > 0):
                if (len(input) <= size):
                    checks.append(True)
                else:
                    checks.append(False)
            if (input.replace(".", "").isdigit() or input =="") and input.count(".") <= 1:
                checks.append(True)
            else:
                checks.append(False)
            return not False in checks
                
        # Criação do campo de entrada
        self.label = tk.Label(janela, text=label)
        self.entrada = tk.Entry(janela, justify='center', textvariable=tk.StringVar())
        reg = janela.register(validar_input) 
        self.entrada.config(validate ="key",validatecommand =(reg, '%P'))
        self.entrada.insert(0, placeholder)
        self.entrada.bind("<KeyRelease>", fx)
        
    def get_value(self):
        valor = self.entrada.get()
        return valor

    def get_button(self):
        return self.entrada 
    
    def get_label(self):
        return self.entrada 

    def setPlaceButton(self, indice = 0):
        '''Função interna usado para criar um button na tela'''
        WIDTH, BORDER, INTER_BORDER = 50, 50, 10
        x = BORDER+(WIDTH*indice)+(INTER_BORDER*indice)
        #Fixa o input           
        self.label.place(x=x, y=0, width=WIDTH)
        self.entrada.place(x=x, y=20, width=WIDTH)
    
    def switchText(self,newText):
        #Altera Texto
        self.entrada.delete(0, tk.END)  # Limpa o conteúdo atual do input
        self.entrada.insert(0, newText)
