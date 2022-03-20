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

    def verificaBorda(self, cor):
        if cor == YELLOW:
            if self.posicao[0] == ROWS-1:
                return True
            return False
        else:
            if self.posicao[1] == COLS-1:
                return True
            return False

    # def verificaBordaInferior(self):
    #     if self.posicao[0] == ROWS-1:
    #         return True
    #     return False

    # def verificaBordaDireita(self):
    #     if self.posicao[1] == COLS-1:
    #         return True
    #     return False

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

    def getVizinhos(self):
        vizinhos = []
        l, c = self.posicao

        if l+1 < ROWS:
            vizinhos.append((l+1, c))
        if l-1 >= 0:
            vizinhos.append((l-1, c))
        if c+1 < COLS:
            vizinhos.append((l, c+1))
        if c-1 >= 0:
            vizinhos.append((l, c-1))

        if c % 2 == 0: # coluna par, vizinho na diagonal inferior
            if l+1 < ROWS and c+1 < COLS:
                vizinhos.append((l+1, c+1))
            if l+1 < ROWS and c-1 >= 0:
                vizinhos.append((l+1, c-1))
        else: # coluna impar, vizinho na diagonal superior
            if l-1 >= 0 and c+1 < COLS:
                vizinhos.append((l-1, c+1))
            if l-1 >= 0 and c-1 >= 0:
                vizinhos.append((l-1, c-1))

        return vizinhos

    def empurrarPecaDirecao(self, direcao):
        pass