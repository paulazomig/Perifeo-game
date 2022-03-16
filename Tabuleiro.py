import pygame
import math
from Constantes import *
from Peca import *
from Hexagono import *
from Jogador import *


class Tabuleiro:
    def __init__(self):
        pygame.init()
        self.logo = pygame.image.load("images/logo.png")
        self.tabuleiro = pygame.image.load("images/tabuleiro.png")
        self.tela = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Perifero')

    # esse array tem as coordenadas do centro de cada hexagono no tabuleiro
        self.matrizCoordsHexagonos = [ [(x0, y0),      (x0+dx, y0-dy),      (x0+2*dx, y0),      (x0+3*dx, y0-dy),      (x0+4*dx, y0)],
                                     [(x0, y0+2*dy), (x0+dx, y0-dy+2*dy), (x0+2*dx, y0+2*dy), (x0+3*dx, y0-dy+2*dy), (x0+4*dx, y0+2*dy)],
                                     [(x0, y0+4*dy), (x0+dx, y0-dy+4*dy), (x0+2*dx, y0+4*dy), (x0+3*dx, y0-dy+4*dy), (x0+4*dx, y0+4*dy)],
                                     [(x0, y0+6*dy), (x0+dx, y0-dy+6*dy), (x0+2*dx, y0+6*dy), (x0+3*dx, y0-dy+6*dy), (x0+4*dx, y0+6*dy)],
                                     [(x0, y0+8*dy), (x0+dx, y0-dy+8*dy), (x0+2*dx, y0+8*dy), (x0+3*dx, y0-dy+8*dy), (x0+4*dx, y0+8*dy)] ]
        
        self.hexagonos = list()
        self.hexagonosBordaInferior = list()
        self.hexagonosBordaSuperior = list()
        self.hexagonosBordaEsquerda = list()
        self.hexagonosBordaDireita = list()

        self.pecas = list()
        self.jogadores = list()

        self.partidaEmAndamento = True

    # funcao que desenha o tabuleiro
    def desenharTabuleiro(self):
        self.tela.fill(WHITE)
        self.tela.blit(self.tabuleiro, (0, 0))

    def criarListaHexagonos(self):
        for i in range(ROWS):
            for j in range(COLS):
                hexagono = Hexagono(self.matrizCoordsHexagonos[i][j], None)
                self.hexagonos.append(hexagono)

    def criarListaHexagonosBordaSuperior(self):
        i = 0
        for j in range(ROWS):
            hexagono = Hexagono(self.matrizCoordsHexagonos[i][j], None)
            self.hexagonosBordaSuperior.append(hexagono)

    def criarListaHexagonosBordaInferior(self):
        i = 4
        for j in range(ROWS):
            hexagono = Hexagono(self.matrizCoordsHexagonos[i][j], None)
            self.hexagonosBordaInferior.append(hexagono)

    def criarListaHexagonosBordaEsquerda(self):
        j = 0 
        for i in range(ROWS):
            hexagono = Hexagono(self.matrizCoordsHexagonos[i][j], None)
            self.hexagonosBordaEsquerda.append(hexagono)

    def criarListaHexagonosBordaDireita(self):
        j = 4
        for i in range(ROWS):
            hexagono = Hexagono(self.matrizCoordsHexagonos[i][j], None)
            self.hexagonosBordaDireita.append(hexagono)

    def criarJogador(self):
        jogador1 = Jogador("AMARELO", 0, False)
        jogador2 = Jogador("PRETO", 1, True)
        self.jogadores.append(jogador1)
        self.jogadores.append(jogador2)
    
    def verificaTurnoJogador(self):
        for i in self.jogadores:
            if i.getTurno() == True:
                return i
    
    def inverterTurno(self):
        for i in self.jogadores:
            if i.getTurno():
                i.setTurno(False)
            else:
                i.setTurno(True)

    def identificaHexagono(self, coord):
        for hexagono in self.hexagonos:
            if coord == hexagono.getPosicao():
                return hexagono
        return

    # funcao que define as coordenadas da peca a ser inserida no tabuleiro apos clique do mouse
    def calculaCentroidePeca(self, mouse_coord):
        piece_coord = None
        for i in range(ROWS):
            for j in range(COLS):
                coord = self.matrizCoordsHexagonos[i][j]
                dist = math.sqrt((coord[0]-mouse_coord[0])**2 + (coord[1]-mouse_coord[1])**2)
                if dist < CLICK_RADIUS:
                    piece_coord = coord
                    break
        return piece_coord

    # AMARELO: cor 0 (== 0 --False)
    # PRETO: cor 1 (!= 0 --True)
    #criacao de pecas com alternancia de cores
    def criarPeca(self, flagCor, coord):
        if flagCor == 0:
            peca = Peca(YELLOW, coord)
        else:
            peca = Peca(BLACK, coord)
        return peca


    # caso seja um hexágono válida e que não esteja ocupado, insere peça. Caso esteja ocupada, chama self.empurrarPeca()
    def inserirPeca(self, coord):
        hexagono = self.identificaHexagono(coord)
        jogador = self.verificaTurnoJogador()
        if hexagono != None and self.verificaValidadeInserirPeca(hexagono):
            novaPeca = self.criarPeca((1 - jogador.getCor()), coord)
            if not hexagono.verificaOcupado():
                self.pecas.append(novaPeca)
                self.inverterTurno()
                hexagono.setPeca(novaPeca)
                print(self.identificaHexagono(coord).getPosicao())
            else:
                #empurrar peça
                pass
    
    def verificaValidadeInserirPeca(self, hexagono):
        for i in self.hexagonosBordaDireita:
            if i.getPosicao() == hexagono.getPosicao():
                return True
        for i in self.hexagonosBordaEsquerda:
            if i.getPosicao() == hexagono.getPosicao():
                return True
        for i in self.hexagonosBordaInferior:
            if i.getPosicao() == hexagono.getPosicao():
                return True
        for i in self.hexagonosBordaSuperior:
            if i.getPosicao() == hexagono.getPosicao():
                return True
        return False

    def iniciarSistema(self):
        logo = True
        while logo:
            self.tela.fill(WHITE)
            self.tela.blit(self.logo, (10, 100))
            pygame.display.update()
            pygame.time.wait(3000)
            logo = False
 
        self.iniciarPartida()

    def iniciarPartida(self):        
        clock = pygame.time.Clock()
        self.desenharTabuleiro()
        self.criarJogador()
        self.criarListaHexagonos()
        self.criarListaHexagonosBordaSuperior()
        self.criarListaHexagonosBordaInferior()
        self.criarListaHexagonosBordaEsquerda()
        self.criarListaHexagonosBordaDireita()       

        # Partida em andamento
        while self.partidaEmAndamento:
            clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.partidaEmAndamento = False
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_coord = pygame.mouse.get_pos()                    
                    peca_coord = self.calculaCentroidePeca(mouse_coord)
                    if peca_coord:
                        self.inserirPeca(peca_coord) 

            # desenha pecas no tabuleiro
            for p in self.pecas:            
                pygame.draw.circle(self.tela, p.cor, p.coord, p.radius)

            pygame.display.update()

        pygame.quit()


jogo = Tabuleiro()
jogo.iniciarSistema()