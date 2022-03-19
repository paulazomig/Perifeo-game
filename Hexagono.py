from time import sleep
from Constantes import *
from Peca import *

class Hexagono:

    def __init__(self, posicao, coordenada, peca=None):
        self.posicao = posicao   # posicao na matriz do tabuleiro
        self.coord = coordenada  # coordenada geometrica no canvas do jogo
        self.peca = peca

# --------- Getters e Setters --------------
    # getter
    def getPosicao(self):
        return self.posicao
      
    def getCoord(self):
        return self.coord

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

    def analisaBorda(self):
        if self.posicao[0] == 0 or self.posicao[0] == ROWS-1:
            return True
        if self.posicao[1] == 0 or self.posicao[1] == COLS-1:
            return True
        return False

    # recebe um hexagoono e checa se ele esta na vizinhança imediata do tabuleiro
    def analisaEntorno(self, vizinho):
        # tratamento de excessoes do tabuleiro (vizinhança de hexagono)
        a = +1 if (self.posicao[1] % 2 == 0) else -1
        
        if (vizinho.posicao[0] == self.posicao[0]) and (vizinho.posicao[1] == self.posicao[1]-1):
            return True
        if (vizinho.posicao[0] == self.posicao[0]) and (vizinho.posicao[1] == self.posicao[1]+1):
            return True
        if (vizinho.posicao[0] == self.posicao[0]-1) and (vizinho.posicao[1] == self.posicao[1]):
            return True
        if (vizinho.posicao[0] == self.posicao[0]+1) and (vizinho.posicao[1] == self.posicao[1]):
            return True
        if (vizinho.posicao[0] == self.posicao[0]+a) and (vizinho.posicao[1] == self.posicao[1]+1):
            return True
        if (vizinho.posicao[0] == self.posicao[0]+a) and (vizinho.posicao[1] == self.posicao[1]-1):
            return True
        return False

    def empurrarPecaDirecao(self, direcao):
        pass