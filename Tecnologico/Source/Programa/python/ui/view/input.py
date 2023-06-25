import tkinter as tk


        
class Input():

    def __init__(self,janela, fx ,label="",size=4) -> None:
        def validar_input(input):
            if ( (input.isdigit() or input == "") or ("." in input and input.count(".") <=1) ) and len(input) <= size:
                return True
            return False
        
        # Criação do campo de entrada
        self.label = tk.Label(janela, text=label)
        self.entrada = tk.Entry(janela, justify='center', textvariable=tk.StringVar())
        reg = janela.register(validar_input) 
        self.entrada.config(validate ="key",validatecommand =(reg, '%P'))
        self.entrada.insert(0, "1.0")
        self.entrada.bind("<KeyRelease>", fx)
        self._location()

        
    def get_value(self):
        valor = self.entrada.get()
        return valor

    def get_button(self):
        return self.entrada   

    def _location(self):
        '''Função interna usado para criar um button na tela'''
        WIDTH, BORDER, INTER_BORDER = 50, 50, 10
        n_buttons=0
        i = n_buttons
        x = BORDER+(WIDTH*i)+(INTER_BORDER*i)

        #Fixa o input           
        self.label.place(x=x, y=0, width=WIDTH)
        self.entrada.place(x=x, y=20, width=WIDTH)