import sys
import pygame
from Pieces import Pawn
from Pieces import Bishop
from Pieces import King
from Pieces import Queen
from Pieces import Rook
from Pieces import Knight
# from Game import current_player_color


pygame.init()
pygame.font.init()
my_font = pygame.font.SysFont('monospace', 50)


def check_element_in_arr(element, arr):
    for i in arr:
        for k in i:
            if element == k:
                return True
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

        # self.board[1][0] = Pawn(1, 0, 'b')
        # self.board[1][1] = Pawn(1, 1, 'b')
        # self.board[1][2] = Pawn(1, 2, 'b')
        # self.board[1][3] = Pawn(1, 3, 'b')
        # self.board[1][4] = Pawn(1, 4, 'b')
        # self.board[1][5] = Pawn(1, 5, 'b')
        # self.board[1][6] = Pawn(1, 6, 'b')
        # self.board[1][7] = Pawn(1, 7, 'b')

        self.board[5][4] = King(5, 4, 'b')

        self.board[7][0] = Rook(7, 0, 'w')
        self.board[7][1] = Knight(7, 1, 'w')
        self.board[7][2] = Bishop(7, 2, 'w')
        self.board[7][4] = Queen(7, 4, 'w')
        self.board[7][3] = King(7, 3, 'w')
        self.board[7][5] = Bishop(7, 5, 'w')
        self.board[7][6] = Knight(7, 6, 'w')
        self.board[7][7] = Rook(7, 7, 'w')

        # self.board[6][0] = Pawn(6, 0, 'w')
        # self.board[6][1] = Pawn(6, 1, 'w')
        # self.board[6][2] = Pawn(6, 2, 'w')
        # self.board[6][3] = Pawn(6, 3, 'w')
        # self.board[6][4] = Pawn(6, 4, 'w')
        # self.board[6][5] = Pawn(6, 5, 'w')
        # self.board[6][6] = Pawn(6, 6, 'w')
        # self.board[6][7] = Pawn(6, 7, 'w')

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

        king_did_not_move = False

        if type(self.board[oi][oj]) == type(self.check_pawn):
            self.board[oi][oj].times_moved = 1
            self.update_old_piece = True
            self.remove_old_piece = True
            self.move_old_piece = True


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


        if color_current == 'w':
            if type(self.board[oi][oj]) == type(self.check_king) and self.board[oi][oj].color == 'w':
                king_pos = oi, oj
                danger_spots = self.king_danger_moves(king_pos[0], king_pos[1])
                if check_element_in_arr((ni, nj), danger_spots):
                    king_did_not_move = True
                    self.update_old_piece = False
                    self.remove_old_piece = False
                    self.move_old_piece = False
                 #  Return 1 so that you will not change player

        else:
            if type(self.board[oi][oj]) == type(self.check_king) and self.board[oi][oj].color == 'b':
                king_pos = oi, oj
                danger_spots = self.king_danger_moves(king_pos[0], king_pos[1])
                if check_element_in_arr((ni, nj), danger_spots):
                    king_did_not_move = True
                    self.update_old_piece = False
                    self.remove_old_piece = False
                    self.move_old_piece = False
                 #  Return 1 so that you will not change player




        print(self.remove_old_piece)
        print(self.move_old_piece)
        print(self.update_old_piece)


        if self.update_old_piece:
            self.board[oi][oj].move(ni, nj)


        if self.move_old_piece:
            self.board[ni][nj] = self.board[oi][oj]


        if self.remove_old_piece:
            self.board[oi][oj] = 0

        self.remove_old_piece = True
        self.move_old_piece = True
        self.update_old_piece = True


        return king_did_not_move


    def king_danger_moves(self, k, l):
        danger_moves = []

        for i in range(self.rows):
            for j in range(self.columns):
                if self.board[i][j] != 0:
                    if self.board[i][j].color != self.board[k][l].color:
                        danger_moves.append(self.board[i][j].return_valid_moves(self.board))

        return danger_moves



    def return_valid(self, i, j):
        return self.board[i][j].return_valid_moves(self.board)


    def change_piece(self):

        return_piece = 'Q'

        clock = pygame.time.Clock()
        rect1 = pygame.Rect(1100/4 + 10, 900/4 + 10, 1100/2 - 20, 900/8)
        rect2 = pygame.Rect(1100/4 + 10, 900/4 + 20 + 900/8, 1100/2 - 20, 900/8)
        rect3 = pygame.Rect(1100/4 + 10, 900/4 + 30 + 900/4, 1100/2 - 20, 900/8)
        rect4 = pygame.Rect(1100/4 + 10, 900/4 + 40 + 900/8 + 900/4, 1100/2 - 20, 900/8)
        text1 = my_font.render('QUEEN', True, 'white')
        text2 = my_font.render('BISHOP', True, 'white')
        text3 = my_font.render('ROOK', True, 'white')
        text4 = my_font.render('KNIGHT', True, 'white')

        while True:
            clock.tick(60)
            mpos = pygame.mouse.get_pos()

            pygame.draw.rect(self.screen, 'black', (1100/4, 900/4, 1100/2, 900/2 + 50), 0)
            pygame.draw.rect(self.screen, 'red', rect1, 0)
            pygame.draw.rect(self.screen, 'red', rect2, 0)
            pygame.draw.rect(self.screen, 'red', rect3, 0)
            pygame.draw.rect(self.screen, 'red', rect4, 0)

            self.screen.blit(text1, (1100/4 + 200, 900/4 + 50))
            self.screen.blit(text2, (1100/4 + 200, 900/4 + 60 + 900/8))
            self.screen.blit(text3, (1100/4 + 200, 900/4 + 70 + 900/4))
            self.screen.blit(text4, (1100/4 + 200, 900/4 + 80 + 900/8 + 900/4))


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