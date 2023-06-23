import pygame

bishop_white = pygame.image.load('./images/bishop.png')
king_white = pygame.image.load('./images/king.png')
queen_white = pygame.image.load('./images/queen.png')
rook_white = pygame.image.load('./images/rook.png')
knight_white = pygame.image.load('./images/knight.png')
pawn_white = pygame.image.load('./images/pawn.png')

bishop_black = pygame.image.load('./images/bishop_black1.png')
king_black = pygame.image.load('./images/king_black1.png')
queen_black = pygame.image.load('./images/queen_black1.png')
rook_black = pygame.image.load('./images/rook_black1.png')
knight_black = pygame.image.load('./images/knight_black1.png')
pawn_black = pygame.image.load('./images/pawn_black1.png')

a = []
a.append(bishop_white)
a.append(king_white)
a.append(queen_white)
a.append(rook_white)
a.append(knight_white)
a.append(pawn_white)

b = []
b.append(bishop_black)  # 0
b.append(king_black)  # 1
b.append(queen_black)  # 2
b.append(rook_black)  # 3
b.append(knight_black)  # 4
b.append(pawn_black)  # 5

A = []
B = []

WIDTH = 1100
HEIGHT = 900

for i in range(6):
    A.append(pygame.transform.scale(a[i], (int(WIDTH / 8), int(HEIGHT / 8))))

for i in range(6):
    B.append(pygame.transform.scale(b[i], (int(WIDTH / 8), int(HEIGHT / 8))))


class pieces:
    def __init__(self, row, column, color):
        self.row = row
        self.column = column
        self.color = color
        self.selected = False
        self.drawimage = None
        self.width = int(1100 / 8)
        self.height = int(900 / 8)
        self.check = False

    def my_color(self):
        return self.color

    def possible_moves(self, board, online=False):
        pass

    def draw(self, screen, board):
        if self.color == 'w':
            self.drawimage = A[self.image]
        else:
            self.drawimage = B[self.image]

        # BLOCK THAT DENOTES CHECK
        if self.check:
            pygame.draw.rect(screen, (110, 0, 0),
                             (self.column * self.width + 1, self.row * self.height, self.width + 6, self.height + 5), 0)

        # PIECE IMAGE
        screen.blit(self.drawimage, (self.column * self.width + 2, self.row * self.height))

        # IF SELECTED DRAW THE RECTANGLE AND DOTS
        if self.selected:
            possible_moves = self.possible_moves(board)
            if len(possible_moves):
                for d in possible_moves:
                    if d != 0:
                        center = d[1] * self.width + self.width / 2, d[0] * self.height + self.height / 2
                        pygame.draw.circle(screen, (250, 150, 0), center, 15, 0)

            pygame.draw.rect(screen, (250, 150, 0),
                             (self.column * self.width + 1, self.row * self.height, self.width + 6, self.height + 5), 6)

    def move(self, new_row, new_column):
        self.row = new_row
        self.column = new_column

    def return_possible_moves(self, board, online=False):
        return self.possible_moves(board, online)


class Queen(pieces):
    image = 2
    moves = 0

    def possible_moves(self, board, online=False):
        moves = []
        i = self.row
        j = self.column

        # COPY PASE OF BOSHOP AND ROOK

        # BISHOP
        # top right
        if i > 0 and j < 7:
            ti = i
            tj = j
            while ti > 0 and tj < 7:
                p = board[ti - 1][tj + 1]
                if p == 0:
                    moves.append((ti - 1, tj + 1))
                    if ti - 1 > 0 and tj + 1 < 7:
                        if board[ti - 2][tj + 2] != 0:
                            if board[ti - 2][tj + 2].color != self.color:
                                moves.append((ti - 2, tj + 2))
                            break
                else:
                    if p.color != self.color:
                        moves.append((ti - 1, tj + 1))
                    break
                ti -= 1
                tj += 1

        # top left
        if i > 0 and j > 0:
            ti = i
            tj = j
            while ti > 0 and tj > 0:
                p = board[ti - 1][tj - 1]
                if p == 0:
                    moves.append((ti - 1, tj - 1))
                    if ti - 1 > 0 and tj - 1 > 0:
                        if board[ti - 2][tj - 2] != 0:
                            if board[ti - 2][tj - 2].color != self.color:
                                moves.append((ti - 2, tj - 2))
                            break
                else:
                    if p.color != self.color:
                        moves.append((ti - 1, tj - 1))
                    break
                ti -= 1
                tj -= 1

        # bottom right
        if i < 7 and j < 7:
            ti = i
            tj = j
            while ti < 7 and tj < 7:
                p = board[ti + 1][tj + 1]
                if p == 0:
                    moves.append((ti + 1, tj + 1))
                    if ti + 1 < 7 and tj + 1 < 7:
                        if board[ti + 2][tj + 2] != 0:
                            if board[ti + 2][tj + 2].color != self.color:
                                moves.append((ti + 2, tj + 2))
                            break
                else:
                    if p.color != self.color:
                        moves.append((ti + 1, tj + 1))
                    break
                ti += 1
                tj += 1

        # bottom left
        if i < 7 and j > 0:
            ti = i
            tj = j
            while ti < 7 and tj > 0:
                p = board[ti + 1][tj - 1]
                if p == 0:
                    moves.append((ti + 1, tj - 1))
                    if ti + 1 < 7 and tj - 1 > 0:
                        if board[ti + 2][tj - 2] != 0:
                            if board[ti + 2][tj - 2].color != self.color:
                                moves.append((ti + 2, tj - 2))
                            break
                else:
                    if p.color != self.color:
                        moves.append((ti + 1, tj - 1))
                    break
                ti += 1
                tj -= 1

        # ROOK

        # top
        if i > 0:
            # finding all the obstacle
            # arr will have positions(row) in increasing order
            arr = []
            for x in range(0, i):
                p = board[x][j]
                if p != 0:
                    arr.append(x)

            if len(arr) == 0:
                for k in range(0, i):
                    moves.append((k, j))
            else:
                first_obstacle_row = arr[len(arr) - 1]  # last element of array
                if board[first_obstacle_row][j].color != self.color:
                    moves.append((first_obstacle_row, j))
                for k in range(first_obstacle_row + 1, i):
                    moves.append((k, j))

        # Bottom
        if i < 7:
            # if while going down !=0 , then that coordinate is the first obstacle coordinate
            first_obs = 8
            for x in range(i + 1, 8):
                p = board[x][j]
                if p != 0:
                    first_obs = x
                    break

            # available spots
            for k in range(i + 1, first_obs):
                moves.append((k, j))
            if first_obs != 8:
                if board[first_obs][j].color != self.color:
                    moves.append((first_obs, j))

        # right
        if j < 7:
            first_obs = 8
            for x in range(j + 1, 8):
                p = board[i][x]
                if p != 0:
                    first_obs = x
                    break

            # available spots
            for k in range(j + 1, first_obs):
                moves.append((i, k))

            if first_obs != 8:
                if board[i][first_obs].color != self.color:
                    moves.append((i, first_obs))

        # left
        if j > 0:
            # finding all the obstacle
            # arr will have positions(row) in increasing order
            arr = []
            for x in range(0, j):
                p = board[i][x]
                if p != 0:
                    arr.append(x)

            if len(arr) == 0:
                for k in range(0, j):
                    moves.append((i, k))
            else:
                first_obstacle_column = arr[len(arr) - 1]  # last element of array
                if board[i][first_obstacle_column].color != self.color:
                    moves.append((i, first_obstacle_column))
                for k in range(first_obstacle_column + 1, j):
                    moves.append((i, k))

        return moves


class Bishop(pieces):
    image = 0
    moves = 0
    def possible_moves(self, board, online=False):
        moves = []
        i = self.row
        j = self.column

        # top right
        if i > 0 and j < 7:
            ti = i
            tj = j
            while ti > 0 and tj < 7:
                p = board[ti - 1][tj + 1]
                if p == 0:
                    moves.append((ti - 1, tj + 1))
                    if ti - 1 > 0 and tj + 1 < 7:
                        if board[ti - 2][tj + 2] != 0:
                            if board[ti - 2][tj + 2].color != self.color:
                                moves.append((ti - 2, tj + 2))
                            break
                else:
                    if p.color != self.color:
                        moves.append((ti - 1, tj + 1))
                    break
                ti -= 1
                tj += 1

        # top left
        if i > 0 and j > 0:
            ti = i
            tj = j
            while ti > 0 and tj > 0:
                p = board[ti - 1][tj - 1]
                if p == 0:
                    moves.append((ti - 1, tj - 1))
                    if ti - 1 > 0 and tj - 1 > 0:
                        if board[ti - 2][tj - 2] != 0:
                            if board[ti - 2][tj - 2].color != self.color:
                                moves.append((ti - 2, tj - 2))
                            break
                else:
                    if p.color != self.color:
                        moves.append((ti - 1, tj - 1))
                    break
                ti -= 1
                tj -= 1

        # bottom right
        if i < 7 and j < 7:
            ti = i
            tj = j
            while ti < 7 and tj < 7:
                p = board[ti + 1][tj + 1]
                if p == 0:
                    moves.append((ti + 1, tj + 1))
                    if ti + 1 < 7 and tj + 1 < 7:
                        if board[ti + 2][tj + 2] != 0:
                            if board[ti + 2][tj + 2].color != self.color:
                                moves.append((ti + 2, tj + 2))
                            break
                else:
                    if p.color != self.color:
                        moves.append((ti + 1, tj + 1))
                    break
                ti += 1
                tj += 1

        # bottom left
        if i < 7 and j > 0:
            ti = i
            tj = j
            while ti < 7 and tj > 0:
                p = board[ti + 1][tj - 1]
                if p == 0:
                    moves.append((ti + 1, tj - 1))
                    if ti + 1 < 7 and tj - 1 > 0:
                        if board[ti + 2][tj - 2] != 0:
                            if board[ti + 2][tj - 2].color != self.color:
                                moves.append((ti + 2, tj - 2))
                            break
                else:
                    if p.color != self.color:
                        moves.append((ti + 1, tj - 1))
                    break
                ti += 1
                tj -= 1

        return moves


class King(pieces):
    image = 1
    moves = 0
    check = False

    def possible_moves(self, board, online=False):
        moves = []
        i = self.row
        j = self.column

        # top left
        if i > 0 and j > 0:
            p = board[i - 1][j - 1]
            if p == 0:
                moves.append((i - 1, j - 1))
            else:
                # IF THE OTHER PLAYER IS NOT THE SAME COLOR AND NOT A KING
                if p.color != self.color:
                    moves.append((i - 1, j - 1))

        # top middle
        if i > 0:
            p = board[i - 1][j]
            if p == 0:
                moves.append((i - 1, j))
            else:
                if p.color != self.color:
                    moves.append((i - 1, j))

        # top right
        if i > 0 and j < 7:
            p = board[i - 1][j + 1]
            if p == 0:
                moves.append((i - 1, j + 1))
            else:
                if p.color != self.color:
                    moves.append((i - 1, j + 1))

        # middle right
        if j < 7:
            p = board[i][j + 1]
            if p == 0:
                moves.append((i, j + 1))
            else:
                if p.color != self.color:
                    moves.append((i, j + 1))

        # middle left
        if j > 0:
            p = board[i][j - 1]
            if p == 0:
                moves.append((i, j - 1))
            else:
                if p.color != self.color:
                    moves.append((i, j - 1))

        # bottom left
        if i < 7 and j > 0:
            p = board[i + 1][j - 1]
            if p == 0:
                moves.append((i + 1, j - 1))
            else:
                if p.color != self.color:
                    moves.append((i + 1, j - 1))

        # bottom middle
        if i < 7:
            p = board[i + 1][j]
            if p == 0:
                moves.append((i + 1, j))
            else:
                if p.color != self.color:
                    moves.append((i + 1, j))

        # bottom right
        if i < 7 and j < 7:
            p = board[i + 1][j + 1]
            if p == 0:
                moves.append((i + 1, j + 1))
            else:
                if p.color != self.color:
                    moves.append((i + 1, j + 1))

        castle_moves = self.castling(board)
        moves.append(castle_moves[0])
        moves.append(castle_moves[1])
        return moves

    def castling(self, board):
        oi = self.row
        oj = self.column
        ni = oi

        color_current = self.color
        right_castle_move = 0
        left_castle_move = 0
        if self.moves == 0 and (oi == 0 or oi == 7):
            # KING HAS ZERO MOVES
            # CHECKING OF THE POSITION BETWEEN THE KING AND ROOK FOR CHECK IS DONE IN board.py
            if not self.check:
                # FOR RIGHT ROOK
                if board[ni][7] != 0:
                    if isinstance(board[ni][7], Rook) and board[ni][7].color == color_current:
                        # THE NEW POSITION HAS ROOK OF SAME COLOR
                        if board[ni][7].moves == 0:
                            # MOVES OF ROOK ARE ZERO
                            if board[oi][oj + 1] == 0 and board[oi][oj + 2] == 0:
                                # SPACE BETWEEN THEM IS EMPTY
                                right_castle_move = (ni, 6)

                # FOR LEFT ROOK
                if board[ni][0] != 0:
                    if isinstance(board[ni][0], Rook) and board[ni][0].color == color_current:
                        # THE NEW POSITION HAS ROOK OF SAME COLOR
                        if board[ni][0].moves == 0:
                            # MOVES OF ROOK ARE ZERO
                            if board[oi][1] == 0 and board[oi][2] == 0 and board[oi][3] == 0:
                                # SPACE BETWEEN THEM IS EMPTY
                                left_castle_move = (ni, 2)

        return right_castle_move, left_castle_move


class Knight(pieces):
    image = 4
    moves = 0

    def possible_moves(self, board, online=False):
        moves = []
        i = self.row
        j = self.column

        # point bottom right
        if i < 6 and j < 7:
            p = board[i + 2][j + 1]
            if p == 0:
                moves.append((i + 2, j + 1))
            else:
                if p.color != self.color:
                    moves.append((i + 2, j + 1))

        # point bottom left
        if i < 6 and j > 0:
            p = board[i + 2][j - 1]
            if p == 0:
                moves.append((i + 2, j - 1))
            else:
                if p.color != self.color:
                    moves.append((i + 2, j - 1))

        # point right-down
        if i < 7 and j < 6:
            p = board[i + 1][j + 2]
            if p == 0:
                moves.append((i + 1, j + 2))
            else:
                if p.color != self.color:
                    moves.append((i + 1, j + 2))

        # point left-down
        if i < 7 and j > 1:
            p = board[i + 1][j - 2]
            if p == 0:
                moves.append((i + 1, j - 2))
            else:
                if p.color != self.color:
                    moves.append((i + 1, j - 2))

        # point top right
        if i > 1 and j < 7:
            p = board[i - 2][j + 1]
            if p == 0:
                moves.append((i - 2, j + 1))
            else:
                if p.color != self.color:
                    moves.append((i - 2, j + 1))

        # point top left
        if i > 1 and j > 0:
            p = board[i - 2][j - 1]
            if p == 0:
                moves.append((i - 2, j - 1))
            else:
                if p.color != self.color:
                    moves.append((i - 2, j - 1))
        # point right top
        if i > 0 and j < 6:
            p = board[i - 1][j + 2]
            if p == 0:
                moves.append((i - 1, j + 2))
            else:
                if p.color != self.color:
                    moves.append((i - 1, j + 2))

        # point left top
        if i > 0 and j > 1:
            p = board[i - 1][j - 2]
            if p == 0:
                moves.append((i - 1, j - 2))
            else:
                if p.color != self.color:
                    moves.append((i - 1, j - 2))

        return moves


class Rook(pieces):
    image = 3
    moves = 0

    def possible_moves(self, board, online=False):
        moves = []
        i = self.row
        j = self.column

        # top
        if i > 0:
            # finding all the obstacle
            # arr will have positions(row) in increasing order
            arr = []
            for x in range(0, i):
                p = board[x][j]
                if p != 0:
                    arr.append(x)

            if len(arr) == 0:
                for k in range(0, i):
                    moves.append((k, j))
            else:
                first_obstacle_row = arr[len(arr) - 1]  # last element of array
                if board[first_obstacle_row][j].color != self.color:
                    moves.append((first_obstacle_row, j))
                for k in range(first_obstacle_row + 1, i):
                    moves.append((k, j))

        # Bottom
        if i < 7:
            # if while going down !=0 , then that coordinate is the first obstacle coordinate
            first_obs = 8
            for x in range(i + 1, 8):
                p = board[x][j]
                if p != 0:
                    first_obs = x
                    break

            # available spots
            for k in range(i + 1, first_obs):
                moves.append((k, j))
            if first_obs != 8:
                if board[first_obs][j].color != self.color:
                    moves.append((first_obs, j))

        # right
        if j < 7:
            first_obs = 8
            for x in range(j + 1, 8):
                p = board[i][x]
                if p != 0:
                    first_obs = x
                    break

            # available spots
            for k in range(j + 1, first_obs):
                moves.append((i, k))

            if first_obs != 8:
                if board[i][first_obs].color != self.color:
                    moves.append((i, first_obs))

        # left
        if j > 0:
            # finding all the obstacle
            # arr will have positions(row) in increasing order
            arr = []
            for x in range(0, j):
                p = board[i][x]
                if p != 0:
                    arr.append(x)

            if len(arr) == 0:
                for k in range(0, j):
                    moves.append((i, k))
            else:
                first_obstacle_column = arr[len(arr) - 1]  # last element of array
                if board[i][first_obstacle_column].color != self.color:
                    moves.append((i, first_obstacle_column))
                for k in range(first_obstacle_column + 1, j):
                    moves.append((i, k))

        return moves


class Pawn(pieces):
    image = 5
    moves = 0
    has_changed = False
    en_passant_left_status = False
    en_passant_right_status = False

    def possible_moves(self, board, online=False):
        moves = []
        i = self.row
        j = self.column

        if self.moves == 0:
            border_w = i - 2
            border_b = i + 2
        else:
            border_w = i - 1
            border_b = i + 1

        print(online)

        if self.color == "w" or online:
            if self.row > 0:
                arr = []
                for x in range(border_w, i):
                    p = board[x][j]
                    if p != 0:
                        arr.append(x)

                # FOR FORWARDS
                if len(arr) == 0:
                    for k in range(border_w, i):
                        moves.append((k, j))

                else:
                    for k in range(arr[len(arr) - 1] + 1, i):
                        moves.append((k, j))

                # FOR SIDES
                if j < 7:
                    p = board[i - 1][j + 1]
                    if p != 0:
                        if p.color != self.color:
                            moves.append((i - 1, j + 1))
                if j > 0:
                    p = board[i - 1][j - 1]
                    if p != 0:
                        if p.color != self.color:
                            moves.append((i - 1, j - 1))

                # EN_PASSANT MOVES
                if self.en_passant_left_status:
                    # FOR LEFT PAWN
                    if self.column > 0:
                        # OF DIFFERENT COLOR
                        if board[i][j - 1] != 0:
                            if board[i][j - 1].color != self.color:
                                moves.append((i - 1, j - 1))

                if self.en_passant_right_status:
                    # FOR RIGHT PAWN
                    if self.column < 7:
                        # OF DIFFERENT COLOR
                        if board[i][j + 1] != 0:
                            if board[i][j + 1].color != self.color:
                                moves.append((i - 1, j + 1))

            return moves

        elif self.color == "b":
            if self.row < 7:

                first_obs = border_b + 1
                for x in range(i + 1, border_b + 1):
                    p = board[x][j]
                    if p != 0:
                        first_obs = x
                        break

                # available spots

                for k in range(i + 1, first_obs):
                    moves.append((k, j))

                # FOR SIDES
                if j < 7:
                    p = board[i + 1][j + 1]
                    if p != 0:
                        if p.color != self.color:
                            moves.append((i + 1, j + 1))

                if j > 0:
                    p = board[i + 1][j - 1]
                    if p != 0:
                        if p.color != self.color:
                            moves.append((i + 1, j - 1))

                # EN PASSANT MOVES
                if self.en_passant_left_status:
                    # FOR LEFT PAWN
                    if self.column > 0:
                        # OF DIFFERENT COLOR
                        if board[i][j - 1] != 0:
                            if board[i][j - 1].color != self.color:
                                moves.append((i + 1, j - 1))

                if self.en_passant_right_status:
                    # FOR RIGHT PAWN
                    if self.column < 7:
                        # OF DIFFERENT COLOR
                        if board[i][j + 1] != 0:
                            if board[i][j + 1].color != self.color:
                                moves.append((i + 1, j + 1))

            return moves