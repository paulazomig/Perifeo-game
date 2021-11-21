import pygame

# screen size
WIDTH = 600
HEIGHT = 662

# frame rate
FPS = 60

# game defs
ROWS, COLS = 5, 5
NUM_HEXAGONS = ROWS * COLS

# RGB
YELLOW = (237, 231, 24)
BLUE = (0, 0, 255)
BLACK = (0,0,0)
WHITE = (255, 255, 255)

# Raio clicavel de cada casa do tabuleiro
CLICK_RADIUS = 45

# Coordenadas base do tabuleiro

# essas coordenadas foram tiradas da imagem tabuleiro.png
# x0 e y0 são o centro da primeira casa do tabuleiro (superior esquerda)
# dy é a distância do centro de um hexagono ate seu topo (h/2)
# dx é a distancia do centro de um hexagono ate o centro de um hexagono vizinho
x0 = 130
y0 = 160
dy = 49
dx = 85
