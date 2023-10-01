import csv
def leer(ruta):
    with open(ruta, "r", newline="") as archivo:
        lector = csv.reader(archivo)
        for fila in lector:
            id,nombre,titulo,institucion,email = fila
            print(nombre,titulo,institucion,email)

