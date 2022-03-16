from xmlrpc.client import boolean


class Jogador:

    def __init__(self, nome, cor=int, turno=boolean):
        self.nome = nome
        self.cor = cor
        self.turno = turno

    # --------- Getters e Setters --------------
    def getNome(self):
        return self.nome
      
    def getCor(self):
        return self.cor
    
    def getTurno(self):
        return self.turno
      
    def setNome(self, nome):
        self.nome = nome

    def setCor(self, cor):
        self.cor = cor

    def setTurno(self, turno):
        self.turno = turno
# ------------------------------------------- 


    def verificaTurno(self):
        return self.turno

    def identificaJogador(self):
        pass

    def notificaJogador(self):
        pass

    