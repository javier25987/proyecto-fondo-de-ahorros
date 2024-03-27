import tkinter.messagebox as tkm
import tkinter.simpledialog as tks
import sqlite3 as sql
import datetime

def modificar_string(s, elemento, modificador):
    lista_s = [i for i in s]
    lista_s[elemento] = modificador
    new_s = ''.join(lista_s)
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

def leer_ajuste_n(ajuste_n, nombre_b):
    base = sql.connect(nombre_b)
    cursor = base.cursor()
    instruc = f"SELECT valor FROM ajustes WHERE rowid = {ajuste_n}"
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

def insertar_socio(nombre, puestos, nombre_b, n=50):
    base = sql.connect(nombre_b)
    cursor = base.cursor()
    basico = 'n'*n
    multas = '0'*n
    nombre = nombre.lower()
    instruc = f"INSERT INTO socios VALUES ('{nombre}', {puestos}, '{basico}', '{multas}', '{basico}', 'activo', 0, 0, 0, 0 )"
    cursor.execute(instruc)
    base.commit()
    base.close()

def cargar_datos_texto(nombre_b='', usuario=1, tabla='', columna='', nuevo_valor=''):
    base = sql.connect(nombre_b)
    cursor = base.cursor()
    instruc = f"UPDATE {tabla} SET {columna} = '{nuevo_valor}' WHERE rowid = {usuario}"
    cursor.execute(instruc)
    base.commit()
    base.close()

def cargar_datos_numeros(nombre_b='', usuario=1, tabla='', columna='', nuevo_valor=''):
    base = sql.connect(nombre_b)
    cursor = base.cursor()
    instruc = f"UPDATE {tabla} SET {columna} = {nuevo_valor} WHERE rowid = {usuario}"
    cursor.execute(instruc)
    base.commit()
    base.close()

def pagar_cuotas(usuario=1, n=1, nombre_b=''):
    base = sql.connect(nombre_b)
    cursor = base.cursor()
    instruc = f"SELECT cuotas FROM socios WHERE rowid = {usuario}"
    cursor.execute(instruc)
    cuota_cursor = cursor.fetchall()[0][0]
    base.commit()
    base.close()

    for _ in range(n):
        execute = [i for i in cuota_cursor if i != 'p']
        posicion = cuota_cursor.find(execute[0])
        cuota_cursor = modificar_string(cuota_cursor, posicion, 'p')

    cargar_datos_texto(nombre_b=nombre_b, usuario=usuario, tabla='socios', columna='cuotas', nuevo_valor=cuota_cursor)

def sumar_una_multa(usuario=1, semana=1, nombre_b=''):
    base = sql.connect(nombre_b)
    cursor = base.cursor()
    instruc = f"SELECT multas FROM socios WHERE rowid = {usuario}"
    cursor.execute(instruc)
    cuota_cursor = cursor.fetchall()[0][0]
    base.commit()
    base.close()

    cuota_cursor = [i for i in cuota_cursor]
    cuota_cursor = list(map(int, cuota_cursor))
    cuota_cursor[semana-1] = cuota_cursor[semana-1] + 1
    cuota_cursor = list(map(str, cuota_cursor))
    cuota_cursor = ''.join(cuota_cursor)

    cargar_datos_texto(nombre_b=nombre_b, usuario=usuario, tabla='socios', columna='multas', nuevo_valor=cuota_cursor)

def pagar_una_multa(usuario=1, nombre_b=''):
    base = sql.connect(nombre_b)
    cursor = base.cursor()
    instruc = f"SELECT multas FROM socios WHERE rowid = {usuario}"
    cursor.execute(instruc)
    cuota_cursor = cursor.fetchall()[0][0]
    base.commit()
    base.close()

    cuota_cursor = list(map(int, cuota_cursor))

    k = 0
    for i in cuota_cursor:
        if i != 0:
            cuota_cursor[k] = i - 1
            break
        k += 1

    cuota_cursor = list(map(str, cuota_cursor))
    cuota_cursor = ''.join(cuota_cursor)

    cargar_datos_texto(nombre_b=nombre_b, usuario=usuario, tabla='socios', columna='multas', nuevo_valor=cuota_cursor)

def pagar_una_multa(usuario=1, nombre_b=''):
    base = sql.connect(nombre_b)
    cursor = base.cursor()
    instruc = f"SELECT multas FROM socios WHERE rowid = {usuario}"
    cursor.execute(instruc)
    cuota_cursor = cursor.fetchall()[0][0]
    base.commit()
    base.close()

    value = False
    cuota_cursor = list(map(int, cuota_cursor))

    k = 0
    for i in cuota_cursor:
        if i != 0:
            cuota_cursor[k] = i - 1
            value = True
            break
        k += 1
    else:
        tkm.showwarning('error', 'en teoria es imposible que un usuario\npague cuotas cuando no las debe\ngenial, encontraste un bug')

    cuota_cursor = list(map(str, cuota_cursor))
    cuota_cursor = ''.join(cuota_cursor)

    if value:
        cargar_datos_texto(nombre_b=nombre_b, usuario=usuario, tabla='socios', columna='multas', nuevo_valor=cuota_cursor)

if __name__ == '__main__':
    pagar_cuotas(usuario=1,nombre_b='FONDO_1_2024.db')