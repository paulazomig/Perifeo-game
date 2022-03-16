class Peca:

    def __init__(self, color, coord):
        self.color = color
        self.coord = coord

        # radius of a drawn piece on the board
        self.radius = 40

    def __str__(self):
        return str(self.color) + ' ' + str(self.coord)