import sys
import pygame
from Pieces import Pawn
from Pieces import Bishop
from Pieces import King
from Pieces import Queen
from Pieces import Rook
from Pieces import Knight
from pygame import mixer
pygame.init()
pygame.font.init()
pygame.mixer.init()
my_font = pygame.font.SysFont('monospace', 70)

check_sound = pygame.mixer.Sound('./sounds/move-check.mp3')
promote_sound = pygame.mixer.Sound('./sounds/promote.mp3')
notify_sound = pygame.mixer.Sound('./sounds/notify.mp3')


check_list = []
check_tup = ()


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



class Board:

    def __init__(self, rows, columns, screen):
        self.rows = rows
        self.columns = columns
        self.board = [[0 for x in range(8)] for _ in range(self.rows)]
        self.temp_var = self.board[0][0]
        self.status = False
        self.king_status = True
        self.check_pawn = Pawn(0, 0, 'b')
        self.check_king = King(0, 0, 'w')
        self.screen = screen
        self.remove_old_piece = True
        self.move_old_piece = True
        self.update_old_piece = True

        self.board[0][0] = Rook(0, 0, 'b')
        self.board[0][1] = Knight(0, 1, 'b')
        self.board[0][2] = Bishop(0, 2, 'b')
        self.board[0][3] = Queen(0, 3, 'b')
        self.board[0][4] = King(0, 4, 'b')
        self.board[0][5] = Bishop(0, 5, 'b')
        self.board[0][6] = Knight(0, 6, 'b')
        self.board[0][7] = Rook(0, 7, 'b')

        self.board[1][0] = Pawn(1, 0, 'b')
        self.board[1][1] = Pawn(1, 1, 'b')
        self.board[1][2] = Pawn(1, 2, 'b')
        self.board[1][3] = Pawn(1, 3, 'b')
        self.board[1][4] = Pawn(1, 4, 'b')
        self.board[1][5] = Pawn(1, 5, 'b')
        self.board[1][6] = Pawn(1, 6, 'b')
        self.board[1][7] = Pawn(1, 7, 'b')

        # self.board[3][4] = King(3, 4, 'w')
        # self.board[4][4] = King(4, 4, 'b')
        # self.board[2][6] = Pawn(2, 6, 'w')
        # self.board[5][6] = Pawn(5, 6, 'b')



        self.board[7][0] = Rook(7, 0, 'w')
        self.board[7][1] = Knight(7, 1, 'w')
        self.board[7][2] = Bishop(7, 2, 'w')
        self.board[7][3] = Queen(7, 3, 'w')
        self.board[7][4] = King(7, 4, 'w')
        self.board[7][5] = Bishop(7, 5, 'w')
        self.board[7][6] = Knight(7, 6, 'w')
        self.board[7][7] = Rook(7, 7, 'w')

        self.board[6][0] = Pawn(6, 0, 'w')
        self.board[6][1] = Pawn(6, 1, 'w')
        self.board[6][2] = Pawn(6, 2, 'w')
        self.board[6][3] = Pawn(6, 3, 'w')
        self.board[6][4] = Pawn(6, 4, 'w')
        self.board[6][5] = Pawn(6, 5, 'w')
        self.board[6][6] = Pawn(6, 6, 'w')
        self.board[6][7] = Pawn(6, 7, 'w')

    def draw(self, screen):
        for i in range(self.rows):
            for j in range(self.columns):
                if self.board[i][j] != 0:
                    if self.board[i][j].selected:
                        self.temp_var = self.board[i][j]
                        self.status = True
                    else:
                        self.board[i][j].draw(screen, self.board)
        if self.status:
            self.temp_var.draw(screen, self.board)
            self.status = False

    def selected(self, k, l):
        for i in range(self.rows):
            for j in range(self.columns):
                if self.board[i][j] != 0:
                    if i == k and j == l:
                        pass
                    else:
                        self.board[i][j].selected = False

        if self.board[k][l] != 0:
            if self.board[k][l].selected:
                self.board[k][l].selected = False
            else:
                self.board[k][l].selected = True


    def deselect_all(self):
        for i in range(self.rows):
            for j in range(self.columns):
                if self.board[i][j] != 0:
                    self.board[i][j].selected = False

    def check_any_selected(self):
        for i in range(self.rows):
            for j in range(self.columns):
                if self.board[i][j] != 0:
                    if self.board[i][j].selected:
                        return True

        return False



    def move_piece(self, oi, oj, ni, nj, color_current):

        piece_was_not_able_to_move = False

        if type(self.board[oi][oj]) == type(self.check_pawn):

            if self.board[oi][oj].color == 'w':
                if ni == 0:
                    new_piece = self.change_piece()
                    if new_piece == 'Q':
                        self.board[ni][nj] = Queen(ni, nj, 'w')
                        self.board[oi][oj].has_changed = True
                    if new_piece == 'B':
                        self.board[ni][nj] = Bishop(ni, nj, 'w')
                        self.board[oi][oj].has_changed = True
                    if new_piece == 'R':
                        self.board[ni][nj] = Rook(ni, nj, 'w')
                        self.board[oi][oj].has_changed = True
                    if new_piece == 'K':
                        self.board[ni][nj] = Knight(ni, nj, 'w')
                        self.board[oi][oj].has_changed = True
                    self.update_old_piece = True
                    self.remove_old_piece = True
                    self.move_old_piece = False

            else:
                if ni == 7:
                    new_piece = self.change_piece()
                    if new_piece == 'Q':
                        self.board[ni][nj] = Queen(ni, nj, 'b')
                        self.board[oi][oj].has_changed = True
                    if new_piece == 'B':
                        self.board[ni][nj] = Bishop(ni, nj, 'b')
                        self.board[oi][oj].has_changed = True
                    if new_piece == 'R':
                        self.board[ni][nj] = Rook(ni, nj, 'b')
                        self.board[oi][oj].has_changed = True
                    if new_piece == 'K':
                        self.board[ni][nj] = Knight(ni, nj, 'b')
                        self.board[oi][oj].has_changed = True
                    self.update_old_piece = True
                    self.remove_old_piece = True
                    self.move_old_piece = False
                    promote_sound.play()

        # CHECKING IF THE CURRENT MOVE WILL RESULT IN CHECK FOR CURRENT PLAYER
        # IF NEW POSITION HAS A PIECE
        if self.board[ni][nj] != 0:
            piece_at_new_pos = self.board[ni][nj]
            self.board[ni][nj] = self.board[oi][oj]  # new position
            self.board[oi][oj] = 0

            if self.check(color_current):

                # FINDING KINGS POSITION
                position = 0, 0
                for i in range(self.rows):
                    for j in range(self.columns):
                        if self.board[i][j] != 0 and self.board[i][j].color == color_current and isinstance(
                                self.board[i][j], King):
                            position = i, j
                # CHANGING CHECK STATUS TO FALSE BECAUSE WHEN CHECK() FUNC IN USED IT TURNS IT TRUE IF KING WAS CHECKED
                self.board[position[0]][position[1]].check = False

                piece_was_not_able_to_move = True
                self.update_old_piece = False
                self.remove_old_piece = False
                self.move_old_piece = False
            else:
                pass

            self.board[oi][oj] = self.board[ni][nj]
            self.board[ni][nj] = piece_at_new_pos

            # IF NEW POSITION DOES NOT HAVE A PIECE
        else:
            self.board[ni][nj] = self.board[oi][oj]  # new position
            self.board[oi][oj] = 0

            if self.check(color_current):

                position = 0, 0
                for i in range(self.rows):
                    for j in range(self.columns):
                        if self.board[i][j] != 0 and self.board[i][j].color == color_current and isinstance(self.board[i][j], King):
                            position = i, j

                self.board[position[0]][position[1]].check = False

                piece_was_not_able_to_move = True
                self.update_old_piece = False
                self.remove_old_piece = False
                self.move_old_piece = False
            else:
                pass

            self.board[oi][oj] = self.board[ni][nj]
            self.board[ni][nj] = 0

        # FINALLY MOVING PIECES
        if self.update_old_piece:
            self.board[oi][oj].move(ni, nj)
        if self.move_old_piece:
            self.board[ni][nj] = self.board[oi][oj]
        if self.remove_old_piece:
            self.board[oi][oj] = 0

        self.remove_old_piece = True
        self.move_old_piece = True
        self.update_old_piece = True

        # AFTER CHECKING ALL THE CONDITIONS AND MOVING THE PIECE CHECK KING STATUS
        # IF IT IS STILL IN CHECK TURN THE CHECK_STATUS TO TRUE
        if self.check(color_current):
            position = 0, 0
            for i in range(self.rows):
                for j in range(self.columns):
                    if self.board[i][j] != 0 and self.board[i][j].color == color_current and isinstance(
                            self.board[i][j], King):
                        position = i, j
            self.board[position[0]][position[1]].check = True

        # CHECKING FOR OTHER COLOR
        if color_current == 'w':
            if self.check('b'):
                check_sound.play()
        else:
            if self.check('w'):
                check_sound.play()


        return piece_was_not_able_to_move


    def check_valid_moves(self, oi, oj, ni, nj, color_current):
        if self.board[ni][nj] != 0:
            piece_at_new_pos = self.board[ni][nj]
            self.board[ni][nj] = self.board[oi][oj]  # new position
            self.board[oi][oj] = 0

            if self.check(color_current):
                # FINDING KINGS POSITION
                position = 0, 0
                for i in range(self.rows):
                    for j in range(self.columns):
                        if self.board[i][j] != 0 and self.board[i][j].color == color_current and isinstance(self.board[i][j], King):
                            position = i, j
                            break
                # CHANGING CHECK STATUS TO FALSE BECAUSE WHEN CHECK() FUNC IN USED IT TURNS IT TRUE IF KING WAS CHECKED
                self.board[position[0]][position[1]].check = False
                self.board[oi][oj] = self.board[ni][nj]
                self.board[ni][nj] = piece_at_new_pos
                # THIS PRODUCES CHECK SO RETURN NOT A VALID MOVE
                return False

            else:
                self.board[oi][oj] = self.board[ni][nj]
                self.board[ni][nj] = piece_at_new_pos
                return True

            # IF NEW POSITION DOES NOT HAVE A PIECE
        else:
            self.board[ni][nj] = self.board[oi][oj]  # new position
            self.board[oi][oj] = 0

            if self.check(color_current):
                position = 0, 0
                for i in range(self.rows):
                    for j in range(self.columns):
                        if self.board[i][j] != 0 and self.board[i][j].color == color_current and isinstance(self.board[i][j], King):
                            position = i, j
                            break

                self.board[position[0]][position[1]].check = False
                self.board[oi][oj] = self.board[ni][nj]
                self.board[ni][nj] = 0
                return False
            else:
                self.board[oi][oj] = self.board[ni][nj]
                self.board[ni][nj] = 0
                return True



    def king_danger_moves(self, k, l):
        danger_moves = []

        for i in range(self.rows):
            for j in range(self.columns):
                if self.board[i][j] != 0:
                    if self.board[i][j].color != self.board[k][l].color:

                        # ONLY CHECK THE LEFT AND RIGHT FOR PAWN
                        if type(self.board[i][j]) == type(self.check_pawn):
                            if self.board[i][j].color == 'b':
                                if j < 7:
                                    danger_moves.append((i + 1, j + 1))
                                if j > 0:
                                    danger_moves.append((i + 1, j - 1))

                            else:
                                if j < 7:
                                    danger_moves.append((i - 1, j + 1))
                                if j > 0:
                                    danger_moves.append((i - 1, j - 1))

                        elif isinstance(self.board[i][j], King):
                            pass

                        else:
                            danger_moves.append(self.board[i][j].return_possible_moves(self.board))

        return danger_moves



    def return_valid(self, i, j):
        return self.board[i][j].return_possible_moves(self.board)



    def check(self, for_color):
        position = 0, 0
        for i in range(self.rows):
            for j in range(self.columns):
                if self.board[i][j] != 0 and self.board[i][j].color == for_color and isinstance(self.board[i][j], King):
                    position = i, j
                    break

        enemy_moves = self.king_danger_moves(position[0], position[1])
        if check_element_in_arr((position[0], position[1]), enemy_moves):
            self.board[position[0]][position[1]].check = True
            return True
        else:
            self.board[position[0]][position[1]].check = False
            return False

    def checkmate(self, for_color):

        if self.check(for_color):
            # IF KING IN CHECK

            for i in range(8):
                for j in range(8):
                    if self.board[i][j] != 0:
                        if self.board[i][j].color == for_color:
                            all_possible_moves_for_a_piece = self.board[i][j].return_possible_moves(self.board)
                            for move in all_possible_moves_for_a_piece:
                                if self.check_valid_moves(i, j, move[0], move[1], for_color):  # TRUE FOR VALID
                                    # IF THIS IS TRUE THAT MEANS A VALID MOVE WAS FOUND SO RETURN NOT CHECKMATE
                                    return 0
                                else:
                                    pass
            # IF FOR EVERY POSSIBLE MOVES FOR EVERY PIECE NO POSITION WAS FOUND
            # SUCH THAT A CHECK WAS NOT PRODUCED
            # BECAUSE THE KING IS ALREADY IN CHECK RETURN 1

            position = 0, 0
            for i in range(self.rows):
                for j in range(self.columns):
                    if self.board[i][j] != 0 and self.board[i][j].color == for_color and isinstance(self.board[i][j], King):
                        position = i, j
                        break
            self.board[position[0]][position[1]].check = True

            return 1
        # KING WAS NOT IN CHECK SO RETURN NOT CHECKMATE
        else:
            return 0



    def stalemate(self, for_color):

        for i in range(8):
            for j in range(8):
                if self.board[i][j] != 0:
                    if self.board[i][j].color == for_color:
                        all_possible_moves_for_a_piece = self.board[i][j].return_possible_moves(self.board)
                        for move in all_possible_moves_for_a_piece:
                            if self.check_valid_moves(i, j, move[0], move[1], for_color): # TRUE FOR VALID
                                # IF THIS IS TRUE THAT MEANS A VALID MOVE WAS FOUND SO RETUEN NOT STALEMATE IE 0
                                return 0
                            else:
                                pass
        
        return 1

    def change_piece(self):

        return_piece = 'Q'

        clock = pygame.time.Clock()
        rect1 = pygame.Rect(1100/4 + 10, 900/4 + 10, 1100/2 - 20, 900/8)
        rect2 = pygame.Rect(1100/4 + 10, 900/4 + 20 + 900/8, 1100/2 - 20, 900/8)
        rect3 = pygame.Rect(1100/4 + 10, 900/4 + 30 + 900/4, 1100/2 - 20, 900/8)
        rect4 = pygame.Rect(1100/4 + 10, 900/4 + 40 + 900/8 + 900/4, 1100/2 - 20, 900/8)
        text1 = my_font.render('QUEEN', True, 'black')
        text2 = my_font.render('BISHOP', True, 'black')
        text3 = my_font.render('ROOK', True, 'black')
        text4 = my_font.render('KNIGHT', True, 'black')
        color = (155, 250, 0)
        while True:
            clock.tick(60)
            mpos = pygame.mouse.get_pos()
            pygame.draw.rect(self.screen, 'black', (1100/4, 900/4, 1100/2, 900/2 + 50), 0)
            pygame.draw.rect(self.screen, color, rect1, 0)
            pygame.draw.rect(self.screen, color, rect2, 0)
            pygame.draw.rect(self.screen, color, rect3, 0)
            pygame.draw.rect(self.screen, color, rect4, 0)

            self.screen.blit(text1, (1100/4 + 150, 900/4 + 40))
            self.screen.blit(text2, (1100/4 + 150, 900/4 + 50 + 900/8))
            self.screen.blit(text3, (1100/4 + 150, 900/4 + 60 + 900/4))
            self.screen.blit(text4, (1100/4 + 150, 900/4 + 70 + 900/8 + 900/4))


            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            if rect1.collidepoint(mpos) and pygame.mouse.get_pressed()[0]:
                return_piece = 'Q'
                break
            if rect2.collidepoint(mpos) and pygame.mouse.get_pressed()[0]:
                return_piece = "B"
                break
            if rect3.collidepoint(mpos) and pygame.mouse.get_pressed()[0]:
                return_piece = "R"
                break
            if rect4.collidepoint(mpos) and pygame.mouse.get_pressed()[0]:
                return_piece = "K"
                break



            pygame.display.update()

        return return_piece