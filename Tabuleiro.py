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

        # setado para False quando o jogo é vencido.
        self.partidaEmAndamento = True



#--------------- MÉTODOS AUXILIARES ----------------

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
            pass
    
    def getHexagonosBordaSuperior(self):
        return self.matrizHexagonos[0]

    def getHexagonosBordaEsquerda(self):
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
        jogadorTurno = self.verificaTurnoJogador()
        novaPeca = self.criarPeca((1 - jogadorTurno.getFlagCor()), coord) # cria uma peça da cor oposta do jogador
        if not hexagono.verificaOcupado():
            hexagono.setPeca(novaPeca)
            self.inverterTurno() # seta o turno do jogador atual para False e do outro jogador para True
            return True
        return False

    # funcao que retorna hexagono que foi clicado
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

    # analista de o jogador esta tentando empurrar as peças em uma direção válida
    # unicos casos eliminados do tabuleiro são nas casas: (0,2), (4,1), (4,3)
    def analisaDirecaoValida(self, prim_hexagono, sec_hexagono):
        if prim_hexagono.getPosicao() == (0,2) or prim_hexagono.getPosicao() == (4,1) or prim_hexagono.getPosicao() == (4,3):
            if prim_hexagono.getPosicao()[1] != sec_hexagono.getPosicao()[1]:
                print('Direção inválida! Exceção da casa {}'.format(prim_hexagono.getPosicao()))
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
                else:
                    hexagono = self.matrizHexagonos[lin1-i][col1]
                
                if hexagono.verificaOcupado():
                    pecas_p_empurrar.append(hexagono.getPeca())
                    pos_p_empurrar.append(hexagono.getPosicao())
                else:
                    # precisa adicionar a próxima posição que está vazia no tabuleiro
                    # pois é pra ela que a última peça da fila será movida
                    pos_p_empurrar.append(hexagono.getPosicao())
                    break
            
            if len(pecas_p_empurrar) == ROWS:
                mixer.music.load('sounds/bad-beep-incorrect.mp3')
                mixer.music.play()
                print('Coluna {} está cheia. Não é possível adicionar peças'.format(col1))
                return False

        # existem duas exceções à essa regra: (0, 1) e (0, 3)
        # nesses casos a diagonal vai para baixo. em todas as outras casas ela vai para cima
        elif lin1 == lin2 and (col1 != 1 and col1 != 3):
            cont_hexagonos_diagonal = 0 # variável para contar quantas casas existem em uma diagonal
            r = lin1
            for j in range(COLS):
                if col1 < col2:
                    c = col1 + j

                    # nas colunas de índice ímpar é precise decrementar 1 da linha para
                    # continuar andando na diagonal para cima
                    if j % 2 == 0 and j > 0:
                        r -= 1
                    
                    if c < COLS and r >= 0:
                        hexagono = self.matrizHexagonos[r][c]
                        cont_hexagonos_diagonal += 1
                    else:
                        print('Saiu do tabuleiro andando para a direita')
                        break
                else:
                    c = col1 - j

                    # nas colunas de índice ímpar é precise decrementar 1 da linha para
                    # continuar andando na diagonal para cima
                    if j % 2 == 0 and j > 0:
                        r -= 1
                    
                    if r >= 0 and c >=0:
                        hexagono = self.matrizHexagonos[r][c]
                        cont_hexagonos_diagonal += 1
                    else:
                        print('Saiu do tabuleiro andando para a esquerda')
                        break

                if hexagono.verificaOcupado():
                    pecas_p_empurrar.append(hexagono.getPeca())
                    pos_p_empurrar.append(hexagono.getPosicao())
                else:
                    # precisa adicionar a próxima posição que está vazia no tabuleiro
                    # pois é pra ela que a última peça da fila será movida
                    pos_p_empurrar.append(hexagono.getPosicao())
                    break
            
            # transformar em um método estilo: verificaDiagonalCheia()
            # poderia criar um método contaHexagonosNaDiagonal() que roda previamente ao loop
            if len(pecas_p_empurrar) == cont_hexagonos_diagonal:
                mixer.music.load('sounds/bad-beep-incorrect.mp3')
                mixer.music.play()
                print('Diagonal p/ cima a partir de ({},{}) está cheia. Não é possível adicionar peças'.format(lin1, col1))
                return False

        elif lin1 != lin2:
            cont_hexagonos_diagonal = 0 # variável para contar quantas casas existem em uma diagonal
            r = lin1
            for j in range(COLS):
                if col1 < col2:
                    c = col1 + j

                    # nas colunas de índice ímpar é precise incrementar 1 da linha para
                    # continuar andando na diagonal para cima
                    if j % 2 == 1:
                        r += 1
                    
                    if c < COLS and r < ROWS:
                        hexagono = self.matrizHexagonos[r][c]
                        cont_hexagonos_diagonal += 1
                    else:
                        print('Saiu do tabuleiro andando para a direita')
                        break
                else:
                    c = col1 - j

                    # nas colunas de índice ímpar é precise incrementar 1 da linha para
                    # continuar andando na diagonal para cima
                    if j % 2 == 1:
                        r += 1
                    
                    if r < ROWS and c >= 0:
                        hexagono = self.matrizHexagonos[r][c]
                        cont_hexagonos_diagonal += 1
                    else:
                        print('Saiu do tabuleiro andando para a esquerda')
                        break

                if hexagono.verificaOcupado():
                    pecas_p_empurrar.append(hexagono.getPeca())
                    pos_p_empurrar.append(hexagono.getPosicao())
                else:
                    # precisa adicionar a próxima posição que está vazia no tabuleiro
                    # pois é pra ela que a última peça da fila será movida
                    pos_p_empurrar.append(hexagono.getPosicao())
                    break
            
            # transformar em um método estilo: verificaDiagonalCheia()
            # poderia criar um método contaHexagonosNaDiagonal() que roda previamente ao loop
            if len(pecas_p_empurrar) == cont_hexagonos_diagonal:
                mixer.music.load('sounds/bad-beep-incorrect.mp3')
                mixer.music.play()
                print('Diagonal p/ baixo a partir de ({},{}) está cheia. Não é possível adicionar peças'.format(lin1, col1))
                return False
            
        else:
            # printar quais situações estão entrando aqui
            # deveria ser apenas as excessões (0, 1) e (0, 3)
            print('Peça processada: ({}, {})'.format(lin1, col1))

            cont_hexagonos_diagonal = 0 # variável para contar quantas casas existem em uma diagonal
            r = lin1
            for j in range(COLS):
                if col1 < col2:
                    c = col1 + j

                    # nas colunas de índice ímpar é precise incrementar 1 da linha para
                    # continuar andando na diagonal para cima
                    if c % 2 == 1 and c != col1:
                        r += 1
                    
                    if c < COLS and r < ROWS:
                        hexagono = self.matrizHexagonos[r][c]
                        cont_hexagonos_diagonal += 1
                    else:
                        print('Saiu do tabuleiro andando para a direita')
                        break
                else:
                    c = col1 - j

                    # nas colunas de índice ímpar é precise incrementar 1 da linha para
                    # continuar andando na diagonal para cima
                    if c % 2 == 1 and c != col1:
                        r += 1
                    
                    if r < ROWS and c >= 0:
                        hexagono = self.matrizHexagonos[r][c]
                        cont_hexagonos_diagonal += 1
                    else:
                        print('Saiu do tabuleiro andando para a esquerda')
                        break

                if hexagono.verificaOcupado():
                    pecas_p_empurrar.append(hexagono.getPeca())
                    pos_p_empurrar.append(hexagono.getPosicao())
                else:
                    # precisa adicionar a próxima posição que está vazia no tabuleiro
                    # pois é pra ela que a última peça da fila será movida
                    pos_p_empurrar.append(hexagono.getPosicao())
                    break
            
            # transformar em um método estilo: verificaDiagonalCheia()
            # poderia criar um método contaHexagonosNaDiagonal() que roda previamente ao loop
            if len(pecas_p_empurrar) == cont_hexagonos_diagonal:
                print('Diagonal p/ baixo a partir de ({},{}) está cheia. Não é possível adicionar peças'.format(lin1, col1))
                mixer.music.load('sounds/bad-beep-incorrect.mp3')
                mixer.music.play()
                return False

        self.empurraPecas(pecas_p_empurrar, pos_p_empurrar)

        return True

    # funcao recebe lista de peças e de posições analisadas em analisaEmpurraPecas() e empurra naquela direção
    def empurraPecas(self, pecas, pos):
        #zera o primeiro hexagono do vetor de peças, para posteriormente receber a nova peça
        self.matrizHexagonos[pos[0][0]][pos[0][1]].setPeca(None)
        for i in range(len(pecas)):
            # pega a posição do proximo hexagono do vetor e coloca a peça do hexagono atual nele
            hexagono = self.matrizHexagonos[pos[i+1][0]][pos[i+1][1]]
            pecas[i].setCoord(hexagono.getCoord())
            hexagono.setPeca(pecas[i])


    def buscaProfundidade(self, tabuleiro, hexagono, cor):
        l, c = hexagono.getPosicao()
        if tabuleiro[l][c] == False:
            tabuleiro[l][c] = True
            for v in hexagono.getVizinhos():
                # print('{} é vizinho de ({}, {})'.format(v, l, c))
                vizinho = self.getHexagonoRef(v)
                if vizinho.verificaOcupado():
                    # print('{} está ocupado'.format(v))
                    if vizinho.getPeca().getCor() == cor:
                        # print('chamou recursao em {}'.format(vizinho.getPosicao()))
                        if vizinho.verificaBorda(cor):
                            # print('sucesso, acabou em {}'.format(vizinho.getPosicao()))
                            self.vitoria = True
                            return
                        else:
                            self.buscaProfundidade(tabuleiro, vizinho, cor)
                            if self.vitoria:
                                return

    # def buscaProfundidadeAmarelo(self, tabuleiro, hexagono):
    #     l, c = hexagono.getPosicao()
    #     if tabuleiro[l][c] == False:
    #         tabuleiro[l][c] = True
    #         for v in hexagono.getVizinhos():
    #             # print('{} é vizinho de ({}, {})'.format(v, l, c))
    #             vizinho = self.getHexagonoRef(v)
    #             if vizinho.verificaOcupado():
    #                 # print('{} está ocupado'.format(v))
    #                 if vizinho.getPeca().getCor() == YELLOW:
    #                     # print('chamou recursao em {}'.format(vizinho.getPosicao()))
    #                     if vizinho.verificaBordaInferior():
    #                         # print('sucesso, acabou em {}'.format(vizinho.getPosicao()))
    #                         self.vitoria = True
    #                         return
    #                     else:
    #                         self.buscaProfundidadeAmarelo(tabuleiro, vizinho)
    #                         if self.vitoria:
    #                             return

    # def buscaProfundidadePreto(self, tabuleiro, hexagono):
    #     l, c = hexagono.getPosicao()
    #     if tabuleiro[l][c] == False:
    #         tabuleiro[l][c] = True
    #         for v in hexagono.getVizinhos():
    #             # print('{} é vizinho de ({}, {})'.format(v, l, c))
    #             vizinho = self.getHexagonoRef(v)
    #             if vizinho.verificaOcupado():
    #                 # print('{} está ocupado'.format(v))
    #                 if vizinho.getPeca().getCor() == BLACK:
    #                     # print('chamou recursao em {}'.format(vizinho.getPosicao()))
    #                     if vizinho.verificaBordaDireita():
    #                         # print('sucesso, acabou em {}'.format(vizinho.getPosicao()))
    #                         self.vitoria = True
    #                         return
    #                     else:
    #                         self.buscaProfundidadePreto(tabuleiro, vizinho)
    #                         if self.vitoria:
    #                             return
                        
    def verificaCondicaoDeVitoria(self):

        self.vitoria = False
        for h in self.getHexagonosBordaSuperior():
            if h.verificaOcupado() and h.getPeca().getCor() == YELLOW:
                
                # inicializa matriz do tabuleiro com nenhuma casa visitada
                tabuleiro = [
                    [ False, False, False, False, False ],
                    [ False, False, False, False, False ],
                    [ False, False, False, False, False ],
                    [ False, False, False, False, False ],
                    [ False, False, False, False, False ]
                ]

                # roda busca em profundidade no grafo do jogo para tentar chegar até a outra borda
                self.vitoria = False
                self.buscaProfundidade(tabuleiro, h, YELLOW)
                    
                if self.vitoria:
                    print('AMARELO VENCEU')
                    break

        for h in self.getHexagonosBordaEsquerda():
            if h.verificaOcupado() and h.getPeca().getCor() == BLACK:

                # inicializa matriz do tabuleiro com nenhuma casa visitada
                tabuleiro = [
                    [ False, False, False, False, False ],
                    [ False, False, False, False, False ],
                    [ False, False, False, False, False ],
                    [ False, False, False, False, False ],
                    [ False, False, False, False, False ]
                ]

                # roda busca em profundidade no grafo do jogo para tentar chegar até a outra borda
                self.vitoria = False
                self.buscaProfundidade(tabuleiro, h, BLACK)
                    
                if self.vitoria:
                    print('PRETO VENCEU')
                    break

        return self.vitoria



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
                                resultado = self.verificaCondicaoDeVitoria()
                                if not sucesso:
                                    # armazena primeiro hexagono clicado e aguarda segundo click
                                    prim_hexagono = hexagono
                                else:
                                    self.tocaSom('jogadaExecutada')
                            else:
                                self.tocaSom('erro')
                        else: # segundo click no tabuleiro                            
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
                                        self.tocaSom('jogadaExecutada')
                                        resultado = self.verificaCondicaoDeVitoria()
                                else:
                                    self.tocaSom('erro')

                            prim_hexagono = None
                            sec_hexagono = None
                    else:
                        prim_hexagono = None
                        sec_hexagono = None

            # desenha pecas no tabuleiro
            for i in range(ROWS):
                for j in range(COLS):
                    p = self.matrizHexagonos[i][j].getPeca()
                    if p:    
                        pygame.draw.circle(self.tela, p.cor, p.coord, p.radius)

            pygame.display.update()

        pygame.quit()


jogo = Tabuleiro()
jogo.iniciarPartida()