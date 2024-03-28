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
         tkm.showerror('Error', 'el archivo es correcto.\nfalta crear la base de datos')
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
                    nombre_negocio = Pf.leer_ajuste_n(ajuste_n=1, nombre_b=nombre_bd)
                    clave_de_acceso = Pf.leer_ajuste_n(ajuste_n=5, nombre_b=nombre_bd)
                    numero_de_usuarios = int(Pf.leer_ajuste_n(ajuste_n=7, nombre_b=nombre_bd))
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
usuario_actual = 0
anular_usuarios = False

pagina_en_actualizacion = f'fondo de ahorro, esperando nuevas actualizaciones'

#============================================================================= funciones necesarias

class Funciones():
    def __init__(self):
        pass

    def menudeopciones(self):
        self.destroy()
        menu_de_opciones().mainloop()

    def pagodecuotas(self):
        global usuario_actual
        if Pf.leer_ajuste_n(ajuste_n=6, nombre_b=nombre_bd) == 'None':
            tkm.showwarning('error', 'aun no se ha creado un calendario')
        else:
            usuario_actual = 0
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
    
    def buscar_usuario(self):
        global usuario_actual, numero_de_usuarios, nombre_bd, anular_usuarios
        numero_k = self.numero_usuario.get()
        if numero_k == '':
            tkm.showwarning('error', 'el espacio de usuario esta vacio')
        else:
            if Pf.rectificar_numero(numero_k):
                numero_k = int(numero_k)
                if 0 < numero_k <= numero_de_usuarios:
                    usuario_actual = numero_k
                    string = Pf.leer_en_socios(usuario_n=usuario_actual, columna='multas', nombre_b=nombre_bd)
                    if anular_usuarios:
                        if string.count('0') < 47:
                            Pf.cargar_datos_texto(nombre_b=nombre_bd, 
                                                  usuario=usuario_actual, 
                                                  tabla='socios', 
                                                  columna='estado', 
                                                  nuevo_valor='desactivado')
                    if Pf.leer_en_socios(usuario_n=usuario_actual, columna='estado', nombre_b=nombre_bd) == 'activo':
                        Pf.arreglar_asuntos(usuario=usuario_actual, nombre_b=nombre_bd)
                        self.destroy()
                        pago_de_cuotas().mainloop()
                    else:
                        tkm.showwarning('error', 'el usuario no esta activo\nno se puede acceder a el por este metodo')
                else:
                    tkm.showwarning('error', 'me temo que tal usuario no existe')
            else:
                tkm.showwarning('error', 'creo que lo introucido no es un numero')

#=========================================================================== definicion de ventanas
#============================================================ menu del programa
    
class menu_de_opciones(tk.Tk, Funciones):
    def __init__(self):
        super().__init__()

        self.state("zoomed")

        self.title('menu')
        self.iconphoto(False, tk.PhotoImage(file='icono.ico'))

        self.label = tk.Label(self, text=nombre_negocio, font='serif 50')
        self.label.pack(pady=70)

        self.button_pago_cuotas = tk.Button(self, text='pago de cuotas', command=self.pagodecuotas, font=tipo_b)
        self.button_pago_cuotas.pack(pady=3)

        self.button_prestamos = tk.Button(self, text='prestamos', command=self.prestamosasocios, font=tipo_b)
        self.button_prestamos.pack(pady=3)

        self.button_modificar_socios = tk.Button(self, text='modificar socios', command=self.modificarsocios, font=tipo_b)
        self.button_modificar_socios.pack(pady=3)

        self.button_ajustes = tk.Button(self, text='ajustes', command=self.ajustesdelprograma, font=tipo_b)
        self.button_ajustes.pack(pady=3)

        self.label_version = tk.Label(self, text=f'version: 0,0,0     base de datos: {nombre_bd}')
        self.label_version.place(relx=0, rely=0.975)

#============================================================ proceso de cuotas
        
class pago_de_cuotas(tk.Tk, Funciones):
    def __init__(self):
        global usuario_actual
        super().__init__()

        self.state("zoomed")

        self.title('pago de cuotas')
        self.iconphoto(False, tk.PhotoImage(file='icono.ico'))

        self.frame_1 = tk.Frame(self)
        pos_el = 0.75

        self.numero_usuario = tk.Entry(self.frame_1, font='calibri 26')
        self.numero_usuario.place(relx=pos_el, rely=0.4, relwidth=0.05, relheight=0.5)

        self.buscar_usuario = tk.Button(self.frame_1, text='buscar', command=self.buscar_usuario, font=tipo_b)
        self.buscar_usuario.place(relx=pos_el+0.06, rely=0.4, relheight=0.5)


        self.titulo_usuario = tk.Label(self.frame_1, text=Pf.titulo_de_usuario(nombre_b=nombre_bd, usuario=usuario_actual), font='calibri 25')
        self.titulo_usuario.place(relx=0.05, rely=0.3)

        self.frame_1.place(relx=0, rely=0, relheight=0.1, relwidth=1)

        self.frame_2 = tk.Frame(self)

        self.label_cuotas = tk.Label(self.frame_2, text=Pf.string_calendario_usuario(nombre_b=nombre_bd, usuario=usuario_actual), font='calibri 14')
        self.label_cuotas.place(relx=0.05, rely=0)

        self.label_multas = tk.Label(self.frame_2, text=Pf.mostrar_multas(nombre_b=nombre_bd, usuario=usuario_actual), font='calibri 14')
        self.label_multas.place(relx=0.35, rely=0)

        self.frame_2.place(relx=0, rely=0.1, relheight=0.8, relwidth=1)

        self.frame_3 = tk.Frame(self)

        self.button_menu = tk.Button(self.frame_3, text='<-- menu', command=self.menudeopciones, font=tipo_b)
        self.button_menu.place(relx=0.1, rely=0.1)

        self.frame_3.place(relx=0, rely=0.9, relheight=0.1, relwidth=1)

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
