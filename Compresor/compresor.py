import numpy as np
import math
import json
import base64

class Compresor:
    def __init__(self):
        self.__cadena_bwt= ""   #Cadena transformada por BWT
        self.__codigo_completo = "" #Cadena de bits final
        self.__caracteres = []  #Símbolos distintos de la cadena original
        self.__transiciones = None  #Tabla con la cantidad de transiciones por símbolo
        self.__diccionario_transiciones = {} #Diccionario de transiciones
        self.__diccionario_anidado = None   #Diccionario de transiciones anidado
        

    def BWT (self, cadena): #Obtención la cadena transformada por BWT 
        nueva_cadena = cadena
        aux = ""
        aux_caracter = ""
        #Creamos una tabla nxn siendo n el número de carácteres de la cadena
        tabla_burro = np.empty([len(nueva_cadena),len(nueva_cadena)], dtype="U6")
        for i in range(len(nueva_cadena)):
            for j in range(len(nueva_cadena)):
                tabla_burro[i][j]=nueva_cadena[j]
            aux = nueva_cadena[1:]
            aux_caracter = nueva_cadena[0]
            nueva_cadena = aux + aux_caracter
        
        tabla_burro_ord = tabla_burro[np.lexsort(tabla_burro.T[::-1])]
        for j in range(len(nueva_cadena)):
            self.__cadena_bwt += tabla_burro_ord[j][len(nueva_cadena)-1]
    
    def transiciones(self): #Obtención de las transiciones de la cadena transformada
        self.__caracteres = sorted(set(self.__cadena_bwt))  #Obtención de carácteres únicos y ordenados
        n = len(self.__caracteres)

        char_a_indice = {char: idx for idx, char in enumerate(self.__caracteres)}   #Creación de diccionario para mapear caracteres a índices

        self.__transiciones = np.zeros((n, n), dtype=int)

        for i in range(len(self.__cadena_bwt) - 1):
            caracter_actual = self.__cadena_bwt[i]
            caracter_siguiente = self.__cadena_bwt[i + 1]
            
            indice_actual = char_a_indice[caracter_actual]
            indice_siguiente = char_a_indice[caracter_siguiente]
            
            self.__transiciones[indice_actual][indice_siguiente] += 1

    def __decimal_a_binario(self, decimal, longitud):   #Función auxiliar para utilizar en Shannon
        binario = ""
        for _ in range(longitud):
            decimal *= 2
            if decimal >= 1:
                binario += "1"
                decimal -= 1
            else:
                binario += "0"
        return binario

    def __codigos_por_origen(self): #Obtención de la anidación del diccionario de transiciones 
        anidado = {}
        for par, codigo in self.__diccionario_transiciones.items():
            origen, destino = par[0], par[1]
            anidado.setdefault(origen, {})[destino] = codigo
        return anidado
    
    def __empaquetar_bits(self, cadena_bits: str): # Empaqueta la cadena de bits en bitstream
        if not cadena_bits:
            return b"", 0  # Si no hay bits, devuelve vacío y 0 relleno

        bits_faltantes = (8 - (len(cadena_bits) % 8)) % 8   #Cálculo de cuántos bits faltan para completar el último byte
        bits_completos = cadena_bits + ("0" * bits_faltantes)   

        valor_entero = int(bits_completos, 2)   #Conversión de la cadena binaria en entero
        cantidad_bytes = len(bits_completos) // 8
        bytes_empaquetados = valor_entero.to_bytes(cantidad_bytes, "big")
        return bytes_empaquetados, bits_faltantes
  

    def shannon(self): #Generación de la codificación de Shannon usando la matriz de transiciones
        n = len(self.__caracteres)
        
        for i, origen in enumerate(self.__caracteres):  #Obtención de las transiciones válidas desde este origen
            destinos_validos = []   
            for j, destino in enumerate(self.__caracteres):
                if self.__transiciones[i][j] > 0:
                    conteo = self.__transiciones[i][j]
                    destinos_validos.append((destino, conteo))
            
            if len(destinos_validos) == 0:
                continue    #Si no hay destinos válidos salta a la siguiente iteración del bucle
            
            total = sum([conteo for _, conteo in destinos_validos]) #Cálculo total de transiciones desde este origen
            
            probabilidades = [(destino, conteo/total) 
                            for destino, conteo in destinos_validos]
            
            probabilidades.sort(key=lambda x: x[1], reverse=True)
            
            
            acumulada = 0   
            for destino, prob in probabilidades:    #Cálculo de probabilidades acumuladas y códigos
                longitud = math.ceil(math.log2(1/prob)) if prob > 0 else 1  #Cálculo de la longitud del código según la fórmula de Shannon
                
                fa = acumulada
                
                codigo = self.__decimal_a_binario(fa, longitud)
                if not codigo:
                    codigo = '0'
                
                self.__diccionario_transiciones[f"{origen}{destino}"] = codigo
                
                acumulada += prob
        
        self.__diccionario_anidado = self.__codigos_por_origen()

    def codificacion(self): #A partir de la cadena BWT, codificamos utilizando el diccionario de transiciones
        for i in range(len(self.__cadena_bwt) - 1):
            actual = self.__cadena_bwt[i]
            siguiente = self.__cadena_bwt[i + 1]
            clave = f"{actual}{siguiente}"
            codigo = self.__diccionario_transiciones.get(clave, '?')
            self.__codigo_completo += codigo

    def guardar_json(self):
        # start_symbol: primer símbolo de la cadena BWT (tu L)
        start_symbol = self.__cadena_bwt[0] if self.__cadena_bwt else ""

        
        raw_bytes, pad = self.__empaquetar_bits(self.__codigo_completo)
        bitstream_b64 = base64.b64encode(raw_bytes).decode("ascii")

        # 2) Usar el diccionario anidado por contexto que ya creaste
        datos = {
            "codes": self.__diccionario_anidado,   # origen -> {destino: codigo}
            "bitstream_b64": bitstream_b64,        # bytes empaquetados en base64
            "pad_bits": pad,                       # cuantos '0' de relleno al final
            "start_symbol": start_symbol,
            "n_symbols": len(self.__cadena_bwt)
        }

        # 3) JSON compacto (sin espacios ni indentación)
        with open("comprimido.json", "w", encoding="utf-8") as f:
            json.dump(datos, f, ensure_ascii=False, separators=(',', ':'))

    def guardar_json(self): #Se guarda el JSON con la cadena comprimida con los datos necesarios para descomprimir
        simbolo_inicial = self.__cadena_bwt[0] if self.__cadena_bwt else ""

        bytes_empaquetados, bits_relleno = self.__empaquetar_bits(self.__codigo_completo) #Empaquetar el código binario completo en bytes

        flujo_bits_base64 = base64.b64encode(bytes_empaquetados).decode("ascii") #Conversión de los bytes empaquetados a texto base64 para poder guardarlos en JSON

        datos = {
            "codes": self.__diccionario_anidado,    # origen -> {destino: codigo}
            "bitstream_b64": flujo_bits_base64,     # bytes empaquetados codificados en base64
            "pad_bits": bits_relleno,               # cuántos '0' se agregaron al final
            "start_symbol": simbolo_inicial,        # primer símbolo de la BWT
            "n_symbols": len(self.__cadena_bwt)     # longitud total de la cadena
        }

        with open("comprimido.json", "w", encoding="utf-8") as archivo:
            json.dump(datos, archivo, ensure_ascii=False, separators=(',', ':'))