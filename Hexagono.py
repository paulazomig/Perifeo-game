from time import sleep
from Constantes import *
from Peca import *

class Hexagono:

    def __init__(self, posicao, peca=None):
        self.posicao = posicao
        self.peca = peca

# --------- Getters e Setters --------------
    # getter
    def getPosicao(self):
        return self.posicao
      
    # getter
    def getPeca(self):
        return self.peca
      
    # setter
    def setPeca(self, peca):
        self.peca = peca
# -------------------------------------------



    def colocarPeca(self, jogador, direcao):
        pass

    def verificaOcupado(self):
        if self.peca != None:
            return True #está ocupado
        return False #não está ocupado

    def analisaEntorno(self, direcaoOrigem):
        pass

    def empurrarPecaDirecao(self, direcao):
        pass