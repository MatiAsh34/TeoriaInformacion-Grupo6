from cuil_cuit import *

if __name__ == '__main__':
    cuit = input('Ingrese un cuit: ')
    validacion = cuil_cuit(cuit)
    if validacion.validar() == True:
        print(f"El cuit: {cuit}, es valido")
    else:
        print(f"El cuit: {cuit}, no es valido")