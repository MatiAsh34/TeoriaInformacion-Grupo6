import os
from persona import *

if __name__ == "__main__":
    personas = []
    for i in range(20):
        nombre = f"Persona{i+1}"
        direccion = f"Calle {i+1}"
        dni = str(30000000 + i)
        campos = ["S" if i % 2 == 0 else "N" for _ in range(8)]
        personas.append(Persona(nombre, direccion, dni, campos))

    escribir_fijo(personas, "fijos.dat")
    escribir_variable(personas, "variable.dat")

    leidos_fijo = leer_fijo("fijos.dat")
    leidos_variable = leer_variable("variable.dat")

    print("Tamaño fijos.dat:", os.path.getsize("fijos.dat"), "bytes")
    print("Tamaño variable.dat:", os.path.getsize("variable.dat"), "bytes")