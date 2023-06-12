import pygame
from Pieces import Pawn
from Pieces import Bishop
from Pieces import King
from Pieces import Queen
from Pieces import Rook
from Pieces import Knight


class Board:

    def __init__(self, rows, columns):
        self.rows = rows
        self.columns = columns
        self.board = [[0 for x in range(8)] for _ in range(self.rows)]
        self.temp_var = self.board[0][0]
        self.status = False
        self.check_pawn = Pawn(0, 0, 'b')


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

        self.board[5][4] = Queen(5, 4, 'b')

        self.board[7][0] = Rook(7, 0, 'w')
        self.board[7][1] = Knight(7, 1, 'w')
        self.board[7][2] = Bishop(7, 2, 'w')
        self.board[7][4] = Queen(7, 4, 'w')
        self.board[7][3] = King(7, 3, 'w')
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

        # if self.board[k][l] != 0:
        #     if self.board[k][l].selected:
        #         self.board[k][l].selected = False
        #     else:
        #         self.board[k][l].selected = True

        if self.board[k][l] != 0:
            if self.check_selected(k, l):
                self.board[k][l].selected = False
            else:
                self.board[k][l].selected = True

    def move(self, init_row, init_col):
        pass



    def check_selected(self, i, j):
        if self.board[i][j] != 0:
            if self.board[i][j].selected:
                return True
            else:
                return False

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



    def move_piece(self, oi, oj, ni, nj):
        self.board[ni][nj] = self.board[oi][oj]
        self.board[oi][oj].move(ni, nj)
        if type(self.board[oi][oj]) == type(self.check_pawn):
            self.board[oi][oj].times_moved = 1
        self.board[oi][oj] = 0

    def return_valid(self, i, j):
        return self.board[i][j].return_valid_moves(self.board)