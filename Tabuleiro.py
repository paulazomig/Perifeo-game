import pygame
import math
from Constantes import *
from Peca import *
from Hexagono import *
from Jogador import *

from pygame import mixer

mixer.init()
mixer.music.set_volume(1.0)

class Tabuleiro:
    def __init__(self):
        
        pygame.init()
        pygame.font.init()
        self.logo = pygame.image.load("images/logo.png")
        self.tabuleiro = pygame.image.load("images/tabuleiro.png")
        self.tela = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Perifero')
        
#--------------- VARIÁVEIS GLOBAIS ----------------
        # Matriz 5x5 que indexa todos os hexágonos do tabuleiro
        self.matrizHexagonos = [
            [ Hexagono((0,0), (x0, y0)), Hexagono((0,1), (x0+dx, y0-dy)), Hexagono((0,2), (x0+2*dx, y0)), Hexagono((0,3), (x0+3*dx, y0-dy)), Hexagono((0,4), (x0+4*dx, y0)) ],
            [ Hexagono((1,0), (x0, y0+2*dy)), Hexagono((1,1), (x0+dx, y0-dy+2*dy)), Hexagono((1,2), (x0+2*dx, y0+2*dy)), Hexagono((1,3), (x0+3*dx, y0-dy+2*dy)), Hexagono((1,4), (x0+4*dx, y0+2*dy)) ],
            [ Hexagono((2,0), (x0, y0+4*dy)), Hexagono((2,1), (x0+dx, y0-dy+4*dy)), Hexagono((2,2), (x0+2*dx, y0+4*dy)), Hexagono((2,3), (x0+3*dx, y0-dy+4*dy)), Hexagono((2,4), (x0+4*dx, y0+4*dy)) ],
            [ Hexagono((3,0), (x0, y0+6*dy)), Hexagono((3,1), (x0+dx, y0-dy+6*dy)), Hexagono((3,2), (x0+2*dx, y0+6*dy)), Hexagono((3,3), (x0+3*dx, y0-dy+6*dy)), Hexagono((3,4), (x0+4*dx, y0+6*dy)) ],
            [ Hexagono((4,0), (x0, y0+8*dy)), Hexagono((4,1), (x0+dx, y0-dy+8*dy)), Hexagono((4,2), (x0+2*dx, y0+8*dy)), Hexagono((4,3), (x0+3*dx, y0-dy+8*dy)), Hexagono((4,4), (x0+4*dx, y0+8*dy)) ]
        ]
        
        # Lista dos jogadores (preto ou amarelo) contendo nome, número da cor (0 = amarelo, 1 = preto) e turno
        self.jogadores = list()

        # indica o vencedor do jogo
        self.vencedor = None

        # setado para False quando o jogo é vencido.
        self.partidaEmAndamento = True

        # variáveis que armazenam o hexágono que foi clicado
        self.prim_hexagono = None
        self.sec_hexagono = None

        # variáveis que armazenam quais peças tem que ser movidas durante
        # uma inserção na borda e para qual posição
        self.pecas_p_empurrar = []
        self.pos_p_empurrar = []

#--------------- MÉTODOS AUXILIARES ----------------

#   Métodos Interface/Interação com Jogador:
    def desenharTabuleiro(self):
        self.tela.fill(WHITE)
        self.tela.blit(self.tabuleiro, (0, 0))

    def tocaSom(self, flagSom):
        if flagSom == 'jogadaExecutada':
            mixer.music.load('sounds/piece-moving.wav')
            mixer.music.play()

        elif flagSom == 'erro':
            mixer.music.load('sounds/bad-beep-incorrect.mp3')
            mixer.music.play()

        elif flagSom == 'vitoria':
            mixer.music.load('sounds/success.mp3')
            mixer.music.play()
    
    def escreveTela(self, mensagem):
        pygame.draw.rect(self.tela, WHITE, pygame.Rect(0,0, WIDTH, HEIGHT))
        myfont = pygame.font.SysFont(None, 45)
        textsurface = myfont.render(mensagem, False, (0, 0, 0))
        self.tela.blit(self.logo, (10, 100))
        self.tela.blit(textsurface,(50,300))

    def desenhaPecasTabuleiro(self):
        for i in range(ROWS):
            for j in range(COLS):
                p = self.matrizHexagonos[i][j].getPeca()
                if p:    
                    pygame.draw.circle(self.tela, p.cor, p.coord, p.radius)

#   Métodos Lógica de Jogo:    
    def getHexagonosBorda(self, borda):
        if borda == 'superior':
            return self.matrizHexagonos[0]
        else:
            return [ linha[0] for linha in self.matrizHexagonos ]

    def criarJogador(self):
        jogador1 = Jogador("AMARELO", 0, False)
        jogador2 = Jogador("PRETO", 1, True) # jogador preto começa o jogo
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

    def criarPeca(self, flagCor, coord): # criacao de pecas com alternancia de cores
        if flagCor == 0:
            peca = Peca(YELLOW, coord)
        else:
            peca = Peca(BLACK, coord)
        return peca

    # caso seja um hexágono válido e que não esteja ocupado, insere peça. Caso esteja ocupada, chama self.empurrarPeca()
    def inserirPeca(self, hexagono):
        coord = hexagono.getCoord()
        jogadorTurno = self.verificaTurnoJogador()
        novaPeca = self.criarPeca((1 - jogadorTurno.getFlagCor()), coord) # cria uma peça da cor oposta do jogador
        if not hexagono.verificaOcupado():
            hexagono.setPeca(novaPeca)
            self.inverterTurno()
            return True
        return False

    def retornaHexagonoClicado(self, mouse_coord):
        hexagonoClicado = None
        for i in range(ROWS):
            for j in range(COLS):
                hexagono = self.matrizHexagonos[i][j]
                coord = hexagono.getCoord()
                dist = math.sqrt((coord[0]-mouse_coord[0])**2 + (coord[1]-mouse_coord[1])**2)
                if dist < CLICK_RADIUS:
                    hexagonoClicado = hexagono
                    break
        return hexagonoClicado

    # retorna referência do hexágono de uma determinada posição
    def getHexagonoRef(self, pos):
        return self.matrizHexagonos[pos[0]][pos[1]]

    # analista se o jogador esta tentando empurrar as peças em uma direção válida
    # unicos casos de direcao não válida do tabuleiro são nas casas: (0,2), (4,1), (4,3)
    def analisaDirecaoValida(self):
        prim = self.prim_hexagono
        sec = self.sec_hexagono
        if prim.getPosicao() == (0,2) or prim.getPosicao() == (4,1) or prim.getPosicao() == (4,3):
            if prim.getPosicao()[1] != sec.getPosicao()[1]:
                print('Direção inválida! Exceção da casa {}'.format(prim.getPosicao()))
                return False
        if prim.getPosicao()[1] == sec.getPosicao()[1] and prim.getPosicao()[0] != 0 and prim.getPosicao()[0] != ROWS-1:
            print('Direção inválida! Exceção na casa {}'.format(prim.getPosicao()))
            return False
        return True

    def armazenaPecaParaEmpurrar(self, hexagono):
        if hexagono.verificaOcupado():
            self.pecas_p_empurrar.append(hexagono.getPeca())
            self.pos_p_empurrar.append(hexagono.getPosicao())
        else:
            # precisa adicionar a próxima posição que está vazia no tabuleiro
            # pois é pra ela que a última peça da fila será movida
            self.pos_p_empurrar.append(hexagono.getPosicao())

    def verificaDirecaoCheia(self, comprimento, tipo, direcao):
        if len(self.pecas_p_empurrar) == comprimento:
            self.tocaSom('erro')
            print('{} p/ {} está cheia. Não é possível adicionar peças'.format(tipo, direcao))
            return True

    # garante que posição está dentro dos limites do tabuleiro
    def verificaPosicao(self, r, c):
        if r >= 0 and r < ROWS and c >= 0 and c < COLS:
            return True

    # analisa se tem espaco pra empurrar (ou seja, se  nenhuma peca vai ser empurrada para fora do tabuleiro) e chama a função de empurrar
    def analisaEmpurraPecas(self):

        lin1, col1 = self.prim_hexagono.getPosicao()
        lin2, col2 = self.sec_hexagono.getPosicao()
        
        self.pecas_p_empurrar = []
        self.pos_p_empurrar = []

        # analisa se é possível adicionar peca numa coluna (vertical)
        if col1 == col2:
            for i in range(ROWS):
                if lin1 < lin2:
                    hexagono = self.matrizHexagonos[lin1+i][col1]
                else:
                    hexagono = self.matrizHexagonos[lin1-i][col1]
                
                self.armazenaPecaParaEmpurrar(hexagono)
                if not hexagono.verificaOcupado():
                    break
            
            direcao = 'Baixo' if lin2 > lin1 else 'Cima'
            if self.verificaDirecaoCheia(ROWS, 'Coluna', direcao):
                return False

        # existem duas exceções à essa regra: (0, 1) e (0, 3)
        # nesses casos a diagonal vai para baixo. em todas as outras casas ela vai para cima
        elif lin1 == lin2 and (col1 != 1 and col1 != 3):
            cont = 0 # variável para contar quantas casas existem em uma diagonal
            r = lin1
            for j in range(COLS):
                c = col1 + j if col1 < col2 else col1 - j
                if j % 2 == 0 and j > 0: # nas colunas de índice ímpar é preciso decrementar 1 da linha para
                    r -= 1               # continuar andando na diagonal para cima
                    
                if self.verificaPosicao(r, c):
                    hexagono = self.matrizHexagonos[r][c]
                    cont += 1
                else:
                    break

                self.armazenaPecaParaEmpurrar(hexagono)
                if not hexagono.verificaOcupado():
                    break
            
            if self.verificaDirecaoCheia(cont, 'Diagonal', 'Cima'):
                return False

        elif lin1 != lin2:
            cont = 0
            r = lin1
            for j in range(COLS):
                c = col1 + j if col1 < col2 else col1 - j
                if j % 2 == 1:
                    r += 1

                if self.verificaPosicao(r, c):
                    hexagono = self.matrizHexagonos[r][c]
                    cont += 1
                else:
                    break

                self.armazenaPecaParaEmpurrar(hexagono)
                if not hexagono.verificaOcupado():
                    break
            
            if self.verificaDirecaoCheia(cont, 'Diagonal', 'Baixo'):
                return False
            
        else: # excessões (0, 1) e (0, 3)
            cont = 0
            r = lin1
            for j in range(COLS):
                c = col1 + j if col1 < col2 else col1 - j
                if c % 2 == 1 and c != col1:
                    r += 1
                    
                if self.verificaPosicao(r, c):
                    hexagono = self.matrizHexagonos[r][c]
                    cont += 1
                else:
                    break

                self.armazenaPecaParaEmpurrar(hexagono)
                if not hexagono.verificaOcupado():
                    break
            
            if self.verificaDirecaoCheia(cont, 'Diagonal', 'Baixo'):
                return False
                
        return True

    # funcao recebe lista de peças e de posições analisadas em analisaEmpurraPecas() e empurra naquela direção
    def empurraPecas(self):
        pecas = self.pecas_p_empurrar
        pos = self.pos_p_empurrar

        #zera o primeiro hexagono do vetor de peças, para posteriormente receber a nova peça
        self.matrizHexagonos[pos[0][0]][pos[0][1]].setPeca(None)
        for i in range(len(pecas)):
            # pega a posição do proximo hexagono do vetor e coloca a peça do hexagono atual nele
            hexagono = self.matrizHexagonos[pos[i+1][0]][pos[i+1][1]]
            pecas[i].setCoord(hexagono.getCoord())
            hexagono.setPeca(pecas[i])


    def buscaProfundidade(self, tabuleiro, hexagono, cor):
        l, c = hexagono.getPosicao()
        # seta posicão na matriz de controle como ocupada
        if tabuleiro[l][c] == False:
            tabuleiro[l][c] = True
            # verifica se os hexágonos tem vizinhos e se são da cor desejada
            for v in hexagono.getVizinhos():
                vizinho = self.getHexagonoRef(v)
                if vizinho.verificaOcupado():
                    if vizinho.getPeca().getCor() == cor:
                        if vizinho.verificaBorda(cor):
                            self.vitoria = True
                            return
                        else:
                            self.buscaProfundidade(tabuleiro, vizinho, cor)
                            if self.vitoria:
                                return
                        
    
    def verificaCondicaoDeVitoria(self):
        self.vitoria = False
        testes = [ (YELLOW, 'superior'), (BLACK, 'esquerda') ]

        for cor, borda in testes:
            for h in self.getHexagonosBorda(borda):
                if h.verificaOcupado() and h.getPeca().getCor() == cor:
                    
                    # inicializa matriz de casas visitadas no tabuleiro a ser preenchida durante a busca em profundidade
                    tabuleiro = [
                        [ False, False, False, False, False ],
                        [ False, False, False, False, False ],
                        [ False, False, False, False, False ],
                        [ False, False, False, False, False ],
                        [ False, False, False, False, False ]
                    ]

                    # roda busca em profundidade no grafo do jogo para tentar chegar até a outra borda
                    self.vitoria = False
                    self.buscaProfundidade(tabuleiro, h, cor)
                        
                    if self.vitoria:
                        self.partidaEmAndamento = False
                        if cor == YELLOW:
                            self.vencedor = self.jogadores[0]
                        else:
                            self.vencedor = self.jogadores[1]
                        break

    def processaPrimeiroClique(self, hexagono):
        if hexagono.analisaBorda(): # perde o click se o hexagono clicado nao estiver na borda
            sucesso = self.inserirPeca(hexagono)   
            if not sucesso:
                self.prim_hexagono = hexagono # armazena primeiro hexagono clicado e aguarda segundo click
            else:
                self.verificaCondicaoDeVitoria()
                self.tocaSom('jogadaExecutada')
        else:
            self.tocaSom('erro')

    def processaSegundoClique(self, hexagono):
        # checar se o segundo hexagono esta na vizinhança imediata do primeiro (isto configura um segundo click válido)               
        # perde o click se o hexagono do segundo click nao for vizinho do primeiro
        if self.prim_hexagono.analisaEntorno(hexagono):
            self.sec_hexagono = hexagono
            if self.analisaDirecaoValida():
                # checar se a vertical/diagonal esta cheia p/ poder empurrar as peças
                if self.analisaEmpurraPecas():
                    self.empurraPecas()
                    self.inserirPeca(self.prim_hexagono)
                    self.tocaSom('jogadaExecutada')
                    self.verificaCondicaoDeVitoria()
            else:
                self.tocaSom('erro')
        else:
            self.tocaSom('erro')

        # limpa hexagonos clicados após processar o segundo clique
        self.prim_hexagono = None
        self.sec_hexagono = None


#--------------- MÉTODOS SISTEMA ----------------

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
                        if self.prim_hexagono == None:
                            self.processaPrimeiroClique(hexagono)
                        else:                            
                            self.processaSegundoClique(hexagono)                            
                    else:
                        self.prim_hexagono = None
                        self.sec_hexagono = None

            self.desenhaPecasTabuleiro()

            pygame.display.update()
        
        self.encerrarSistema()

    def encerrarSistema(self):
        if self.vencedor:
            self.tocaSom('vitoria')
            self.escreveTela("Jogador {} venceu o jogo!".format(self.vencedor.getNome()))
        else:
            self.escreveTela("  Jogo finalizado. Até a próxima!")
        pygame.display.update()
        pygame.time.wait(4000)
        pygame.quit()

jogo = Tabuleiro()
jogo.iniciarSistema()