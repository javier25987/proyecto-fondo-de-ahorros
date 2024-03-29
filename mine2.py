import tkinter.messagebox as tkm
import Pfunciones as Pf

caja = tkm.askquestion('pago', f'se reciben 2000 por 8 multa(s),\n¿desea continuar?')

if caja == 'yes':
    Pf.sumar_una_multa(usuario=1, semana=1, nombre_b='FONDO_1_2024.db')
    Pf.sumar_una_multa(usuario=1, semana=5, nombre_b='FONDO_1_2024.db')
    Pf.sumar_una_multa(usuario=1, semana=8, nombre_b='FONDO_1_2024.db')
    Pf.sumar_una_multa(usuario=1, semana=7, nombre_b='FONDO_1_2024.db')
    Pf.sumar_una_multa(usuario=1, semana=11, nombre_b='FONDO_1_2024.db')
    Pf.sumar_una_multa(usuario=1, semana=17, nombre_b='FONDO_1_2024.db')
    Pf.sumar_una_multa(usuario=1, semana=18, nombre_b='FONDO_1_2024.db')

import tkinter as tk

numero_t = 0

class root(tk.Tk):
    def __init__(self):
        global numero_t
        super().__init__()
        self.title('prueva')
        self.state('zoomed')

        self.label = tk.Label(self, text=f'el valor del boton es = {numero_t}'*numero_t)
        self.label.pack()

        self.valor = tk.IntVar()
        self.valor.set(0)

        opciones = [0,1,2,3,4,5,6,7,8,9]

        self.drop = tk.OptionMenu(self, self.valor, *opciones)
        self.drop.configure(font='calibri 20')
        self.drop.pack() #ipadx=20, ipady=10

        self.buton = tk.Button(self, text='cambair', command=self.cambiar)
        self.buton.pack()

    def cambiar(self):
        global numero_t
        print(numero_t, self.valor.get())
        numero_t = self.valor.get()
        self.destroy()
        root().mainloop()

root().mainloop()