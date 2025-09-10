class Comparativa:
    def __init__(self, cadena1, cadena2):
        lista1=[]
        lista2=[]
        lista1=list(cadena1)
        lista2=list(cadena2)
        lista1.remove(" ")
        lista2.remove(" ")
        self.cadena1 = lista1
        self.cadena2 = lista2
    
    def comparar_cadenas(self):
        probabilidad = 0
        coincidencias = 0
        for i in range(len(self.cadena1)):
            j=0
            while j < len(self.cadena2):
                if self.cadena1[i]!= self.cadena2[j]:
                    j=j+1
                else:
                    coincidencias += 1
                    self.cadena2.pop(j)
        probabilidad = coincidencias/len(self.cadena1)
        return probabilidad