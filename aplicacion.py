#============================================================================= librerias necesarias
import tkinter as tk 
import tkinter.messagebox as tkm
import tkinter.simpledialog as tks
import sqlite3 as sql
import datetime
import Pfunciones as Pf
#============================================================================= ajustes del programa
ejecutar_programa = False
try:
    with open('ArchivoControl.txt', 'r') as f:
        contenido = f.readlines()

    if contenido == ['1']:
         tkm.showerror('Error', 'el archivo es correcto\nfalta crear la base de datos')
    elif len(contenido) != 2:
        tkm.showerror('Error', 'el formato no es\nel de un archivo de\ncontrol reconocido')
    else:
        try:
            n = int(contenido[0].strip())
            s = contenido[1].strip()
            if s[:6] == 'FONDO_' and s[-3:] == '.db' and s[6] == str(n-1): 
                try:
                    open(s)
                    nombre_bd = contenido[1]
                    nombre_negocio = Pf.leer_ajuste_n(1, nombre_bd)
                    clave_de_acceso = Pf.leer_ajuste_n(5, nombre_bd)
                    print(clave_de_acceso)
                    ejecutar_programa = True
                except:
                    tkm.showerror('Error', 'base de datos no encontrada')
            else:
                tkm.showerror('Error', 'el formato no es\nel de un archivo de\ncontrol reconocido')
        except:
            tkm.showerror('Error', 'el formato no es\nel de un archivo de\ncontrol reconocido') 
except:   
    tkm.showerror('Error', 'no se encuentra el\narchivo de control')
    
tipo_b = 'calibri 15'
tipo_l = 'calibri 12'

pagina_en_actualizacion = f'fondo de ahorro, esperando nuevas actualizaciones'

#============================================================================= funciones necesarias

class Funciones():
    def __init__(self):
        pass

    def menudeopciones(self):
        self.destroy()
        menu_de_opciones().mainloop()

    def pagodecuotas(self):
        self.destroy()
        pago_de_cuotas().mainloop()

    def ajustesdelprograma(self):
        if Pf.preguntar_la_clave(clave_p=clave_de_acceso):
            self.destroy()
            ajustes_del_programa().mainloop()

    def prestamosasocios(self):
        self.destroy()
        prestamos_a_socios().mainloop()

    def modificarsocios(self):
        if Pf.preguntar_la_clave(clave_p=clave_de_acceso):
            self.destroy()
            modificar_socios().mainloop()

#=========================================================================== definicion de ventanas
#============================================================ menu del programa
    
class menu_de_opciones(tk.Tk, Funciones):
    def __init__(self):
        super().__init__()

        self.state("zoomed")

        self.title('menu')
        self.iconphoto(False, tk.PhotoImage(file='icono.ico'))

        self.label = tk.Label(self, text=nombre_negocio, font='calibri 20')
        self.label.pack()

        self.button_pago_cuotas = tk.Button(self, text='pago de cuotas', command=self.pagodecuotas, font=tipo_b)
        self.button_pago_cuotas.pack()

        self.button_prestamos = tk.Button(self, text='prestamos', command=self.prestamosasocios, font=tipo_b)
        self.button_prestamos.pack()

        self.button_modificar_socios = tk.Button(self, text='modificar socios', command=self.modificarsocios, font=tipo_b)
        self.button_modificar_socios.pack()

        self.button_ajustes = tk.Button(self, text='ajustes', command=self.ajustesdelprograma, font=tipo_b)
        self.button_ajustes.pack()

        self.label_version = tk.Label(self, text=f'version: 0,0,0     base de datos: {nombre_bd}')
        self.label_version.place(relx=0, rely=0.975)

        valor = tk.StringVar()
        valor.set('todas')

        self.drop = tk.OptionMenu(self, valor, 'todas', 'opcion_1', 'opcion_2', 'opcion_3')
        self.drop.configure(font=tipo_b)
        self.drop.pack() #ipadx=20, ipady=10

#============================================================ proceso de cuotas
        
class pago_de_cuotas(tk.Tk, Funciones):
    def __init__(self):
        super().__init__()

        self.state("zoomed")

        self.title('pago de cuotas')
        self.iconphoto(False, tk.PhotoImage(file='icono.ico'))

        self.label = tk.Label(self, text=pagina_en_actualizacion, font=tipo_l)
        self.label.pack()

        self.button_menu = tk.Button(self, text='menu', command=self.menudeopciones, font=tipo_b)
        self.button_menu.pack()

#========================================================= ajustes del programa
        
class ajustes_del_programa(tk.Tk, Funciones):
    def __init__(self):
        super().__init__()

        self.state("zoomed")

        self.title('ajustes')
        self.iconphoto(False, tk.PhotoImage(file='icono.ico'))

        self.label = tk.Label(self, text=pagina_en_actualizacion, font=tipo_l)
        self.label.pack()

        self.button_menu = tk.Button(self, text='menu', command=self.menudeopciones, font=tipo_b)
        self.button_menu.pack()

#============================================================ prestamos a socios
        
class prestamos_a_socios(tk.Tk, Funciones):
    def __init__(self):
        super().__init__()

        self.state("zoomed")

        self.title('prestamos')
        self.iconphoto(False, tk.PhotoImage(file='icono.ico'))

        self.label = tk.Label(self, text=pagina_en_actualizacion, font=tipo_l)
        self.label.pack()

        self.button_menu = tk.Button(self, text='menu', command=self.menudeopciones, font=tipo_b)
        self.button_menu.pack()

#============================================================ modificar socios
        
class modificar_socios(tk.Tk, Funciones):
    def __init__(self):
        super().__init__()

        self.state("zoomed")

        self.title('socios')
        self.iconphoto(False, tk.PhotoImage(file='icono.ico'))

        self.label = tk.Label(self, text=pagina_en_actualizacion, font=tipo_l)
        self.label.pack()

        self.button_menu = tk.Button(self, text='menu', command=self.menudeopciones, font=tipo_b)
        self.button_menu.pack()

#================================================================================== ejecucion final

if __name__ == '__main__':
    if ejecutar_programa:
        menu_de_opciones().mainloop()