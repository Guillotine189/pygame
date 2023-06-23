import sys
from board import Board
import pygame
from Pieces import Pawn
from Pieces import King
from Pieces import Rook
from Pieces import Bishop
from Pieces import Knight
from client import Network


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

# INITIALIZING IMAGES
board_image = pygame.image.load('./images/board5.png')
board_image = pygame.transform.scale(board_image, (WIDTH, HEIGHT))
starting_screen_image = pygame.transform.scale(pygame.image.load('./images/starting_screen.png'), (1100, 650))

# CLOCK
clock = pygame.time.Clock()

# VARIABLES ONLY FOR COMPARISON
check_list = []
check_tup = ()

# ADD SOUNDS
check_sound = pygame.mixer.Sound('./sounds/move-check.mp3')
promote_sound = pygame.mixer.Sound('./sounds/promote.mp3')
notify_sound = pygame.mixer.Sound('./sounds/notify.mp3')
capture_sound = pygame.mixer.Sound('./sounds/capture.mp3')

class Button:
    def __init__(self, text, x, y, w, h):
        self.text = text
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def draw(self):
        button_text = font_.render(self.text, True, 'black')
        button_rect = pygame.rect.Rect((self.x, self.y), (self.w, self.h))
        if self.check_hover():
            pygame.draw.rect(screen, (255, 255, 255), button_rect, 0, 5)
        else:
            pygame.draw.rect(screen, 'grey', button_rect, 0, 5)

        screen.blit(button_text, (self.x + 15, self.y))

    def check_click(self):
        left_button = pygame.mouse.get_pressed()[0]
        button_rect = pygame.rect.Rect((self.x, self.y), (self.w, self.h))
        mouse_pos = pygame.mouse.get_pos()
        if left_button and button_rect.collidepoint(mouse_pos):
            return 1
        else:
            return 0

    def check_hover(self):
        mouse_pos = pygame.mouse.get_pos()
        button_rect = pygame.rect.Rect((self.x, self.y), (self.w, self.h))
        if button_rect.collidepoint(mouse_pos):
            return 1
        else:
            return 0


# THIS TAKES THE POSITION I AND J AND CHECK IF THAT POSITION HAS A PIECE SAME AS THE CURRENT PLAYER COLOR
def check_current_player_by_color(bo, i, j, current_player_color):
    if bo.board[i][j] != 0:
        if bo.board[i][j].my_color() == current_player_color:
            return True
        else:
            return False


# GENERIC FUNCTION TO THAT CHECKS IF AN ELEMENT IS IN AN ARRAY OR NOT

def check_element_in_arr(element, arr):
    # print(arr)
    for i in arr:
        # print(i, element)
        if type(i) == type(check_tup):
            # THIS IS A TUPLE
            if element == i:
                return True
        elif type(i) == type(check_list) and len(i) > 0:
            # THE TUPLES ARE IN A LIST
            for j in i:
                # print(j, element)
                if element == j:
                    return True
        else:
            # ZERO LENGTH LIST
            pass

    return False


# THIS FUNCTION RETURN THE X AND Y COORDINATE FOR THE BOARD
def click(mpos):
    y_co = int(mpos[0]/(WIDTH/8))
    x_co = int(mpos[1]/(HEIGHT/8))
    return x_co, y_co


def loosing_screen(text):
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


def starting_screen():
    pygame.display.set_caption('STARTING SCREEN')

    online_button = Button("ONLINE", 150, 400, 270, 70)
    offline_button = Button("OFFLINE", 640, 400, 320, 70)

    while True:
        screen.fill((0, 0, 0))
        screen.blit(starting_screen_image, (0, 125))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if offline_button.check_click():
                    offline_game()
                if online_button.check_click():
                    waiting_screen()

            online_button.draw()
            offline_button.draw()
            pygame.display.update()


def waiting_screen():
    print("WAITING screen")
    pygame.display.set_caption('WAITING SCREEN')
    # CREATING PLAYER OBJECT P1
    Player = Network()
    print(Player.first_message)

    if not Player.first_message:
        starting_screen()
    my_color = Player.send('init')

    pygame.display.set_caption('WAITING..')
    menu_button = Button('MAIN MENU', 320, 420, 400, 70)
    text = font_.render('WAITING FOR PLAYER..', True, (255, 255, 255)).convert_alpha()

    while True:

        # ASK FOR P2 CONNECTION STATUS
        status = Player.send('con_stat')

        screen.fill('black')
        screen.blit(starting_screen_image, (0, 125))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Player.client.send("!D".encode(Player.format))
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if menu_button.check_click():
                    Player.client.send("!D".encode(Player.format))
                    starting_screen()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    Player.client.send("!D".encode(Player.format))
                    starting_screen()

        # IF P2 STATUS = 1
        if int(status):
            online_game(Player, my_color)

        # DRAWING BUTTON, TEXT
        screen.blit(text, (140, 200))
        menu_button.draw()
        pygame.display.update()
        clock.tick(60)


def read_moves(moves):
    moves_ = moves.split(" ")
    return int(moves_[0]), int(moves_[1]), int(moves_[2]), int(moves_[3])

def make_moves(tup):
    return str(tup[0]) + " " + str(tup[1]) + " " + str(tup[2]) + " " + str(tup[3])



def read_board(board):
    return_element = []
    board_new = board.split(" ")
    print(board_new)
    for i in range(64):
        return_element += board_new[i]
    return return_element



def online_game(Player, my_color):
    pygame.display.set_caption('CHESS ONLINE')

    if my_color == 'w':
        bo = Board(8, 8, screen, 'w')
    else:
        bo = Board(8, 8, screen, 'b')

    move = 0
    start_row = 0
    start_col = 0
    current_player_color = 'w'

    while True:
        mpos = pygame.mouse.get_pos()
        screen.fill((0, 0, 0))
        screen.blit(board_image, (0, 0))
        bo.draw(screen)

        pl_2_stat = Player.send('con_stat')
        if int(pl_2_stat):

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    Player.client.send("!D".encode(Player.format))
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if move == 0:
                        current_player_color = Player.send('current_player')
                        print(current_player_color)

                    #  MY TURN CONFIRMED
                    if current_player_color == my_color:
                        i, j = click(mpos)

                        if move == 0 and bo.board[i][j] != 0 and bo.board[i][j].color == current_player_color:
                            bo.selected(i, j)
                            start_row = i
                            start_col = j

                        if bo.check_any_selected() and move == 0:
                            move += 1

                        # IF THE NEW POSITION SELECTED IS THE ORIGINAL POSITION
                        elif (i, j) == (start_row, start_col):
                            move = 0
                            bo.deselect_all()

                        # IF PLAYER SELECTED ANOTHER PIECE
                        elif move == 1 and (bo.board[i][j] != 0 and bo.board[i][j].color == current_player_color):
                            bo.selected(i, j)
                            start_row = i
                            start_col = j

                        # WHEN 2ND TIME MOUSE IS PRESSED
                        elif bo.check_any_selected() and move == 1:
                            valid_moves = bo.return_valid(start_row, start_col, True)

                            if check_element_in_arr((i, j), valid_moves):
                                payload = start_row, start_col, i, j
                                payload = make_moves(payload)
                                move = 0
                                # NOW THE NEW POSITION COMES INSIDE THE POSSIBLE MOVES
                                # SEND THIS TO SERVER TO FIND IF ITS VALID OR NOT
                                garbage = Player.send('MOVED')
                                piece_was_not_able_to_move = Player.send(payload)

                                if int(piece_was_not_able_to_move):
                                    check_sound.play()
                                else:
                                    move_sound.play()
                                    commands = Player.send('new_board')
                                    # print(exec(new_board))
                                    commands = commands.split(' ')
                                    for command in commands:
                                        print(command)
                                        exec(command)
                                    bo.deselect_all()



                        else:
                            #
                            check_sound.play()
                            bo.deselect_all()
                            move = 0

                    else:
                        # IF NOT MY CHANCE
                        move = 0
                        check_sound.play()
                        bo.deselect_all()


            pygame.display.update()


        else:
            # P2 NOT ONLONE
            Player.client.send('!D'.encode(Player.format))
            disconnect_screen()


def disconnect_screen():
    text = font_.render('OTHER PLAYER DISCONNECTED', True, (255, 255, 255)).convert_alpha()

    # CREATING BUTTON
    menu_button = Button('MAIN MENU', 320, 420, 400, 70)

    while True:
        screen.fill((0, 0, 0))
        screen.blit(starting_screen_image, (0, 95))
        screen.blit(text, (25, 250))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if menu_button.check_click():
                starting_screen()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    starting_screen()

        menu_button.draw()
        pygame.display.update()



def offline_game():

    pygame.display.set_caption('OFFLINE CHESS')

    # MAKING A BOARD
    bo = Board(8, 8, screen, 'w')
    total_moves = 0

    # INITIALIZING GAME VARIABLES
    move = 0
    start_row = 0
    start_col = 0

    # SETTING CURRENT PLAYER COLOR
    current_player_color = 'w'

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
                    starting_screen()
            if event.type == pygame.MOUSEBUTTONDOWN:

                # GET THE ROW AND COLUMN OF THE CLICKED POSITION
                i, j = click(mpos)

                # MOVE IS ZERO WHEN NO PIECE IS SELECTED
                if move == 0 and check_current_player_by_color(bo, i, j, current_player_color):
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

                    # TODO  check if this does anything (bo.board[i][j] == 0 or bo.board[i][j].color != bo.board[start_row][start_col].color)
                    # CHECK IF THE NEW POSITION SELECTED IS EMPTY(ZERO), OR HAS A DIFFERENT COLOR PIECE
                    # THEN CHECK WEATHER THAT NEW POSITION IS IN THE VALID MOVES LIST

                    if check_element_in_arr((i, j), valid_moves):
                        move = 0
                        # THIS FUNCTIONS TAKES THE OLD AND NEW POSITION
                        # CHECKS WEATHER IT CAN MOVE THE PIECE TO THE NEW POSITION OR NOT
                        piece_was_not_able_to_move, online_garbage = bo.move_piece(start_row, start_col, i, j, current_player_color)
                        # WEATHER THE PIECE WAS MOVED OR NOT DESELECT EVERYTHING
                        bo.deselect_all()

                        if piece_was_not_able_to_move:
                            check_sound.play()
                            pass
                        else:
                            move_sound.play()
                            total_moves += 1

                            # CHANGE THE EN_PASSANT STATUS OF ALL PAWN OF SAME COLOR TO BE FALSE
                            for ti in range(8):
                                for tj in range(8):
                                    if bo.board[ti][tj] != 0 and isinstance(bo.board[ti][tj], Pawn) and bo.board[ti][tj].color == current_player_color:
                                        if bo.board[ti][tj].en_passant_left_status or bo.board[ti][tj].en_passant_right_status:
                                            bo.board[ti][tj].en_passant_left_status = False
                                            bo.board[ti][tj].en_passant_right_status = False

                            # TURNING EN_PASSANT STATUS OF ENEMY PAWN TRUE
                            if isinstance(bo.board[i][j], Pawn) and abs(start_row - i) == 2:
                                # FOR ENEMY PAWN ON LEFT
                                if j > 0:
                                    if bo.board[i][j-1] != 0 and isinstance(bo.board[i][j-1], Pawn) and bo.board[i][j-1].color != current_player_color:
                                        bo.board[i][j - 1].en_passant_right_status = True

                                # FOR ENEMY PAWN ON RIGHT
                                if j < 7:
                                    if bo.board[i][j+1] != 0 and isinstance(bo.board[i][j+1], Pawn) and bo.board[i][j+1].color != current_player_color:
                                        bo.board[i][j + 1].en_passant_left_status = True


                            # CHANGE THE CURRENT PLAYER COLOR
                            if current_player_color == 'w':
                                current_player_color = 'b'
                            else:
                                current_player_color = 'w'

                            # AFTER THE PIECE HAS MOVED, CHECK IF THE PIECE WAS PAWN, ROOK OR KING
                            # AND CHANGE THE VARIABLE THAT CHANGES THE VALID MOVES FOR THEM
                            if isinstance(bo.board[i][j], Pawn):
                                bo.board[i][j].moves = 1

                            if isinstance(bo.board[i][j], King):
                                bo.board[i][j].moves = 1

                            if isinstance(bo.board[i][j], Rook):
                                bo.board[i][j].moves = 1

                            # CHECK FOR TIE
                            if total_moves >= 100:
                                screen.blit(board_image, (0, 0))
                                bo.draw(screen)
                                pygame.display.update()
                                stalemate_screen('DRAW')


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
                                stalemate_screen('DRAW')
                            if count == 61:
                                for i in range(8):
                                    for j in range(8):
                                        if bo.board[i][j] != 0 and (isinstance(bo.board[i][j], Knight) or isinstance(bo.board[i][j], Bishop)):
                                            screen.blit(board_image, (0, 0))
                                            bo.draw(screen)
                                            pygame.display.update()
                                            stalemate_screen('DRAW')

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

                    # IF THE NEW POSITION SELECTED IF THE ORIGINAL POSITION
                    elif (i, j) == (start_row, start_col):
                        move = 0
                        bo.deselect_all()

                    # IF THE NEW POSITION HAS NO PIECE BUT IS ALSO NOT IN THE VALID MOVES LIST
                    elif bo.board[i][j] == 0:
                        move = 0
                        bo.deselect_all()

                    # IF THE NEW POSITION HAS THE SAME COLOR PLAYER AS CURRENT PLAYER
                    elif bo.board[i][j] != 0 and check_current_player_by_color(bo, i, j, current_player_color):
                        bo.selected(i, j)
                        start_row = i
                        start_col = j
                else:
                    # IF NO PIECE IS SELECTED, JUST CLICKING BLANK SPOTS
                    check_sound.play()
                    move = 0

        pygame.display.update()
        clock.tick(60)


starting_screen()
