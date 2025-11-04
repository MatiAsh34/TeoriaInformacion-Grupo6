import json
import base64

class Descompresor:
    def __init__(self):
        self.__cadena_decodificada = ""     #Se almacena la cadena decodificada 
        self.__codigos_por_origen = {}      # origen -> {destino: codigo}
        self.__simbolo_inicial = ""         # primer símbolo de la BWT
        self.__cantidad_simbolos = 0        # Cantidad de simbolos de la cadena
        self.__bitstream = ""               # Flujo de bits 
        self.__inversos_por_origen = {}
        self.__longitud_maxima_por_origen = {}

    def abrir_json(self):   #Abre, lee, y decodifica de base64 la cadena recibida desde el JSON
        with open("comprimido.json", "r", encoding="utf-8") as archivo: 
            datos = json.load(archivo)

        #Carga todos los campos del JSON
        self.__codigos_por_origen = datos["codes"]    
        flujo_base64 = datos["bitstream_b64"]
        bits_relleno = int(datos.get("pad_bits", 0))
        self.__simbolo_inicial = datos["start_symbol"]
        self.__cantidad_simbolos = int(datos["n_symbols"])

        bytes_crudos = base64.b64decode(flujo_base64)   #Decodifica de Base64 a bytes y luego a cadena de bits binarios
        cadena_bits = "".join(f"{byte:08b}" for byte in bytes_crudos)

        if bits_relleno:
            cadena_bits = cadena_bits[:-bits_relleno]

        self.__bitstream = cadena_bits

        # Precalcula los diccionarios inversos
        self.__inversos_por_origen = {
            origen: {codigo: destino for destino, codigo in destinos.items()}
            for origen, destinos in self.__codigos_por_origen.items()
        }
        # Precalcula las longitudes máximas por contexto
        self.__longitud_maxima_por_origen = {
            origen: max((len(codigo) for codigo in destinos.values()), default=0)
            for origen, destinos in self.__codigos_por_origen.items()
        }

    def decodificar(self):  # Utilizando el diccionario obtenido del JSON, decodifica la cadena de bits
        bits = self.__bitstream
        salida = [self.__simbolo_inicial]
        indice = 0
        simbolo_actual = self.__simbolo_inicial

        while indice < len(bits) and len(salida) < self.__cantidad_simbolos:
            inversos = self.__inversos_por_origen.get(simbolo_actual, {})
            longitud_max = self.__longitud_maxima_por_origen.get(simbolo_actual, 0)

            longitud = 1

            while indice + longitud <= len(bits) and longitud <= longitud_max:
                fragmento = bits[indice:indice + longitud]
                simbolo_destino = inversos.get(fragmento)

                if simbolo_destino is not None:
                    salida.append(simbolo_destino)
                    simbolo_actual = simbolo_destino
                    indice += longitud
                    break
                longitud += 1


        self.__cadena_decodificada = "".join(salida)

    def BWT_inversa(self):  #Cálculo de la cadena original a partir de la cadena transformada
        n = len(self.__cadena_decodificada)
        tabla = [""] * n
        
        for _ in range(n):  #Reconstruye la tabla
            for i in range(n):
                tabla[i] = self.__cadena_decodificada[i] + tabla[i]
            tabla.sort()
        
        for fila in tabla:
            if fila.endswith('$'):
                return fila