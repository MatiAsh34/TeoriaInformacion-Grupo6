from informacion_mutua import *

if __name__ == "__main__":
    R = int(input("INDIQUE QUE TIPO DE CANAL: 2 binario 3 ternario 4 cuaternario: "))
    canal = CanalRario(R)

    canal.leer_entrada()
    canal.leer_matriz()
    canal.imprimir_matriz()

    canal.calcular_probabilidad_salida()
    canal.calcular_entropia()
    canal.calcular_entropia_condicionada()
    canal.calcular_informacion_mutua()
