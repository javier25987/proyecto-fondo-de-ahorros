import tkinter as tk 

nombre_negocio = 'fondo san javier'

n = 'fondo de ahorro, esperando nuevas actualizaciones'

class Funciones():
    def __init__(self):
        pass

    def funcion_1(self):
        pass

class primera_ventana(tk.Tk, Funciones):
    def __init__(self):
        super().__init__()

        self.state("zoomed")

        self.title(nombre_negocio)

        self.label = tk.Label(self, text=n)
        self.label.pack()

        self.button_crear_socio = tk.Button(self, text='crear socio', command=self.funcion_1)
        self.button_crear_socio.pack()

        self.label_version = tk.Label(self, text='version 0,0,0')
        self.label_version.place(relx=0, rely=0.975)

primera_ventana().mainloop()