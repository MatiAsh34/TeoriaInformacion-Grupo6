from compresor import *

if __name__=='__main__':
    with open("ejemplo_entrada.txt", "r") as archivo:   #Obtención de la cadena desde un archivo txt
        ejemplo = archivo.read() 
    compresor1 = Compresor()
    compresor1.BWT(ejemplo)
    compresor1.transiciones()
    compresor1.shannon()
    compresor1.codificacion()
    compresor1.guardar_json()