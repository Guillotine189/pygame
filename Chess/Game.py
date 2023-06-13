import sys
from board import Board
import pygame
from Pieces import Pawn

pygame.init()
pygame.font.init()
font_ = pygame.font.SysFont('monospace', 70)

# 139, 110 - size of block
        # self.board[4][4] = King(4, 4, 'b')

WIDTH = 1100
HEIGHT = 900
screen = pygame.display.set_mode((WIDTH, HEIGHT))

board_image = pygame.image.load('./images/board2.png')
board_image = pygame.transform.scale(board_image, (WIDTH, HEIGHT))


clock = pygame.time.Clock()

# rect = pygame.rect.Rect(0, 0, WIDTH, HEIGHT)


bo = Board(8, 8, screen)

def check_current_player_by_color(bo, i, j):
    if bo.board[i][j] != 0:
        if bo.board[i][j].my_color() == current_player_color:
            return True
        else:
            return False


def check_element_in_arr(element, arr):
    for i in arr:
        if i == element:
            return True
    return False

def click(mpos):
    y_co = int(mpos[0]/(WIDTH/8))
    x_co = int(mpos[1]/(HEIGHT/8))
    return x_co, y_co



move = 0
start_row = 0
start_col = 0

current_player_color = 'w'



def loosing_screen(text):
    text = text + ' WON'
    text_ = font_.render(text, True, 'white')
    text_rect = text_.get_rect()
    back_rect = text_rect
    text_rect.center = 1100/2, 900/2

    while True:
        pygame.draw.rect(screen, 'black', back_rect, 0)
        screen.blit(text_, text_rect)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

def stalemate_screen(text):
    text_ = font_.render(text, True, 'white')
    text_rect = text_.get_rect()
    back_rect = text_rect
    text_rect.center = 1100/2, 900/2
    while True:
        pygame.draw.rect(screen, 'black', back_rect, 0)
        screen.blit(text_, text_rect)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        pygame.display.update()



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
            if move == 0 and check_current_player_by_color(bo, i, j):
                bo.selected(i, j)
                start_row = i
                start_col = j

            if bo.check_any_selected() and move == 0:
                move += 1
                print("SELECTED")
            elif bo.check_any_selected() and move == 1:
                valid_moves = bo.return_valid(start_row, start_col)

                if (bo.board[i][j] == 0 or bo.board[i][j].color != bo.board[start_row][start_col].color) and check_element_in_arr((i, j), valid_moves):
                    move = 0
                    piece_was_not_able_to_move = bo.move_piece(start_row, start_col, i, j, current_player_color)
                    bo.deselect_all()
                    if piece_was_not_able_to_move:
                        pass
                    else:
                        if current_player_color == 'w':
                            current_player_color = 'b'
                        else:
                            current_player_color = 'w'

                        if isinstance(bo.board[i][j], Pawn):
                            bo.board[i][j].times_moved = 1

                        # CHECK FOR TIE
                        count = 0
                        for i in range(8):
                            for j in range(8):
                                if bo.board[i][j] == 0:
                                    count += 1
                        # IF ONLY THE 2 KINGS ARE LEFT
                        if count == 62:
                            screen.blit(board_image, (0, 0))
                            bo.draw(screen)
                            pygame.display.update()
                            stalemate_screen('STALEMATE')

                        # CHECK FOR CHECKMATE
                        a = bo.checkmate('w')
                        b = bo.checkmate('b')

                        if a:
                            screen.blit(board_image, (0, 0))
                            bo.draw(screen)
                            pygame.display.update()
                            loosing_screen('BLACK')
                        if b:
                            screen.blit(board_image, (0, 0))
                            bo.draw(screen)
                            pygame.display.update()
                            loosing_screen('WHITE')

                        # CHECK FOR STALEMATE
                        a = bo.stalemate('w')
                        b = bo.stalemate('b')

                        if a:
                            screen.blit(board_image, (0, 0))
                            bo.draw(screen)
                            pygame.display.update()
                            stalemate_screen('STALEMATE')
                        if b:
                            screen.blit(board_image, (0, 0))
                            bo.draw(screen)
                            pygame.display.update()
                            stalemate_screen('STALEMATE')

                        # CHECK FOR NORMAL CHECK
                        bo.check('w')
                        bo.check('b')

                        print("MOVED")

                elif (i, j) == (start_row, start_col):
                    move = 0
                    bo.deselect_all()
                    print("DESELECTED")
                elif bo.board[i][j] == 0:
                    move = 0
                    bo.deselect_all()
                    print("DESELECTED")
                elif bo.board[i][j] != 0 and check_current_player_by_color(bo, i, j):
                    bo.selected(i, j)
                    start_row = i
                    start_col = j
                    print("NEW SELECTED")
            else:
                move = 0
                print("DESELECTED")


    pygame.display.update()
    clock.tick(60)

