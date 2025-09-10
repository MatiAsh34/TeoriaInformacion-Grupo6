import os
import struct

class Archivo_bmp:
    _FILE_HDR_FMT = "<2sIHHI" 

    def __init__(self, filename: str):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.path = os.path.join(base_dir, filename)
        self.data = {}

    def validar_extension(self) -> bool:
        return self.path.lower().endswith(".bmp")

    def leer_header(self):
        with open(self.path, "rb") as f:
            file_hdr = f.read(14)
            sig, file_size, r1, r2, data_offset = struct.unpack(self._FILE_HDR_FMT, file_hdr)

            if sig != b"BM":
                raise ValueError("Signature inválida (no es 'BM').")

            dib_size = struct.unpack("<I", f.read(4))[0]
            f.seek(14)
            dib_bytes = f.read(dib_size)

        if dib_size >= 40:
            (size, width, height, planes, bitcount, comp, img_size,
             xppm, yppm, colors_used, colors_imp) = struct.unpack("<IiiHHIIiiII", dib_bytes[:40])
        else:
            raise ValueError(f"DIB header inesperado: {dib_size} bytes (mínimo 40).")

        self.data = {
            "Signature": sig.decode("ascii"),
            "FileSize": file_size,
            "DataOffset": data_offset,
            "DIB_Size": dib_size,
            "Width": width,
            "Height": height,
            "Planes": planes,
            "BitCount": bitcount,
            "Compression": comp,
            "ImageSize": img_size,
            "XPixelsPerM": xppm,
            "YPixelsPerM": yppm,
            "ColorsUsed": colors_used,
            "ColorsImportant": colors_imp,
        }

    def mostrar_header(self):
        if not self.data:
            print("Todavía no se leyó la cabecera.")
            return
        print("\nCabecera BMP:\n")
        for k, v in self.data.items():
            print(f"{k}: {v}")