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

def rectificar_numero(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

def leer_ajuste_n(ajuste_n=0, nombre_b=''):
    base = sql.connect(nombre_b)
    cursor = base.cursor()
    instruc = f"SELECT valor FROM ajustes WHERE rowid = {ajuste_n}"
    cursor.execute(instruc)
    datos = cursor.fetchall()
    base.commit()
    base.close()
    return datos[0][0]

def leer_en_socios(usuario_n=0, columna='', nombre_b=''):
    if usuario_n != 0:
        base = sql.connect(nombre_b)
        cursor = base.cursor()
        instruc = f"SELECT {columna} FROM socios WHERE rowid = {usuario_n}"
        cursor.execute(instruc)
        datos = cursor.fetchall()
        base.commit()
        base.close()
        return datos[0][0]
    else:
        return '0'*50

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

def insertar_socio(nombre, puestos, nombre_b, n=50):
    base = sql.connect(nombre_b)
    cursor = base.cursor()
    basico = 'n'*n
    multas = '0'*n
    nombre = nombre.lower()
    nombre = nombre.strip()
    nombre = ' '.join(nombre.split())
    instruc = f"INSERT INTO socios VALUES ('{nombre}', {puestos}, 0, '{basico}', '{multas}', '{basico}', 'activo', 0, 0, 0, 0 )"
    cursor.execute(instruc)
    base.commit()
    base.close()

    k = leer_ajuste_n(ajuste_n=7, nombre_b=nombre_b)
    k = str(int(k) + 1)

    cargar_datos_numeros(nombre_b=nombre_b, usuario=7, tabla='ajustes', columna='valor', nuevo_valor=k)

def pagar_n_cuotas(usuario=1, n=1, nombre_b='', tesorero='1'):
    cuota_cursor= leer_en_socios(usuario_n=usuario, columna='cuotas', nombre_b=nombre_b)
    tesorero_cursor = leer_en_socios(usuario_n=usuario, columna='tesorero', nombre_b=nombre_b)

    for _ in range(n):
        execute = [i for i in cuota_cursor if i != 'p']
        posicion = cuota_cursor.find(execute[0])
        cuota_cursor = modificar_string(cuota_cursor, posicion, 'p')
        tesorero_cursor = modificar_string(tesorero_cursor, posicion, tesorero)

    cargar_datos_texto(nombre_b=nombre_b, usuario=usuario, tabla='socios', columna='cuotas', nuevo_valor=cuota_cursor)
    cargar_datos_texto(nombre_b=nombre_b, usuario=usuario, tabla='socios', columna='tesorero', nuevo_valor=tesorero_cursor)

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
    cuota_cursor[semana] = cuota_cursor[semana] + 1
    cuota_cursor = list(map(str, cuota_cursor))
    cuota_cursor = ''.join(cuota_cursor)

    cargar_datos_texto(nombre_b=nombre_b, usuario=usuario, tabla='socios', columna='multas', nuevo_valor=cuota_cursor)

def pagar_una_multa(usuario=1, nombre_b=''):
    base = sql.connect(nombre_b)
    cursor = base.cursor()
    instruc = f"SELECT multas FROM socios WHERE rowid = {usuario}"
    cursor.execute(instruc)
    multa_cursor = cursor.fetchall()[0][0]
    base.commit()
    base.close()

    value = False
    multa_cursor = list(map(int, multa_cursor))

    k = 0
    for i in multa_cursor:
        if i != 0:
            multa_cursor[k] = i - 1
            value = True
            break
        k += 1
    else:
        tkm.showwarning('error', 'no hay multas por pagar')

    multa_cursor = list(map(str, multa_cursor))
    multa_cursor = ''.join(multa_cursor)

    if value:
        cargar_datos_texto(nombre_b=nombre_b, usuario=usuario, tabla='socios', columna='multas', nuevo_valor=multa_cursor)

def crear_y_cargar_el_calendario_general(fecha_inicial='', dobles=[], nombre_b=''):
    fechas = crear_listado_de_fechas(primera_fecha=fecha_inicial, dobles=dobles)

    if fechas == False:
        tkm.showwarning('error', 'faltan datos o las fechas\ndobles no son validas')
    else:
        s_fechas = '-'.join(fechas)
        cargar_datos_texto(nombre_b=nombre_b, usuario=6, tabla='ajustes', columna='valor', nuevo_valor=s_fechas)
        tkm.showinfo('info', 'el calendario ha sido creado')

def string_calendario_usuario(usuario=0, nombre_b=''):
    calendario = leer_ajuste_n(ajuste_n=6, nombre_b=nombre_b).split('-')
    if usuario == 0:
        s = ''
        for i in range(25):
            s += calendario[i][:-3]+'  ____'+'  T__'+'  _'+ '\t' +calendario[i+25][:-3]+'  ____'+'  T__'+ '  _'+'\n'
        return s
    else:
        multas = [i for i in leer_en_socios(usuario_n=usuario, columna='multas', nombre_b=nombre_b)]
        cuotas = [i for i in leer_en_socios(usuario_n=usuario, columna='cuotas', nombre_b=nombre_b)]
        tesoreros = [i for i in leer_en_socios(usuario_n=usuario, columna='tesorero', nombre_b=nombre_b)]
        s = ''
        for i in range(25):
            r_m_1 = multas[i]
            r_c_1 = cuotas[i]
            r_t_1 = tesoreros[i]
            k = i + 25
            r_m_2 = multas[k]
            r_c_2 = cuotas[k]
            r_t_2 = tesoreros[k]

            if r_m_1 == '0':
                m_1 = '  _'
            else:
                m_1 = f'  {r_m_1}'
            
            if r_c_1 == 'p':
                c_1 = '  pago'
            elif r_c_1 == 'd':
                c_1 = '  debe'
            else:
                c_1 = '  ____'
            
            if r_t_1 == 'n':
                t_1 = '  T__'
            else:
                t_1 = f'  T_{r_t_1}'

            if r_m_2 == '0':
                m_2 = '  _'
            else:
                m_2 = f'  {r_m_2}'
            
            if r_c_2 == 'p':
                c_2 = '  pago'
            elif r_c_2 == 'd':
                c_2 = '  debe'
            else:
                c_2 = '  ____'
            
            if r_t_2 == 'n':
                t_2 = '  T__'
            else:
                t_2 = f'  T_{r_t_2}'
            
            s += calendario[i][:-3] + c_1 + t_1 + m_1 + '\t' + calendario[k][:-3] + c_2 + t_2 + m_2 + '\n'

        return s

def rectificar_nombre(nombre):
    nombre = nombre.split()
    nombre = list(map(lambda x: modificar_string(x, 0, x[0].upper()), nombre))
    return ' '.join(nombre)

def titulo_de_usuario(usuario=0, nombre_b=''):
    if usuario == 0:
        s = '№0   usuario aun no identificado          №puestos: x'
        return s
    else:
        nombre = leer_en_socios(usuario_n=usuario, columna='nombre', nombre_b=nombre_b)
        p = leer_en_socios(usuario_n=usuario, columna='puestos', nombre_b=nombre_b)
        s = f'№{usuario}   {rectificar_nombre(nombre)}          №puestos: {p}'
        return s
    
def arreglar_asuntos(usuario=1, nombre_b=''):
    calendario = leer_ajuste_n(ajuste_n=6, nombre_b=nombre_b).split('-')
    calendario = list(map(lambda x: list(map(lambda k: int(k), x.split('/'))), calendario))
    calendario = list(map(lambda x: datetime.datetime(*x), calendario))
    fecha_actual = datetime.datetime.now()
    revisiones = int(leer_en_socios(usuario_n=usuario, columna='revisiones', nombre_b=nombre_b))
    cuotas = [i for i in leer_en_socios(usuario_n=usuario, columna='cuotas', nombre_b=nombre_b)]
    lista_revisiones = list(map(lambda x: x > fecha_actual, calendario))
    n_semanas_pasadas = sum([1 for i in lista_revisiones if i == False])
    if n_semanas_pasadas > revisiones:
        for i in range(50):
            if calendario[i] > fecha_actual:
                break
            else:
                if cuotas[i] == 'p':
                    pass
                else:
                    sumar_una_multa(usuario=usuario, semana=i, nombre_b=nombre_b)
                    k = leer_en_socios(usuario_n=usuario, columna='cuotas', nombre_b=nombre_b)
                    k = modificar_string(k, i, 'd')
                    cargar_datos_texto(nombre_b=nombre_b, usuario=usuario, tabla='socios', columna='cuotas', nuevo_valor=k)
                    cargar_datos_numeros(nombre_b=nombre_b, usuario=usuario, tabla='socios', columna='revisiones', nuevo_valor=n_semanas_pasadas)
    else:
        pass

def mostrar_multas(usuario=0, nombre_b=''):
    if usuario == 0:
        return '_____ MULTAS _____\nno hay multas'
    calendario = leer_ajuste_n(ajuste_n=6, nombre_b=nombre_b).split('-')
    multas = multas = [int(i) for i in leer_en_socios(usuario_n=usuario, columna='multas', nombre_b=nombre_b)]
    multa = int(leer_ajuste_n(ajuste_n=2, nombre_b=nombre_b))
    puestos = leer_en_socios(usuario_n=usuario, columna='puestos', nombre_b=nombre_b)
    total = 0
    s = '______ MULTAS ______\n\n'
    if all(i == 0 for i in multas):
        s += 'no hay multas'
    else:
        for i in range(50):
            k = multas[i]
            if k != 0:
                j = k*multa*puestos
                s += f'{calendario[i][:-3]}: {j}\n'
                total += j
        s += f'\nTOTAL: {total}'
    return s

#fechas_dobles = ['2024/10/14/19', '2024/11/11/19']
#crear_y_cargar_el_calendario_general(fecha_inicial='2024/01/01/19', dobles=fechas_dobles, nombre_b='FONDO_1_2024.db')

if __name__ == '__main__':
    pass
    #pagar_n_cuotas(usuario=1, n=10, nombre_b='FONDO_1_2024.db', tesorero='1')