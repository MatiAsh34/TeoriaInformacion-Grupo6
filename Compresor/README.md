Este proyecto permite comprimir y descomprimir archivos de texto usando los algoritmos:

    - BWT (Burrows–Wheeler Transform)
    - Modelo de Markov de orden 1
    - Codificación de Shannon

La compresión genera un archivo comprimido.json y la descompresión reconstruye el texto original.

Requisitos previos

    - Tener instalado Python 3.10 o superior
    - Instalar las librerías necesarias ejecutando en la terminal:
        pip install numpy

El texto de entrada debe terminar con el símbolo $. Este símbolo indica el final del texto y es necesario para que la transformación BWT funcione correctamente.