class Peca:

    def __init__(self, cor, coord):
        self.cor = cor
        self.coord = coord

        # radius of a drawn piece on the board
        self.radius = 40

# --------- Getters e Setters --------------  
    def getCoord(self):
        return self.coord

    def getCor(self):
        return self.cor

    def setCoord(self, coord):
        self.coord = coord

    def __str__(self):
        return str(self.cor) + ' ' + str(self.coord)