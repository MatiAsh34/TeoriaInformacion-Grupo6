import os

class Persona:
    def __init__(self, nombre, direccion, dni, campos):
        self.nombre = nombre
        self.direccion = direccion
        self.dni = dni
        self.campos = campos  

def escribir_fijo(personas, archivo):
    with open(archivo, "w", encoding="utf-8") as f:
        for p in personas:
            nombre = p.nombre.ljust(30)[:30]
            direccion = p.direccion.ljust(40)[:40]
            dni = p.dni.ljust(8)[:8]
            campos = "".join(p.campos)

            registro = nombre + direccion + dni + campos + "\n"
            f.write(registro)

def leer_fijo(archivo):
    personas = []
    with open(archivo, "r", encoding="utf-8") as f:
        for linea in f:
            nombre = linea[0:30].strip()
            direccion = linea[30:70].strip()
            dni = linea[70:78].strip()
            campos = list(linea[78:86])
            personas.append(Persona(nombre, direccion, dni, campos))
    return personas

def escribir_variable(personas, archivo):
    with open(archivo, "w", encoding="utf-8") as f:
        for p in personas:
            registro = ";".join([p.nombre, p.direccion, p.dni] + p.campos)
            f.write(registro + "\n")

def leer_variable(archivo):
    personas = []
    with open(archivo, "r", encoding="utf-8") as f:
        for linea in f:
            partes = linea.strip().split(";")
            nombre, direccion, dni = partes[0], partes[1], partes[2]
            campos = partes[3:]
            personas.append(Persona(nombre, direccion, dni, campos))
    return personas