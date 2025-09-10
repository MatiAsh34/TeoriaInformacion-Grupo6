from archivo_bmp import *

if __name__ == "__main__":
    nombre = input("Ingrese el nombre del archivo .bmp: ")
    bmp = Archivo_bmp(nombre)

    if not bmp.validar_extension():
        print("El archivo no tiene extensión .bmp")
    else:
        try:
            bmp.leer_header()
            bmp.mostrar_header()
        except Exception as e:
            print("Error al leer/validar el BMP:", e)
