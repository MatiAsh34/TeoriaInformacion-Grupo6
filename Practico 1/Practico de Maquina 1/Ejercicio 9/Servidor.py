import socket
import zlib

ALFABETO = "ABCDEFGH"

def descomprimir_alfabeto(letters, pad_bits):
    """Convierte letras A..H en bytes"""
    bits = "".join(f"{ALFABETO.index(ch):03b}" for ch in letters)
    if pad_bits:
        bits = bits[:-pad_bits]  # sacar el padding
    return bytes(int(bits[i:i+8], 2) for i in range(0, len(bits), 8))

ip = "0.0.0.0"
puerto = 5555
servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor.bind((ip, puerto))
servidor.listen(1)

print(f"[*] Esperando conexiones en {ip}:{puerto}")
cliente, direccion = servidor.accept()

print(f"[*] Conexión establecida con {direccion[0]}:{direccion[1]}")

data = cliente.recv(65536).decode("utf-8")  # recibir como texto A..H + padding, recibe 64KB
letters, pad_bits = data.split("|")

compressed = descomprimir_alfabeto(letters, int(pad_bits))

# Descomprimir utilizando la librería zlib
restored = zlib.decompress(compressed)

with open("archivo_recibido.txt", "wb") as f:
    f.write(restored)

print("Archivo recibido y guardado como archivo_recibido.txt")

cliente.close()
servidor.close()
