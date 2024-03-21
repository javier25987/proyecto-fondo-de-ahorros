import tkinter as tk 
import tkinter.messagebox as tkm
import tkinter.simpledialog as tks
import sqlite3 as sql
import datetime as dt

def insertar_ajuste(nombre_ajuste, valor, nombre_base):
    base = sql.connect(nombre_base)
    cursor = base.cursor()
    instruc = f"INSERT INTO ajustes VALUES ('{nombre_ajuste}', '{valor}')"
    cursor.execute(instruc)
    base.commit()
    base.close()

def insertar_socio(nombre, puestos, nombre_base, n=50):
    base = sql.connect(nombre_base)
    cursor = base.cursor()
    basico = 'n'*n
    instruc = f"INSERT INTO socios VALUES ('{nombre}', {puestos}, '{basico}', '{basico}', '{basico}', 'activo', 0, 0, 0, 0 )"
    cursor.execute(instruc)
    base.commit()
    base.close()

    
def crear_base_de_datos():
    nombre = 'FONDO_'
    with open('DatosImportantes.txt', 'r') as file:
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

    base = sql.connect(nombre)
    cursor = base.cursor()
    cursor.execute(
        '''CREATE TABLE socios(
        nombre text,
        puestos integrer,
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

    insertar_socio('ricardo', 50, nombre)

    with open('DatosImportantes.txt', 'w') as file:
        file.write(str(int(lineas[0]) + 1) + '\n' + nombre)

class root(tk.Tk):
    def __init__(self):
        super().__init__()

        self.geometry('800x300+50+50')
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
        de funcionamiento'''

        self.label = tk.Label(self, text=text, font='calibri 12')
        self.label.pack()

        self.button = tk.Button(self, text='crear base de datos', font='calibri 15', command=self.crear)
        self.button.pack()

    def crear(self):
        pregunta = tkm.askyesno('base de datos', 'desea crear la base de datos?')
        if pregunta == True:
            clave = tks.askinteger('contraseña', 'para continuar por favor\nintroduzca la contraseña')
            if clave == 79842130:
                crear_base_de_datos()
        self.destroy()

if __name__ == '__main__':
    root().mainloop()

