import re

class cuil_cuit:
    def __init__(self, cuit):
        self.base = [5, 4, 3, 2, 7, 6, 5, 4, 3, 2]
        cuit_sin_guion = cuit.replace("-", "")
        self.cuit = cuit_sin_guion

    def validar(self):
        band = bool
        if len(self.cuit) != 11:
            band = False

        aux = 0
        for i in range(10):
            aux += int(self.cuit[i]) * self.base[i]

        aux = 11 - (aux - (int(aux / 11) * 11))

        if aux == 11:
            aux = 0
        if aux == 10:
            aux = 9

        band = aux == int(self.cuit[10])

        return band