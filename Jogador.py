from xmlrpc.client import boolean


class Jogador:

    def __init__(self, nome, flagCor=int, turno=boolean):
        self.nome = nome
        self.flagCor = flagCor
        self.turno = turno

    # --------- Getters e Setters --------------
    def getNome(self): # Amarelo ou preto
        return self.nome
      
    def getFlagCor(self):
        return self.flagCor
    
    def getTurno(self):
        return self.turno
      
    def setNome(self, nome):
        self.nome = nome

    def setFlagCor(self, flagCor):
        self.flagCor = flagCor

    def setTurno(self, turno):
        self.turno = turno
# ------------------------------------------- 

    def verificaTurno(self):
        return self.turno

    