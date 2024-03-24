import tkinter as tk 
import tkinter.messagebox as tkm
import tkinter.simpledialog as tks
import sqlite3 as sql
import datetime

def modificar_string(s, elemento, modificador):
    lista_s = [i for i in s]
    lista_s[elemento-1] = modificador
    new_s = ''
    for i in lista_s:
        new_s += i
    return new_s

def fecha_string_formato(fecha):
    s = fecha.split('/')
    s = list(map(int, s))
    return datetime.datetime(*s)

def crear_listado_de_fechas(primera_fecha, dobles, semanas=50):
    fecha = fecha_string_formato(primera_fecha)
    dias = 7
    fechas = []
    n_semanas = semanas - len(dobles)
    for i in range(0, n_semanas):
        new_f = fecha + datetime.timedelta(days=dias*i)
        f_new = new_f.strftime('%Y/%m/%d/%H')
        if f_new in dobles:
            fechas.append(f_new)
        fechas.append(f_new)
    for i in dobles:
        if i not in fechas:
            return False
    return fechas

def rectify(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

def leer_ajuste_n(n, nombre_b):
    base = sql.connect(nombre_b)
    cursor = base.cursor()
    instruc = f"SELECT valor FROM ajustes WHERE rowid = {n}"
    cursor.execute(instruc)
    datos = cursor.fetchall()
    base.commit()
    base.close()
    return datos[0][0]

def preguntar_la_clave(clave_p):
    status = False

    text = '''los parametros que se pueden modificar en la siguiente ventana repercuten 
en el optimo funcionamiento del programa, por lo ello se necesita una
clave de acceso para acceder a ellos, por favor digite la clave de acceso'''

    clave = tks.askstring('contraseña', text,)

    try:
        clave = clave.strip()
    except:
        tkm.showwarning('error', 'bueno, gracias por intentalo')
        return status

    if clave == clave_p:
        status = True
    elif clave == '':
        tkm.showwarning('error', 'la contraseña no puede estar vacia')
    else:
        tkm.showwarning('error', 'la contraseña no es correcta')
    
    return status

if __name__ == '__main__':
    pass