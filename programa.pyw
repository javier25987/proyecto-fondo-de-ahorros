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
         tkm.showerror('Error', 'El archivo es correcto.\nFalta crear la base de datos.')
    elif len(contenido) != 2:
        tkm.showerror('Error', 'El formato no es\nel de un archivo de\ncontrol reconocido.')
    else:
        try:
            n = int(contenido[0].strip())
            s = contenido[1].strip()
            if s[:6] == 'FONDO_' and s[-3:] == '.db' and s[6] == str(n-1): 
                try:
                    open(s)
                    nombre_bd = contenido[1]
                    nombre_negocio = Pf.leer_ajuste_n(ajuste_n=1, nombre_b=nombre_bd)
                    valor_de_la_multa = int(Pf.leer_ajuste_n(ajuste_n=2, nombre_b=nombre_bd))
                    clave_de_acceso = Pf.leer_ajuste_n(ajuste_n=5, nombre_b=nombre_bd)
                    numero_de_usuarios = int(Pf.leer_ajuste_n(ajuste_n=7, nombre_b=nombre_bd))
                    anular_usuarios = Pf.leer_ajuste_n(ajuste_n=8, nombre_b=nombre_bd) == 'True'
                    cobrar_las_multas = Pf.leer_ajuste_n(ajuste_n=9, nombre_b=nombre_bd) == 'False'
                    valor_de_la_cuota = int(Pf.leer_ajuste_n(ajuste_n=10, nombre_b=nombre_bd))
                    ejecutar_programa = True
                except:
                    tkm.showerror('Error', 'Base de datos no encontrada.')
            else:
                tkm.showerror('Error', 'El formato no es\nel de un archivo de\ncontrol reconocido.')
        except:
            tkm.showerror('Error', 'El formato no es\nel de un archivo de\ncontrol reconocido.') 
except:   
    tkm.showerror('Error', 'No se encuentra el\narchivo de control.')
    
tipo_b = 'calibri 15'
tipo_l = 'calibri 12'
usuario_actual = 0

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
            tkm.showwarning('error', 'Aun no se ha creado un calendario.')
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
        global usuario_actual, numero_de_usuarios, nombre_bd, anular_usuarios, cobrar_las_multas
        numero_k = self.numero_usuario.get()
        if numero_k == '':
            tkm.showwarning('Error', 'El espacio de usuario esta vacio.')
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
                        Pf.arreglar_asuntos(usuario=usuario_actual, nombre_b=nombre_bd, cobrar_multas=cobrar_las_multas)
                        self.destroy()
                        pago_de_cuotas().mainloop()
                    else:
                        tkm.showwarning('Error', 'El usuario no esta activo\nno se puede acceder a el por este metodo.')
                else:
                    tkm.showwarning('Error', 'Me temo que tal usuario no existe.')
            else:
                tkm.showwarning('Error', 'Creo que lo introucido no es un numero.')

    def pagar_multas(self):
        global usuario_actual, nombre_bd, valor_de_la_multa
        k = self.multas_a_pagar.get()
        if usuario_actual == 0 or k == 0:
            pass
        else:
            puestos = Pf.leer_en_socios(usuario_n=usuario_actual, nombre_b=nombre_bd, columna='puestos')
            valor_t = k*valor_de_la_multa*puestos
            caja = tkm.askquestion('Pago', f'Se reciben {Pf.corregir_numero_miles(valor_t)} por {k} multa(s),\n¿desea continuar?')
            if caja == 'yes':
                Pf.pagar_n_multas(usuario=usuario_actual, n=k, nombre_b=nombre_bd)
                Pf.sumar_a_multas(usuario_n=usuario_actual, nombre_b=nombre_bd, valor_s=valor_t)
                self.destroy()
                pago_de_cuotas().mainloop()
            else:
                tkm.showwarning('Error', 'No se completo el pago.')

    def pagar_cuotas(self):
        global usuario_actual, valor_de_la_cuota
        if usuario_actual == 0:
            pass
        else:
            opc_tesorero = self.tesoreros.get()
            if opc_tesorero == 0:
                tkm.showwarning('Error', 'Cero esta castigado y no puede ser\nun tesorero.\nPor favor seleccione un tesorero.')
            else:
                cuotas = self.numero_de_cuotas.get()
                puestos = Pf.leer_en_socios(usuario_n=usuario_actual, nombre_b=nombre_bd, columna='puestos')
                valor_t = puestos*valor_de_la_cuota*cuotas
                caja = tkm.askquestion('Pago', f'Se reciben {Pf.corregir_numero_miles(valor_t)} por {cuotas} cuota(s),\n¿desea continuar?')
                if caja == 'yes':
                    Pf.pagar_n_cuotas(usuario=usuario_actual, nombre_b=nombre_bd, n=cuotas, tesorero=opc_tesorero)
                    Pf.sumar_a_capital(usuario_n=usuario_actual, nombre_b=nombre_bd, valor_s=valor_t)
                    self.destroy()
                    pago_de_cuotas().mainloop()
                else:
                    tkm.showwarning('Error', 'No se completo el pago.')

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

        self.frame_2_1 = tk.Frame(self.frame_2)

        self.label_cuotas = tk.Label(self.frame_2_1, text=Pf.string_calendario_usuario(nombre_b=nombre_bd, usuario=usuario_actual), font='calibri 14')
        self.label_cuotas.place(relx=0, rely=0)

        self.frame_2_1.place(relx=0.05, rely=0, relheight=1, relwidth=0.3)

        self.frame_2_2 = tk.Frame(self.frame_2)

        self.label_multas = tk.Label(self.frame_2_2, text=Pf.mostrar_multas(nombre_b=nombre_bd, usuario=usuario_actual), font='calibri 14')
        self.label_multas.place(relx=0, rely=0)

        self.letrero_multas = tk.Label(self.frame_2_2, text='multas a pagar:', font=tipo_b)
        self.letrero_multas.place(relx=0.45, rely=0.115)

        numero_de_multas = Pf.contar_numero_de_multas(nombre_b=nombre_bd, usuario=usuario_actual)
        self.multas_a_pagar = tk.IntVar()
        self.multas_a_pagar.set(numero_de_multas[-1])

        self.opciones_de_multa = tk.OptionMenu(self.frame_2_2, self.multas_a_pagar, *numero_de_multas)
        self.opciones_de_multa.configure(font=tipo_b)
        self.opciones_de_multa.place(relx=0.75, rely=0.1)

        self.boton_pagar_multas = tk.Button(self.frame_2_2, text='pagar multa(s)', command=self.pagar_multas, font='calibri 16')
        self.boton_pagar_multas.place(relx=0.5, rely=0.4)

        self.frame_2_2.place(relx=0.35, rely=0.5, relheight=0.35, relwidth=0.3)

        self.frame_2_3 = tk.Frame(self.frame_2)
        tesoreros = [1,2,3,4]
        numero_de_cuotas = Pf.contar_numero_de_cuotas(nombre_b=nombre_bd, usuario=usuario_actual)

        self.tesoreros = tk.IntVar()
        self.tesoreros.set(0)

        self.numero_de_cuotas = tk.IntVar()
        self.numero_de_cuotas.set(numero_de_cuotas[0])

        self.letrero_cuotas = tk.Label(self.frame_2_3, text='cuotas a pagar:', font=tipo_b)
        self.letrero_cuotas.place(relx=0.2, rely=0.125)

        self.opciones_de_cuota = tk.OptionMenu(self.frame_2_3, self.numero_de_cuotas, *numero_de_cuotas)
        self.opciones_de_cuota.configure(font=tipo_b)
        self.opciones_de_cuota.place(relx=0.5, rely=0.11)

        self.letrero_tesorero = tk.Label(self.frame_2_3, text='cuotas pagadas a', font=tipo_b)
        self.letrero_tesorero.place(relx=0.16, rely=0.33)

        self.opciones_de_tesorero = tk.OptionMenu(self.frame_2_3, self.tesoreros, *tesoreros)
        self.opciones_de_tesorero.configure(font=tipo_b)
        self.opciones_de_tesorero.place(relx=0.5, rely=0.31)

        self.boton_pagar_cuotas = tk.Button(self.frame_2_3, text='pagar cuota(s)', font='calibri 16', command=self.pagar_cuotas)
        self.boton_pagar_cuotas.place(relx=0.3, rely=0.6)

        self.frame_2_3.place(relx=0.35, rely=0, relheight=0.35, relwidth=0.3)

        self.frame_2.place(relx=0, rely=0.1, relheight=0.8, relwidth=1)

        self.frame_3 = tk.Frame(self)

        self.button_menu = tk.Button(self.frame_3, text='menu', command=self.menudeopciones, font=tipo_b)
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
