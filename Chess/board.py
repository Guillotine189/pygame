import sys
import pygame
from Pieces import Pawn
from Pieces import Bishop
from Pieces import King
from Pieces import Queen
from Pieces import Rook
from Pieces import Knight

# INITIALIZE PYGAME
pygame.init()
pygame.font.init()
pygame.mixer.init()
my_font = pygame.font.SysFont('monospace', 70)

# ADD SOUNDS
check_sound = pygame.mixer.Sound('./sounds/move-check.mp3')
promote_sound = pygame.mixer.Sound('./sounds/promote.mp3')
notify_sound = pygame.mixer.Sound('./sounds/notify.mp3')
capture_sound = pygame.mixer.Sound('./sounds/capture.mp3')

# VARIABLES ONLY FOR COMPARISON
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


    def __init__(self, rows, columns, screen, color):
        self.rows = rows
        self.columns = columns
        self.board = [[0 for x in range(8)] for _ in range(self.rows)]

        self.temp_var = self.board[0][0]  # THIS STORES THE SELECTED PIECE WHILE DRAWING
        self.status = False  # FOR THE SELECTED PIECE

        self.check_pawn = Pawn(0, 0, 'b')  # ONLY FOR COMPARISON , BUT USE ISINSTANCE() MOST OF THE TIME
        self.check_king = King(0, 0, 'w')  # ONLY FOR COMPARISON
        self.screen = screen

        # THE VARIABLE THAT AFTER CHECKING ALL THE CONDITION ACTUALLY UPDATE THE BOARD
        self.remove_old_piece = True
        self.move_old_piece = True
        self.update_old_piece = True
        self.castling = False
        self.promoting = False
        self.isonline = False
        # ADDING PIECES TO THE BOARD

        if color == 'w':
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

            # self.board[2][5] = Rook(2, 5, 'b')
            # self.board[5][5] = Rook(5, 5, 'b')
            # self.board[6][6] = Rook(6, 6, 'w')
            # self.board[6][7] = King(6, 7, 'w')
            # self.board[7][4] = Rook(7, 4, 'w')

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
        else:
            self.board[0][0] = Rook(0, 0, 'w')
            self.board[0][1] = Knight(0, 1, 'w')
            self.board[0][2] = Bishop(0, 2, 'w')
            self.board[0][4] = Queen(0, 4, 'w')
            self.board[0][3] = King(0, 3, 'w')
            self.board[0][5] = Bishop(0, 5, 'w')
            self.board[0][6] = Knight(0, 6, 'w')
            self.board[0][7] = Rook(0, 7, 'w')

            self.board[1][0] = Pawn(1, 0, 'w')
            self.board[1][1] = Pawn(1, 1, 'w')
            self.board[1][2] = Pawn(1, 2, 'w')
            self.board[1][3] = Pawn(1, 3, 'w')
            self.board[1][4] = Pawn(1, 4, 'w')
            self.board[1][5] = Pawn(1, 5, 'w')
            self.board[1][6] = Pawn(1, 6, 'w')
            self.board[1][7] = Pawn(1, 7, 'w')


            self.board[7][0] = Rook(7, 0, 'b')
            self.board[7][1] = Knight(7, 1, 'b')
            self.board[7][2] = Bishop(7, 2, 'b')
            self.board[7][4] = Queen(7, 4, 'b')
            self.board[7][3] = King(7, 3, 'b')
            self.board[7][5] = Bishop(7, 5, 'b')
            self.board[7][6] = Knight(7, 6, 'b')
            self.board[7][7] = Rook(7, 7, 'b')

            self.board[6][0] = Pawn(6, 0, 'b')
            self.board[6][1] = Pawn(6, 1, 'b')
            self.board[6][2] = Pawn(6, 2, 'b')
            self.board[6][3] = Pawn(6, 3, 'b')
            self.board[6][4] = Pawn(6, 4, 'b')
            self.board[6][5] = Pawn(6, 5, 'b')
            self.board[6][6] = Pawn(6, 6, 'b')
            self.board[6][7] = Pawn(6, 7, 'b')



            # self.board[0][0] = Rook(0, 0, 'w')
            # # self.board[0][1] = Knight(0, 1, 'w')
            # # self.board[0][2] = Bishop(0, 2, 'w')
            # # self.board[0][3] = Queen(0, 3, 'w')
            # self.board[0][4] = King(0, 4, 'w')
            # self.board[0][5] = Bishop(0, 5, 'w')
            # self.board[0][6] = Knight(0, 6, 'w')
            # self.board[0][7] = Rook(0, 7, 'w')
            #
            # self.board[1][0] = Pawn(1, 0, 'w')
            # self.board[1][1] = Pawn(1, 1, 'w')
            # self.board[1][2] = Pawn(1, 2, 'w')
            # self.board[1][3] = Pawn(1, 3, 'w')
            # self.board[1][4] = Pawn(1, 4, 'w')
            # self.board[1][5] = Pawn(1, 5, 'w')
            # self.board[1][6] = Pawn(1, 6, 'w')
            # self.board[1][7] = Pawn(1, 7, 'w')
            #
            # # self.board[2][5] = Rook(2, 5, 'b')
            # # self.board[5][5] = Rook(5, 5, 'b')
            # # self.board[6][6] = Rook(6, 6, 'w')
            # # self.board[6][7] = King(6, 7, 'w')
            # # self.board[7][4] = Rook(7, 4, 'w')
            #
            # self.board[7][0] = Rook(7, 0, 'b')
            # # self.board[7][1] = Knight(7, 1, 'b')
            # # self.board[7][2] = Bishop(7, 2, 'b')
            # # self.board[7][3] = Queen(7, 3, 'b')
            # self.board[7][4] = King(7, 4, 'b')
            # self.board[7][5] = Bishop(7, 5, 'b')
            # self.board[7][6] = Knight(7, 6, 'b')
            # self.board[7][7] = Rook(7, 7, 'b')
            #
            # self.board[6][0] = Pawn(6, 0, 'b')
            # self.board[6][1] = Pawn(6, 1, 'b')
            # self.board[6][2] = Pawn(6, 2, 'b')
            # self.board[6][3] = Pawn(6, 3, 'b')
            # self.board[6][4] = Pawn(6, 4, 'b')
            # self.board[6][5] = Pawn(6, 5, 'b')
            # self.board[6][6] = Pawn(6, 6, 'b')
            # self.board[6][7] = Pawn(6, 7, 'b')







    # THIS DRAWS THE BOARD
    def draw(self, screen, online=False):
        for i in range(self.rows):
            for j in range(self.columns):
                if self.board[i][j] != 0:
                    if self.board[i][j].selected:
                        # IF A PIECE IS SELECTED DON'T DRAW IT YET
                        self.temp_var = self.board[i][j]
                        self.status = True
                    else:
                        self.board[i][j].draw(screen, self.board)

        # AFTER EVERY OTHER PIECE HAS FINISHED DRAWING, THE DRAW THE SELECTED PIECE
        if self.status:
            self.temp_var.draw(screen, self.board, online)
            self.status = False

    # THIS FUNCTIONS SELECT OR DESELECT A GIVEN PIECE
    def selected(self, k, l):
        for i in range(self.rows):
            for j in range(self.columns):
                if self.board[i][j] != 0:
                    # IF THE PIECE IS THE PIECE PASSES THROUGH, DON'T DO ANYTHING
                    if i == k and j == l:
                        pass
                    # DESELECT ALL OTHER PIECES
                    else:
                        self.board[i][j].selected = False
                        
        # IF THE PASSES PIECE IS SELECTED, DESELECT IT AND VISE-VERSA
        if self.board[k][l] != 0:
            if self.board[k][l].selected:
                self.board[k][l].selected = False
            else:
                self.board[k][l].selected = True

    # DESELECT EVERY PIECE ON BOARD
    def deselect_all(self):
        for i in range(self.rows):
            for j in range(self.columns):
                if self.board[i][j] != 0:
                    self.board[i][j].selected = False

    # RETURNS TRUE IF ANY PIECE ON BOARD IS SELECTED
    def check_any_selected(self):
        for i in range(self.rows):
            for j in range(self.columns):
                if self.board[i][j] != 0:
                    if self.board[i][j].selected:
                        return True

        return False

    # THIS FUNCTION PASSES ALL THE POSSIBLE MOVES THAT CAN BE MADE BY A PIECE
    # MADE SPECIFICALLY FOR FILE GAME.PY
    def return_valid(self, i, j, online=False):
        return self.board[i][j].return_possible_moves(self.board, online)

    # FUNCTION THAT CHECKS WEATHER A PIECE SHOULD MOVE OR NOT
    # AND THEN MOVE IT IF VALID
    # THIS FUNCITION WILL ONLY BE CALLED WHEN THE NEW POSITION FALLS UNDER 'POSSIBLE MOVES'
    def move_piece(self, oi, oj, ni, nj, color_current, online=False):

        # INITIALLY SET THAT THE PIECE WILL MOVE
        piece_was_not_able_to_move = False

        payload = ''

        # SPECIAL CASE 1 CASTLING
        if isinstance(self.board[oi][oj], King) and (nj == oj + 2 or nj == oj - 2):
            self.update_old_piece = False
            self.remove_old_piece = False
            self.move_old_piece = False

            if nj == 6:
                # FOR RIGHT ROOK IN ORIGINAL VIEW
                if self.check_valid_move(oi, oj, oi, oj + 2, color_current) and self.check_valid_move(oi, oj, oi, oj + 1, color_current):
                    self.castling = True
                    self.board[oi][oj + 2] = self.board[oi][oj]  # KING AT NEW POSITION
                    self.board[oi][oj + 1] = self.board[ni][7]  # ROOK WAS MOVED
                    self.board[oi][oj].move(oi, oj + 2)  # KING MOVED IN IMAGE
                    self.board[ni][7].move(ni, 5)  # ROOK MOVED IN IMAGE
                    self.board[ni][7] = 0  # OLD ROOK IS REMOVED
                    self.board[oi][oj] = 0  # OLD KING REMOVED
                    if online:
                        if color_current == 'b':
                            payload = f'bo.board[{7-oi}][{7-oj}].moves=1 bo.board[{7-ni}][{7-(nj+1)}].moves=1 bo.board[{7-oi}][{7-(oj+2)}]=bo.board[{7-oi}][{7-oj}] bo.board[{7-oi}][{7-(oj+1)}]=bo.board[{7-ni}][7-7] bo.board[{7-oi}][{7-oj}].move({7-oi},{7-(oj+2)}) bo.board[{7-ni}][7-7].move({7-ni},7-5)' \
                                     f' bo.board[{7-ni}][7-7]=0 bo.board[{7-oi}][{7-oj}]=0'
                        else:
                            payload = f'bo.board[{oi}][{oj}].moves=1 bo.board[{ni}][{nj+1}].moves=1 bo.board[{oi}][{oj+2}]=bo.board[{oi}][{oj}] bo.board[{oi}][{oj+1}]=bo.board[{ni}][7] bo.board[{oi}][{oj}].move({oi},{oj+2}) bo.board[{ni}][7].move({ni},5)' \
                                     f' bo.board[{ni}][7]=0 bo.board[{oi}][{oj}]=0'

                else:
                    piece_was_not_able_to_move = True

            elif nj == 2:
                # FOR LEFT ROOK IN ORIGINAL VIEW
                if self.check_valid_move(oi, oj, oi, oj - 2, color_current) and self.check_valid_move(oi, oj, oi, oj - 1, color_current):
                    self.castling = True
                    self.board[oi][oj - 2] = self.board[oi][oj]  # KING AT NEW POSITION
                    self.board[oi][oj - 1] = self.board[ni][0]  # ROOK WAS MOVED
                    self.board[oi][oj].move(oi, oj - 2)  # KING MOVED IN IMAGE
                    self.board[ni][0].move(ni, oj - 1)  # ROOK MOVED IN IMAGE
                    self.board[ni][0] = 0  # OLD ROOK IS REMOVED
                    self.board[oi][oj] = 0  # OLD KING REMOVED
                    if online:
                        if color_current == 'b':
                            payload = f'bo.board[{7-oi}][{7-oj}].moves=1 bo.board[{7-ni}][{7-(nj - 2)}].moves=1 bo.board[{7-oi}][{7-(oj - 2)}]=bo.board[{7-oi}][{7-oj}] bo.board[{7-oi}][{7-(oj - 1)}]=bo.board[{7-ni}][7] bo.board[{7-oi}][{7-oj}].move({7-oi},{7-(oj - 2)}) bo.board[{7-ni}][7-0].move({7-ni},{7-(oj - 1)}) ' \
                                       f'bo.board[{7-ni}][7-0]=0 bo.board[{7-oi}][{7-oj}]=0'
                        else:
                            payload = f'bo.board[{oi}][{oj}].moves=1 bo.board[{ni}][{nj-2}].moves=1 bo.board[{oi}][{oj-2}]=bo.board[{oi}][{oj}] bo.board[{oi}][{oj-1}]=bo.board[{ni}][0] bo.board[{oi}][{oj}].move({oi},{oj-2}) bo.board[{ni}][0].move({ni},{oj-1}) ' \
                              f'bo.board[{ni}][0]=0 bo.board[{oi}][{oj}]=0'
                else:
                    piece_was_not_able_to_move = True



        if online:
            if type(self.board[oi][oj]) == type(self.check_pawn) and not self.check(color_current):
                if self.board[oi][oj].color == 'w' and self.check_valid_move(oi, oj, ni, nj, color_current):
                    if ni == 0:
                        print("WHITE WANTS")
                        payload = 'change_piece()'
                        self.update_old_piece = False
                        self.remove_old_piece = False
                        self.move_old_piece = False
                    if ni == 7:
                        print("BLACK WANTS")
                        payload = 'change_piece()'
                        self.update_old_piece = False
                        self.remove_old_piece = False
                        self.move_old_piece = False





        else:
            # SPECIAL CASE 2 PROMOTION
            if type(self.board[oi][oj]) == type(self.check_pawn) and not self.check(color_current):
                if self.board[oi][oj].color == 'w' and self.check_valid_move(oi, oj, ni, nj, color_current):
                    if ni == 0:
                        self.promoting = True
                        # IF THE ORIGINAL POSITION HAD A WHITE PAWN
                        # AND THE NEW POSITION IS ROW 0
                        # PROMOTE THE PAWN AFTER CHECKING THAT THE KING IS NOT CHECKED
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
                        self.promoting = True
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

        # SPECIAL CASE 3 EN_PASSANT
        if isinstance(self.board[oi][oj], Pawn) and (self.board[oi][oj].en_passant_left_status or self.board[oi][oj].en_passant_right_status) and nj != oj:
            if color_current == 'w':
                self.board[ni+1][nj] = 0  # REMOVING THE PAWN THE NEW PAWN WILL TAKE
                if online:
                    if color_current == 'b':
                        payload += f'bo.board[{7-(ni + 1)}][{7-nj}]=0'
                    else:
                        payload += f'bo.board[{ni+1}][{nj}]=0'
            else:
                self.board[ni-1][nj] = 0
                if online:
                    if color_current == 'b':
                        payload += f'bo.board[{7-(ni-1)}][{7-nj}]=0'
                    else:
                        payload += f'bo.board[{ni-1}][{nj}]=0'

        # FOR EVERY OTHER CASE
        # CHECKING IF THE CURRENT MOVE WILL RESULT IN CHECK FOR CURRENT PLAYER
        if not self.castling and not self.promoting:
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

            if online:
                if color_current == 'b':
                    payload += f' bo.board[{7-oi}][{7-oj}].moves=1  bo.board[{7-oi}][{7-oj}].move({7-ni},{7-nj})'
                else:
                    payload += f' bo.board[{oi}][{oj}].moves=1  bo.board[{oi}][{oj}].move({ni},{nj})'

        if self.move_old_piece:
            # CHECK IF A PIECE WAS CAPTURED
            if self.board[ni][nj] != 0 and self.board[ni][nj].color != self.board[oi][oj].color:
                capture_sound.play()
            self.board[ni][nj] = self.board[oi][oj]

            if online:
                if color_current == 'b':
                    payload += f' bo.board[{7-ni}][{7-nj}]=bo.board[{7-oi}][{7-oj}]'
                else:
                    payload += f' bo.board[{ni}][{nj}]=bo.board[{oi}][{oj}]'

        if self.remove_old_piece:
            self.board[oi][oj] = 0

            if online:
                if color_current == 'b':
                    payload += f' bo.board[{7-oi}][{7-oj}]=0'
                else:
                    payload += f' bo.board[{oi}][{oj}]=0'



        self.remove_old_piece = True
        self.move_old_piece = True
        self.update_old_piece = True
        if self.castling:
            self.castling = False
        if self.promoting:
            self.promoting = False

        # AFTER NOT MOVING THE PIECE CHECK KING STATUS
        # IF IT IS STILL IN CHECK TURN THE CHECK_STATUS TO TRUE
        if self.check(color_current):
            position = 0, 0
            for i in range(self.rows):
                for j in range(self.columns):
                    if self.board[i][j] != 0 and self.board[i][j].color == color_current and isinstance(self.board[i][j], King):
                        position = i, j
            self.board[position[0]][position[1]].check = True

        # CHECKING FOR OTHER COLOR
        if color_current == 'w':
            if self.check('b'):
                check_sound.play()
        else:
            if self.check('w'):
                check_sound.play()



        return piece_was_not_able_to_move, online*(payload)

    # THIS TAKES IN THE OLD AND NEW COORDINATES AND THE COLOR OF CURRENT PLAYER
    # IT CHECKS WEATHER AFTER THE PIECE HAS MOVED TO A NEW POSITION
    # THE CURRENT PLAYER WILL GET CHECKED , IF YES THEN IT RETURNS FALSE, ELSE RETURNS TRUE
    def check_valid_move(self, oi, oj, ni, nj, color_current):

        # IF NEW POSITION HAS A PIECE(WHEN TAKING A PIECE)
        if self.board[ni][nj] != 0:
            piece_at_new_pos = self.board[ni][nj]  # SAVE THE PIECE PRESENT AT NEW POSITION
            self.board[ni][nj] = self.board[oi][oj]  # NEW POSITION HAS OLD PIECE
            self.board[oi][oj] = 0  # OLD PIECE HAS NO PIECE

            # NOW THE MOVE HAS TAKEN PLACE
            if self.check(color_current):
                # FINDING KINGS POSITION
                position = 0, 0
                for i in range(self.rows):
                    for j in range(self.columns):
                        if self.board[i][j] != 0 and self.board[i][j].color == color_current and isinstance(
                                self.board[i][j], King):
                            position = i, j
                            break

                # CHANGING CHECK STATUS TO FALSE BECAUSE WHEN CHECK() FUNC IN USED IT TURNS IT TRUE IF KING WAS CHECKED
                self.board[position[0]][position[1]].check = False
                self.board[oi][oj] = self.board[ni][nj]
                self.board[ni][nj] = piece_at_new_pos
                # THIS PRODUCES CHECK SO RETURN NOT A VALID MOVE
                return False

            else:
                # IF NOT TRUE THEN RETURN TRUE(VALID MOVE)
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
                        if self.board[i][j] != 0 and self.board[i][j].color == color_current and isinstance(
                                self.board[i][j], King):
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

    # THIS FUNCTION RETURNS ALL THE PLACES ON BOARD WHERE THE KING CANNOT MOVE
    # THIS TAKES KINGS COORDINATES
    def king_danger_moves(self, k, l):
        danger_moves = []

        # FOR EVERY ENEMY PIECE ON THE BOARD
        # APPEND ALL POSSIBLE MOVES THAT CAN BE DONE BY ENEMY PLAYER AT CURRENT STATE
        for i in range(self.rows):
            for j in range(self.columns):
                if self.board[i][j] != 0:
                    if self.board[i][j].color != self.board[k][l].color:

                        # ONLY CHECK THE LEFT AND RIGHT FOR PAWN BECAUSE PAWN CANNOT TAKE KING IF KING IS IN FRONT OF PAWN
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

                        # FOR EVEY OTHER ENEMY PIECE APPEND ALL THE POSSIBLE MOVES
                        else:
                            danger_moves.append(self.board[i][j].return_possible_moves(self.board))

        return danger_moves

    # THIS FUNCTIONS CHECK WEATHER THE KING OF COLOR THAT IS PASSED IS IN CHECK OR NOT
    def check(self, for_color):
        # FIND KINGS POSITION
        position = 0, 0
        for i in range(self.rows):
            for j in range(self.columns):
                if self.board[i][j] != 0 and self.board[i][j].color == for_color and isinstance(self.board[i][j], King):
                    position = i, j
                    break

        enemy_moves = self.king_danger_moves(position[0], position[1])

        # IF THE KINGS POSITION IS UNDER enemy_moves, THE KING IS IN CHECK
        if check_element_in_arr((position[0], position[1]), enemy_moves):
            self.board[position[0]][position[1]].check = True
            return True
        else:
            self.board[position[0]][position[1]].check = False
            return False

    # CHECKS FOR CHECKMATE FOR A GIVEN COLOR
    def checkmate(self, for_color):

        # FIRST CHECK IF THE PIECE OF GIVEN COLOR IS IN CHECK
        if self.check(for_color):
            # IF KING IN CHECK
            for i in range(8):
                for j in range(8):
                    if self.board[i][j] != 0:
                        if self.board[i][j].color == for_color:
                            # FOR EVERY PIECE GET ALL POSSIBLE MOVES
                            all_possible_moves_for_a_piece = self.board[i][j].return_possible_moves(self.board)
                            for move in all_possible_moves_for_a_piece:
                                # THE CASTLING ADD 0, 0 TO POSSIBLE MOVES FOR KING
                                # WHEN THIS PART READ IT GIVES ERROR, SO THIS WAS IMP
                                if type(move) == type(1):
                                    pass
                                else:
                                    if self.check_valid_move(i, j, move[0], move[1], for_color):  # TRUE FOR VALID
                                        # IF THIS IS TRUE THAT MEANS A VALID MOVE WAS FOUND SO RETURN NOT CHECKMATE
                                        return 0
                                    else:
                                        pass
            # IF FOR EVERY POSSIBLE MOVES FOR EVERY PIECE NO POSITION WAS FOUND
            # SUCH THAT A CHECK WAS NOT PRODUCED
            # BECAUSE THE KING IS ALREADY IN CHECK RETURN 1

            # TURN THE CHECK FOR KING TO BE TRUE
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

    # RETURNS TRUE IF STALEMATE
    # THIS IS CALLED AFTER CHECKMATE SO NO NEED TO SEE IF THE KING IS IN CHECK OR NOT
    def stalemate(self, for_color):
        for i in range(8):
            for j in range(8):
                if self.board[i][j] != 0:
                    if self.board[i][j].color == for_color:
                        all_possible_moves_for_a_piece = self.board[i][j].return_possible_moves(self.board)
                        for move in all_possible_moves_for_a_piece:
                            if type(move) == type(1):
                                pass
                            else:
                                if self.check_valid_move(i, j, move[0], move[1], for_color): # TRUE FOR VALID
                                    # IF THIS IS TRUE THAT MEANS A VALID MOVE WAS FOUND SO RETURN NOT STALEMATE IE 0
                                    return 0
                                else:
                                    pass

        return 1

    # WHEN THE PAWN IS PROMOTED, THIS FUNCTION IS CALLED
    # THIS RETURNS THE PIECE PLAYER WANTS TO REPLACE PAWN WITH
    def change_piece(self):
        print("SERVER")
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
            clock.tick(10)
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
    