from comparativa_cadenas import *

if __name__ == '__main__':
	cadena1=input("Ingrese primer cadena: ")
	cadena2= input("Ingrese segunda cadena: ")
	comparativa = Comparativa(cadena1,cadena2)
	probabilidad = comparativa.comparar_cadenas()
	print("La probabilidad de que las cadenas sean iguales es de: ", probabilidad)
