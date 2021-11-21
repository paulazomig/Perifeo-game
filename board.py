import pygame
import math

#from pygame import mouse
from constants import *
from piece import *

class Game:
    def __init__(self):
        pygame.init()
        self.bg =  pygame.image.load("images/tabuleiro.png")
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Perifero')

    #bg = pygame.image.load("images/tabuleiro.png")

    # esse array tem as coordenadas do centro de cada hexagono no tabuleiro
        self.board = [ [(x0, y0),      (x0+dx, y0-dy),      (x0+2*dx, y0),      (x0+3*dx, y0-dy),      (x0+4*dx, y0)],
                     [(x0, y0+2*dy), (x0+dx, y0-dy+2*dy), (x0+2*dx, y0+2*dy), (x0+3*dx, y0-dy+2*dy), (x0+4*dx, y0+2*dy)],
                     [(x0, y0+4*dy), (x0+dx, y0-dy+4*dy), (x0+2*dx, y0+4*dy), (x0+3*dx, y0-dy+4*dy), (x0+4*dx, y0+4*dy)],
                     [(x0, y0+6*dy), (x0+dx, y0-dy+6*dy), (x0+2*dx, y0+6*dy), (x0+3*dx, y0-dy+6*dy), (x0+4*dx, y0+6*dy)],
                     [(x0, y0+8*dy), (x0+dx, y0-dy+8*dy), (x0+2*dx, y0+8*dy), (x0+3*dx, y0-dy+8*dy), (x0+4*dx, y0+8*dy)] ]

    # matriz de controle, as casas ocupadas passam a ter valor 1
        self.board_ctrl = [ [0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0] ]

        self.pieces = list()


    # funcao que desenha o tabuleiro
    def drawBoard(self):
        self.screen.fill(WHITE)
        self.screen.blit(self.bg, (0, 0))


    # funcao que define as coordenadas da peca a ser inserida no tabuleiro apos clique do mouse
    def getPieceCoord(self, mouse_coord):
        piece_coord = None
        for i in range(ROWS):
            for j in range(COLS):
                coord = self.board[i][j]
                dist = math.sqrt((coord[0]-mouse_coord[0])**2 + (coord[1]-mouse_coord[1])**2)
                if dist < CLICK_RADIUS and self.board_ctrl[i][j] == 0:
                    piece_coord = coord
                    self.board_ctrl[i][j] = 1
                    break
        return piece_coord


    def mainLoop(self):
        run = True
        clock = pygame.time.Clock()        
        color_flag = 0

        while run:
            clock.tick(FPS)
            self.drawBoard()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_coord = pygame.mouse.get_pos()                    
                    piece_coord = self.getPieceCoord(mouse_coord)
                    
                    # criacao de pecas com alternancia de cores
                    if piece_coord:
                        if color_flag:
                            self.pieces.append(Piece(BLACK, piece_coord))
                        else:
                            self.pieces.append(Piece(YELLOW, piece_coord))
                        color_flag = (1 - color_flag)

            # desenha pecas no tabuleiro
            for p in self.pieces:            
                pygame.draw.circle(self.screen, p.color, p.coord, p.radius)

            pygame.display.update()

        pygame.quit()


jogo = Game()
jogo.mainLoop()