import struct

class Archivo_wav:
    def __init__(self, filename):
        self.filename = filename
        self.header_data = {}

    def validar_extension(self):
        return self.filename.lower().endswith(".wav")

    def leer_header(self):
        with open(self.filename, "rb") as f:
            header = f.read(44)
            campos = struct.unpack('<4sI4s4sIHHIIHH4sI', header)

            self.header_data = {
                "ChunkID": campos[0].decode('ascii'),
                "ChunkSize": campos[1],
                "Format": campos[2].decode('ascii'),
                "Subchunk1ID": campos[3].decode('ascii'),
                "Subchunk1Size": campos[4],
                "AudioFormat": campos[5],
                "NumChannels": campos[6],
                "SampleRate": campos[7],
                "ByteRate": campos[8],
                "BlockAlign": campos[9],
                "BitsPerSample": campos[10],
                "Subchunk2ID": campos[11].decode('ascii'),
                "Subchunk2Size": campos[12]
            }

    def mostrar_header(self):
        if not self.header_data:
            print("No se ha leído la cabecera todavía.")
            return
        print("\nCabecera WAV:\n")
        for k, v in self.header_data.items():
            print(f"{k}: {v}")
