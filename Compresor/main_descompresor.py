from descompresor import *

if __name__=='__main__':
    descompresor1 = Descompresor()
    descompresor1.abrir_json()
    descompresor1.decodificar()
    cadena = descompresor1.BWT_inversa()
    with open("ejemplo_salida.txt", "w") as archivo:    #Creación de un archivo txt con la cadena decodificada
        archivo.write(cadena)