import pygame

bishop_white = pygame.image.load('./images/bishop.jpg')
king_white = pygame.image.load('./images/king.jpg')
queen_white = pygame.image.load('./images/queen.jpg')
rook_white = pygame.image.load('./images/rook.jpg')
knight_white = pygame.image.load('./images/knight.jpg')
pawn_white = pygame.image.load('./images/pawn.jpg')

bishop_black = pygame.image.load('./images/bishop_black.jpg')
king_black = pygame.image.load('./images/king_black.jpg')
queen_black = pygame.image.load('./images/queen_black.jpg')
rook_black = pygame.image.load('./images/rook_black.jpg')
knight_black = pygame.image.load('./images/knight_black.jpg')
pawn_black = pygame.image.load('./images/pawn_black.jpg')

a = []
a.append(bishop_white)
a.append(king_white)
a.append(queen_white)
a.append(rook_white)
a.append(knight_white)
a.append(pawn_white)

b = []
b.append(bishop_black) # 0
b.append(king_black) # 1
b.append(queen_black) # 2
b.append(rook_black) # 3
b.append(knight_black) # 4
b.append(pawn_black) # 5


A = []
B = []

WIDTH = 1100
HEIGHT = 900

for i in range(6):
    A.append(pygame.transform.scale(a[i], (int(WIDTH/8), int(HEIGHT/8))))

for i in range(6):
    B.append(pygame.transform.scale(b[i], (int(WIDTH/8), int(HEIGHT/8))))


class pieces:
    def __init__(self, row, column, color):
        self.row = row
        self.column = column
        self.color = color
        self.selected = False
        self.drawimage = None
        self.width = int(1100/8)
        self.height = int(900/8)

    def move(self):
        pass

    def draw(self, screen):
        if self.color == 'w':
            self.drawimage = A[self.image]
        else:
            self.drawimage = B[self.image]

        screen.blit(self.drawimage, (self.column * self.width, self.row * self.height))
        if self.selected:
            pygame.draw.rect(screen, 'red', (self.column * self.width, self.row * self.height, self.width, self.height), 1)

    def de_select(self):
        self.selected = False

    def select(self):
        self.selected = True

class King(pieces):
    image = 1


class Bishop(pieces):
    image = 0


class Queen(pieces):
    image = 2


class Knight(pieces):
    image = 4


class Rook(pieces):
    image = 3


class Pawn(pieces):
    image = 5

