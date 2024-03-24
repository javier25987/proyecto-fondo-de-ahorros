import sqlite3 as sql

def leer_ajuste_n(n):
    base = sql.connect('FONDO_1_2024.db')
    cursor = base.cursor()
    instruc = f"SELECT valor FROM ajustes WHERE rowid = {n}"
    cursor.execute(instruc)
    datos = cursor.fetchall()
    base.commit()
    base.close()
    return datos[0][0]

dato = leer_ajuste_n(1)
print(dato)
print(type(dato))