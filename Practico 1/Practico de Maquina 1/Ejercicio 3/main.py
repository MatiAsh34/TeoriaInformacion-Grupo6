from entropia_redundancia import *

if __name__ == "__main__":
    nombre = input("Ruta o nombre de archivo: ")
    entropia_redundancia = calculo_entropia_redundancia()
    try:
        res = entropia_redundancia.analizar(nombre)
        for k, v in res.items():
            print(f"{k}: {v}")
    except Exception as e:
        print("Error:", e)
