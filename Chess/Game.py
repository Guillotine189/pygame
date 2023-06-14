import sys
from board import Board
import pygame
from Pieces import Pawn


# LOADING PYGAME
pygame.init()
pygame.font.init()
pygame.mixer.init()
font_ = pygame.font.SysFont('monospace', 70)

# ADDING SOUNDS
move_sound = pygame.mixer.Sound('./sounds/move-self.mp3')
check_sound = pygame.mixer.Sound('./sounds/move-check.mp3')

# 139, 110 - size of block

# INITIALIZING SCREEN
WIDTH = 1100
HEIGHT = 900
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# INITIALIZING BOARD IMAGE
board_image = pygame.image.load('./images/board5.png')
board_image = pygame.transform.scale(board_image, (WIDTH, HEIGHT))

# CLOCK
clock = pygame.time.Clock()


# MAKING A BOARD
bo = Board(8, 8, screen)


# THIS TAKES THE POSITION I AND J AND CHECK IF THAT POSITION HAS A PIECE SAME AS THE CURRENT PLAYER COLOR
def check_current_player_by_color(bo, i, j):
    if bo.board[i][j] != 0:
        if bo.board[i][j].my_color() == current_player_color:
            return True
        else:
            return False


# GENERIC FUNCTION TO THAT CHECKS IF AN ELEMENT IS IN AN ARRAY OR NOT
def check_element_in_arr(element, arr):
    for i in arr:
        if i == element:
            return True
    return False


# THIS FUNCTION RETURN THE X AND Y COORDINATE FOR THE BOARD
def click(mpos):
    y_co = int(mpos[0]/(WIDTH/8))
    x_co = int(mpos[1]/(HEIGHT/8))
    return x_co, y_co


# INITIALIZING GAME VARIABLES
move = 0
start_row = 0
start_col = 0


# SETTING CURRENT PLAYER COLOR
current_player_color = 'w'


def loosing_screen(text):
    print(text, ' WON')
    text = text + ' WON'
    text_ = font_.render(text, True, 'black')
    text_rect = text_.get_rect()
    back_rect = text_rect
    text_rect.center = 1100/2, 900/2

    while True:
        pygame.draw.rect(screen, (150, 255, 0), back_rect, 0)
        pygame.draw.rect(screen, (0, 0, 0), back_rect, 2)
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
    print("STALEMATE")
    text_ = font_.render(text, True, 'black')
    text_rect = text_.get_rect()
    back_rect = text_rect
    text_rect.center = 1100/2, 900/2
    while True:
        pygame.draw.rect(screen, (100, 255, 0), back_rect, 0)
        pygame.draw.rect(screen, (0, 0, 0), back_rect, 2)
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

            # GET THE ROW AND COLUMN OF THE CLICKED POSITION
            i, j = click(mpos)

            # MOVE IS ZERO WHEN NO PIECE IS SELECTED
            if move == 0 and check_current_player_by_color(bo, i, j):
                bo.selected(i, j)
                start_row = i
                start_col = j

            if bo.check_any_selected() and move == 0:
                move += 1

            # WHEN MOVE IS 1, THAT MEANS A PIECE IS SELECTED
            # CHECK IF ANY PIECE WAS SELECTED
            # bo.selected(i, j) FUNCTIONS SELECTS A PIECE AND DESELECTS IF IT'S ALREADY SELECTED

            elif bo.check_any_selected() and move == 1:
                # GET ALL THE POSSIBLE MOVES FOR  THAT PIECE
                valid_moves = bo.return_valid(start_row, start_col)

                # CHECK IF THE NEW POSITION SELECTED IS EMPTY(ZERO), OR HAS A DIFFERENT COLOR PIECE
                # THEN CHECK WEATHER THAT NEW POSITION IS IN THE VALID MOVES LIST
                if (bo.board[i][j] == 0 or bo.board[i][j].color != bo.board[start_row][start_col].color) and check_element_in_arr((i, j), valid_moves):
                    move = 0
                    # THIS FUNCTIONS TAKES THE OLD AND NEW POSITION
                    # CHECKS WEATHER IT CAN MOVE THE PIECE TO THE NEW POSITION OR NOT
                    piece_was_not_able_to_move = bo.move_piece(start_row, start_col, i, j, current_player_color)

                    # WEATHER THE PIECE WAS MOVED OR NOT DESELECT EVERYTHING
                    bo.deselect_all()

                    if piece_was_not_able_to_move:
                        check_sound.play()
                        pass
                    else:
                        move_sound.play()

                        # CHANGE THE CURRENT PLAYER COLOR
                        if current_player_color == 'w':
                            current_player_color = 'b'
                        else:
                            current_player_color = 'w'

                        # AFTER THE PIECE HAS MOVED, CHECK IF THE PIECE WAS PAWN
                        # AND CHANGE THE VARIABLE THAT CHANGES THE VALID MOVES FOR PAWN
                        if isinstance(bo.board[i][j], Pawn):
                            bo.board[i][j].times_moved = 1

                        # CHECK FOR TIE
                        count = 0
                        for i in range(8):
                            for j in range(8):
                                if bo.board[i][j] == 0:
                                    count += 1

                        # IF ONLY THE 2 PIECES ARE LEFT, THEY ARE KINGS THEN
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

                # IF THE NEW POSITION SELECTED IF THE ORIGINAL POSITION
                elif (i, j) == (start_row, start_col):
                    move = 0
                    bo.deselect_all()

                # IF THE NEW POSITION HAS NO PIECE BUT IS ALSO NOT IN THE VALID MOVES LIST
                elif bo.board[i][j] == 0:
                    move = 0
                    bo.deselect_all()

                # IF THE NEW POSITION HAS THE SAME COLOR PLAYER AS CURRENT PLAYER
                elif bo.board[i][j] != 0 and check_current_player_by_color(bo, i, j):
                    bo.selected(i, j)
                    start_row = i
                    start_col = j
            else:
                # IF THE SELECTED IS NOT ANY OF THE ABOVE
                check_sound.play()
                move = 0

    pygame.display.update()
    clock.tick(60)
