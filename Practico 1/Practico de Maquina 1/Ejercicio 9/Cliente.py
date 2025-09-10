import socket
import zlib
from pathlib import Path

ALFABETO = "ABCDEFGH"

def comprimir_alfabeto(data: bytes):
    """Convierte bytes en letras A..H"""
    bits = "".join(f"{b:08b}" for b in data)
    rem = len(bits) % 3
    pad_bits = (3 - rem) % 3
    if pad_bits:
        bits += "0" * pad_bits
    letters = "".join(ALFABETO[int(bits[i:i+3], 2)] for i in range(0, len(bits), 3))
    return letters, pad_bits

servidor = "127.0.0.1"
puerto = 5555
archivo = Path(r'ejemplo.txt')
raw = archivo.read_bytes()

# Comprimir archivo utilizando la librería zlib
compressed = zlib.compress(raw, level=9)

letters, pad_bits = comprimir_alfabeto(compressed)
payload = f"{letters}|{pad_bits}"  # mandamos letras + padding usado, de esta forma 'ABCD | 2'

cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente.connect((servidor, puerto))
cliente.send(payload.encode("utf-8"))

print(f"Archivo {archivo.name} enviado al servidor.")

cliente.close()
