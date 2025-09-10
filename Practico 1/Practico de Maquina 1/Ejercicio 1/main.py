from archivo_wav import * 

if __name__ == "__main__":
    archivo = input("Ingrese el nombre del archivo .wav: ")
    wav = Archivo_wav(archivo)

    if not wav.validar_extension():
        print("El archivo no tiene extensión .wav")
    else:
        try:
            wav.leer_header()
            wav.mostrar_header()
        except Exception as e:
            print("Error al leer el archivo:", e)
