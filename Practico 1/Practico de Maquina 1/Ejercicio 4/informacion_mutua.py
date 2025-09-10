import numpy as np
import math

class CanalRario:
    def __init__(self, R: int):
        self.R = R
        self.matriz = np.zeros((R, R))
        self.entrada = np.zeros(R)
        self.probabilidad_salida = np.zeros(R)
        self.entropia = 0.0
        self.entropia_condicionada = 0.0
        self.informacion_mutua = 0.0

    def leer_entrada(self):
        print("Probabilidades de entrada: ")
        for i in range(self.R):
            self.entrada[i] = float(input())

    def leer_matriz(self):
        for i in range(self.R):
            for j in range(self.R):
                self.matriz[i][j] = float(input())

    def imprimir_matriz(self):
        print("\nMatriz de probabilidad: ")
        for i in range(self.R):
            for j in range(self.R):
                print(f"{self.matriz[i][j]}", end=" ")
            print()  

    def calcular_probabilidad_salida(self):
        for j in range(self.R):
            aux = 0.0
            for i in range(self.R):
                aux += self.entrada[i] * self.matriz[i][j]
            self.probabilidad_salida[j] = aux
        print("Probabilidad de salida: ",self.probabilidad_salida)

    def calcular_entropia(self):
        for i in range(self.R):
            self.entropia += self.probabilidad_salida[i] * math.log2(1 / self.probabilidad_salida[i])
        print("Entropia: ",self.entropia)

    def calcular_entropia_condicionada(self):
        for i in range(self.R):
            self.entropia_condicionada += self.matriz[i][0] * math.log2(1 / self.matriz[i][0])
        print("Entropia condicionada: ",self.entropia_condicionada)

    def calcular_informacion_mutua(self):
        self.informacion_mutua = self.entropia - self.entropia_condicionada
        print("Informacion mutua: ",self.informacion_mutua)


