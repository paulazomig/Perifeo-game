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
        
        self.matrizHexagonos = [
            [ Hexagono((0,0), (x0, y0)), Hexagono((0,1), (x0+dx, y0-dy)), Hexagono((0,2), (x0+2*dx, y0)), Hexagono((0,3), (x0+3*dx, y0-dy)), Hexagono((0,4), (x0+4*dx, y0)) ],
            [ Hexagono((1,0), (x0, y0+2*dy)), Hexagono((1,1), (x0+dx, y0-dy+2*dy)), Hexagono((1,2), (x0+2*dx, y0+2*dy)), Hexagono((1,3), (x0+3*dx, y0-dy+2*dy)), Hexagono((1,4), (x0+4*dx, y0+2*dy)) ],
            [ Hexagono((2,0), (x0, y0+4*dy)), Hexagono((2,1), (x0+dx, y0-dy+4*dy)), Hexagono((2,2), (x0+2*dx, y0+4*dy)), Hexagono((2,3), (x0+3*dx, y0-dy+4*dy)), Hexagono((2,4), (x0+4*dx, y0+4*dy)) ],
            [ Hexagono((3,0), (x0, y0+6*dy)), Hexagono((3,1), (x0+dx, y0-dy+6*dy)), Hexagono((3,2), (x0+2*dx, y0+6*dy)), Hexagono((3,3), (x0+3*dx, y0-dy+6*dy)), Hexagono((3,4), (x0+4*dx, y0+6*dy)) ],
            [ Hexagono((4,0), (x0, y0+8*dy)), Hexagono((4,1), (x0+dx, y0-dy+8*dy)), Hexagono((4,2), (x0+2*dx, y0+8*dy)), Hexagono((4,3), (x0+3*dx, y0-dy+8*dy)), Hexagono((4,4), (x0+4*dx, y0+8*dy)) ]
        ]

        self.pecas = list()
        self.jogadores = list()

        self.partidaEmAndamento = True

    def getHexagonosBordaSuperior(self):
        return self.matrizHexagonos[0]

    def getHexagonosBordaInferior(self):
        return self.matrizHexagonos[-1]

    def getHexagonosBordaEsquerda(self):
        return [ linha[0] for linha in self.matrizHexagonos ]

    def getHexagonosBordaDireita(self):
        return [ linha[-1] for linha in self.matrizHexagonos ]

    # checa se a posição a inserir a peça é na borda
    def verificaValidadeInserirPeca(self, hexagono):
        for i in self.getHexagonosBordaDireita():
            if i.getPosicao() == hexagono.getPosicao():
                return True
        for i in self.getHexagonosBordaEsquerda():
            if i.getPosicao() == hexagono.getPosicao():
                return True
        for i in self.getHexagonosBordaInferior():
            if i.getPosicao() == hexagono.getPosicao():
                return True
        for i in self.getHexagonosBordaSuperior():
            if i.getPosicao() == hexagono.getPosicao():
                return True
        return False

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

    # criacao de pecas com alternancia de cores
    def criarPeca(self, flagCor, coord):
        if flagCor == 0:
            peca = Peca(YELLOW, coord)
        else:
            peca = Peca(BLACK, coord)
        return peca

    # caso seja um hexágono válida e que não esteja ocupado, insere peça. Caso esteja ocupada, chama self.empurrarPeca()
    def inserirPeca(self, hexagono):
        coord = hexagono.getCoord()
        jogador = self.verificaTurnoJogador()
        novaPeca = self.criarPeca((1 - jogador.getCor()), coord)
        if not hexagono.verificaOcupado():
            self.pecas.append(novaPeca)
            self.inverterTurno()
            hexagono.setPeca(novaPeca)
            print(hexagono.getCoord())
            return True
        return False

    # funcao que retorna hexagono que foi clicado
    def retornaHexagonoClicado(self, mouse_coord):
        click_hexagono = None
        for i in range(ROWS):
            for j in range(COLS):
                hexagono = self.matrizHexagonos[i][j]
                coord = hexagono.getCoord()
                dist = math.sqrt((coord[0]-mouse_coord[0])**2 + (coord[1]-mouse_coord[1])**2)
                if dist < CLICK_RADIUS:
                    click_hexagono = hexagono
                    break
        return click_hexagono

    # unicos casos eliminados do tabuleiro são nas casas: (0,2), (4,1), (4,3)
    def analisaDirecaoValida(self, prim_hexagono, sec_hexagono):
        if prim_hexagono.getPosicao() == (0,2) or prim_hexagono.getPosicao() == (4,1) or prim_hexagono.getPosicao() == (4,3):
            if prim_hexagono.getPosicao()[1] != sec_hexagono.getPosicao()[1]:
                print('INVALIDO!!!!')
                return False
        return True

    # analisa se tem espaco pra empurrar (ou seja, se  nrnhuma peca vai ser empurrada para fora do tabuleiro)
    # e chama a função de empurrar
    def analisaEmpurraPecas(self, prim_hexagono, sec_hexagono):
        lin1 = prim_hexagono.getPosicao()[0]
        col1 = prim_hexagono.getPosicao()[1]

        lin2 = sec_hexagono.getPosicao()[0]
        col2 = sec_hexagono.getPosicao()[1]
        
        pecas_p_empurrar = list()
        pos_p_empurrar = list()

        # analisa se é possível adicionar peca numa coluna (vertical)
        if col1 == col2:
            cont = 0
            for i in range(ROWS):
                if lin1 < lin2:
                    hexagono = self.matrizHexagonos[lin1+i][col1]
                elif lin1 > lin2:
                    hexagono = self.matrizHexagonos[lin1-i][col1]
                else:
                    print('ERROR!!!')
                    
                if hexagono.verificaOcupado():
                    pecas_p_empurrar.append(hexagono.getPeca())
                    pos_p_empurrar.append(hexagono.getPosicao())
                else:
                    pos_p_empurrar.append(hexagono.getPosicao())
                    break
            
            if len(pecas_p_empurrar) == 5:
                print('COLUNA CHEIA! NAO CONSEGUE ADICIONAR')
                return False

        self.empurraPecas(pecas_p_empurrar, pos_p_empurrar)

        return True

    def empurraPecas(self, pecas, pos):
        self.matrizHexagonos[pos[0][0]][pos[0][1]].setPeca(None)
        for i in range(len(pecas)):
            hexagono = self.matrizHexagonos[pos[i+1][0]][pos[i+1][1]]
            print(pos[i+1][0])
            print(hexagono.getPosicao())
            print(pecas[i].coord)
            pecas[i].setCoord(hexagono.getCoord())
            hexagono.setPeca(pecas[i])

    def desenharTabuleiro(self):
        self.tela.fill(WHITE)
        self.tela.blit(self.tabuleiro, (0, 0))

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

        prim_hexagono = None
        sec_hexagono = None

        # Partida em andamento
        while self.partidaEmAndamento:
            clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.partidaEmAndamento = False
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    
                    mouse_coord = pygame.mouse.get_pos()
                    hexagono = self.retornaHexagonoClicado(mouse_coord)

                    if hexagono != None:
                        if prim_hexagono == None: # primeiro click no tabuleiro
                            if hexagono.analisaBorda(): # perde o click se o hexagono clicado nao estiver na borda
                                sucesso = self.inserirPeca(hexagono)
                                if not sucesso:
                                    # armazena primeiro hexagono clicado e aguarda segundo click
                                    prim_hexagono = hexagono
                        else: # segundo click no tabuleiro

                            # se não estiver, mover as pecas até q entre a nova peca colocada
                            
                            # checar se o segundo hexagono esta na vizinhança imediata do primeiro                            
                            # isto configura um segundo click válido
                            # perde o click se o hexagono do segundo click nao for vizinho do primeiro
                            if prim_hexagono.analisaEntorno(hexagono):
                                sec_hexagono = hexagono
                                # ver se a diagonal escolhida é válida
                                if self.analisaDirecaoValida(prim_hexagono, sec_hexagono):
                                    # checar se a vertical/diagonal esta cheia p/ poder empurrar as peças
                                    if self.analisaEmpurraPecas(prim_hexagono, sec_hexagono):
                                        self.inserirPeca(prim_hexagono)

                            prim_hexagono = None
                            sec_hexagono = None
                    else:
                        prim_hexagono = None
                        sec_hexagono = None

            # desenha pecas no tabuleiro
            # for p in self.pecas:
            for i in range(ROWS):
                for j in range(COLS):
                    p = self.matrizHexagonos[i][j].getPeca()
                    if p:    
                        pygame.draw.circle(self.tela, p.cor, p.coord, p.radius)

            pygame.display.update()

        pygame.quit()


jogo = Tabuleiro()
jogo.iniciarPartida()