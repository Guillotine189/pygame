import sys
from board import Board
import pygame

pygame.init()

# 139, 110 - size of block

WIDTH = 1100
HEIGHT = 900
screen = pygame.display.set_mode((WIDTH, HEIGHT))

board_image = pygame.image.load('./images/board.png')
board_image = pygame.transform.scale(board_image, (WIDTH, HEIGHT))


clock = pygame.time.Clock()

# rect = pygame.rect.Rect(0, 0, WIDTH, HEIGHT)


bo = Board(8, 8)




def click(mpos):
    y_co = int(mpos[0]/(WIDTH/8))
    x_co = int(mpos[1]/(HEIGHT/8))
    return x_co, y_co




while True:
    mpos = pygame.mouse.get_pos()
    screen.fill("black")
    screen.blit(board_image, (0, 0))

    bo.draw(screen)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            i, j = click(mpos)
            print(i, j)
            bo.selected(i, j)

    pygame.display.update()
    clock.tick(60)
