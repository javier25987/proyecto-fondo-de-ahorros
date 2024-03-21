#============================================================================= librerias necesarias
import tkinter as tk 
import tkinter.messagebox as tkm
import tkinter.simpledialog as tks
import sqlite3 as sql
import datetime as dt
import os

#============================================================================= ajustes del programa
ejecutar_programa = False
try:
    with open('DatosImportantes.txt', 'r') as f:
        contenido = f.readlines()

    if len(contenido) != 2:
        tkm.showerror('Error', 'el formato no es\nel de un archivo de\ncontrol reconocido') 
    else:
        try:
            int(contenido[0].strip())
            s = contenido[1].strip()
            if s[:6] == 'FONDO_' and s[-3:] == '.db': #se puede pedir confirmacion por la cifra dada
                try:
                    open(s)
                    nombre_bd = contenido[1]
                    nombre_negocio = 'fondo san javier'
                    clave_de_acceso = '1234'
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

def rectify(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

def preguntar_la_clave():
    global clave_de_acceso

    status = False

    text = '''los parametros que se pueden modificar en la siguiente ventana repercuten 
en el optimo funcionamiento del programa, por lo ello se necesita una
clave de acceso para acceder a ellos, por favor digite la clave de acceso'''

    clave = tks.askstring('contraseña', text,).strip()

    if clave == clave_de_acceso:
        status = True
    elif clave == '':
        tkm.showwarning('error', 'la contraseña no puede estar vacia')
    elif clave == None:
        tkm.showwarning('error', 'lo siento no puedes acceder')
    else:
        tkm.showwarning('error', 'la contraseña no es correcta')
    
    return status

class Funciones():
    def __init__(self):
        pass

    def w_h_screen(self, w_w = 600, h_w = 300):

        width_window = w_w
        height_window = h_w

        width_screen = self.winfo_screenwidth()
        height_screen = self.winfo_screenheight()

        x = (width_screen - width_window) // 2
        y = (height_screen - height_window) // 2

        self.geometry(f'{width_window}x{height_window}+{x}+{y}')

    def menudeopciones(self):
        self.destroy()
        menu_de_opciones().mainloop()

    def pagodecuotas(self):
        self.destroy()
        pago_de_cuotas().mainloop()

    def ajustesdelprograma(self):
        if preguntar_la_clave():
            self.destroy()
            ajustes_del_programa().mainloop()

    def prestamosasocios(self):
        self.destroy()
        prestamos_a_socios().mainloop()

    def modificarsocios(self):
        if preguntar_la_clave():
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

        self.label = tk.Label(self, text=pagina_en_actualizacion, font=tipo_l)
        self.label.pack()

        self.button_pago_cuotas = tk.Button(self, text='pago de cuotas', command=self.pagodecuotas, font=tipo_b)
        self.button_pago_cuotas.pack()

        self.button_prestamos = tk.Button(self, text='prestamos', command=self.prestamosasocios, font=tipo_b)
        self.button_prestamos.pack()

        self.button_modificar_socios = tk.Button(self, text='modificar socios', command=self.modificarsocios, font=tipo_b)
        self.button_modificar_socios.pack()

        self.button_ajustes = tk.Button(self, text='ajustes', command=self.ajustesdelprograma, font=tipo_b)
        self.button_ajustes.pack()

        self.label_version = tk.Label(self, text=f'version 0,0,0     base de datos {nombre_bd}')
        self.label_version.place(relx=0, rely=0.975)

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