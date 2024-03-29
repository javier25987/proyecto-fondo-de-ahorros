import tkinter as tk 
import tkinter.messagebox as tkm
import tkinter.simpledialog as tks
import sqlite3 as sql
import datetime as dt
import Pfunciones as Pf

def insertar_ajuste(nombre_ajuste, valor, nombre_b):
    base = sql.connect(nombre_b)
    cursor = base.cursor()
    instruc = f"INSERT INTO ajustes VALUES ('{nombre_ajuste}', '{valor}')"
    cursor.execute(instruc)
    base.commit()
    base.close()
    
def crear_base_de_datos():
    nombre = 'FONDO_'
    try:
        open('ArchivoControl.txt')
    except:
        tkm.showerror('Error', 'No se encuentra el\narchivo de control.')
        return None
    
    with open('ArchivoControl.txt', 'r') as file:
        lineas = file.readlines()
        lineas[0] = lineas[0].strip()
    
    nombre = nombre + lineas[0] + '_' + dt.datetime.now().strftime('%Y') + '.db'
    
    base = sql.connect(nombre)
    base.commit()
    base.close()

    base = sql.connect(nombre)
    cursor = base.cursor()
    cursor.execute(
        '''CREATE TABLE ajustes(
        nombre_ajuste text,
        valor text
        )'''
    )
    base.commit()
    base.close()

    insertar_ajuste('rotulo', 'fondo san javier', nombre)
    insertar_ajuste('valor de la multa', 3000, nombre)
    insertar_ajuste('interes por prestamo', 0.03, nombre)
    insertar_ajuste('numero de cuotas', 50, nombre)
    insertar_ajuste('clave de acceso', 1234, nombre)
    insertar_ajuste('calendario', 'None', nombre)
    insertar_ajuste('numero de usuarios', 0, nombre)
    insertar_ajuste('anular usuarios', 'False', nombre)
    insertar_ajuste('cobrar multas', 'False', nombre)
    insertar_ajuste('valor de la cuota', 10000, nombre)

    base = sql.connect(nombre)
    cursor = base.cursor()
    cursor.execute(
        '''CREATE TABLE socios(
        nombre text,
        puestos integrer,
        revisiones integrer,
        cuotas text,
        multas text,
        tesorero text,
        estado text,
        capital integrer,
        multas_global integrer,
        deudas integrer,
        multas_extra integrer
        )'''
    )
    base.commit()
    base.close()

    Pf.insertar_socio('ricaRdo zamorA', 10, nombre)

    with open('ArchivoControl.txt', 'w') as file:
        file.write(str(int(lineas[0]) + 1) + '\n' + nombre)

    tkm.showinfo('Base de datos','La base de datos ha sido creada.')

class root(tk.Tk):
    def __init__(self):
        super().__init__()

        self.w_h_screen(w_w = 580, h_w = 420)
        self.title('creacion de la base de datos')
        self.iconphoto(False, tk.PhotoImage(file='icono.ico'))

        text = '''El siguiente programa solamente crea una base de datos en la carpeta
        donde el programa principal se ejecuta, antes de crear la nueva base de datos
        asegurese de que la anterior base de datos este archivada el la carpeta de 
        almacenamiento y que el programa esta listo para iniciar un nuevo periodo. \n
        Por favor no cree una nueva base de datos mientras el programa esta usando una 
        base ya existente, esto podria comprometer todo el optimo funcionamiento del 
        programa entre tanto la perdida de todo el trabajo realizado y posiblemente
        no se pueda realizar la tabulacion de los datos obtenidos en todo el tiempo
        de funcionamiento.\n
        si es la primera vez que crea una base de datos asegurese de haber introducido
        un archivo de texto llamado "ArchivoControl" con el formato ".txt" a la carpeta
        y que este solo tenga un "1" escrito en su primera linea, asi la base de datos se
        creara correctamente, en caso de no haberlo o de de confuciones el boton
        "crear archivo .txt" resolvera este problema'''

        self.label = tk.Label(self, text=text, font='calibri 12')
        self.label.pack()

        self.button = tk.Button(self, text='crear base de datos', font='calibri 15', command=self.crear_bd)
        self.button.pack()

        self.button_arch = tk.Button(self, text='crear archivo .txt', font='calibri 15', command=self.crear_archivo_control)
        self.button_arch.pack()

    def crear_bd(self):
        pregunta = tkm.askyesno('Base de datos', '¿desea crear la base de datos?')
        if pregunta == True:
            clave = tks.askinteger('Contraseña', 'Para continuar por favor\nintroduzca la contraseña.')
            if clave == 79842130:
                crear_base_de_datos()
            else:
                tkm.showwarning('Error', 'la contraseña no es correcta.')
        else:
            tkm.showwarning('Error', 'Bueno, gracias por intentalo.')
        self.destroy()

    def crear_archivo_control(self):
        pregunta = tkm.askyesno('Archivo', '¿desea crear el archivo de control?')
        if pregunta == True:
            clave = tks.askinteger('Contraseña', 'Para continuar por favor\nintroduzca la contraseña.')
            if clave == 79842130:
                with open('ArchivoControl.txt', 'w') as f:
                    f.write('1')
                tkm.showinfo('Archivo de control','El archivo ha sido creado.')
            else:
                tkm.showwarning('Error', 'La contraseña no es correcta.')
        else:
            tkm.showwarning('Error', 'Bueno, gracias por intentalo.')
    
    def w_h_screen(self, w_w = 600, h_w = 500):

        width_window = w_w
        height_window = h_w

        width_screen = self.winfo_screenwidth()
        height_screen = self.winfo_screenheight()

        x = (width_screen - width_window) // 2
        y = (height_screen - height_window) // 2

        self.geometry(f'{width_window}x{height_window}+{x}+{y}')

if __name__ == '__main__':
    root().mainloop()