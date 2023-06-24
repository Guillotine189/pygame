import socket
import threading
from board import Board
from Pieces import *

HOST, PORT = '10.0.0.238', 9994


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()
FORMAT = 'utf-8'

current_player_color = 'w'
other_player_color = 'b'


# GAME VARIABLES
status = [0, 0]  # player 1 and 2 online status
has_played_move = 0
move_played = 0, 0, 0, 0
total_moves = 0
last_move = '0'
new_moves = '0'
end = '0'
end_payload = ''

# GAME
bo = Board(8, 8, 0, 'w')



def make_moves(tup):
    return str(tup[0]) + " " + str(tup[1]) + " " + str(tup[2]) + " " + str(tup[3])

def read_moves(moves):
    moves_ = moves.split(" ")
    return int(moves_[0]), int(moves_[1]), int(moves_[2]), int(moves_[3])


def receive(client, pl_no):

    global status, player_no, current_player_color, other_player_color, move_played, has_played_move, last_move, new_moves, end_payload, end, total_moves

    status[pl_no] = 1

    if pl_no == 0:
        my_color = 'w'
    else:
        my_color = 'b'

    temp_move = ''


    while True:
        try:
            message = client.recv(1024).decode(FORMAT)

            if message == 'init':
                status[pl_no] = 1
                client.send(my_color.encode(FORMAT))

            if message == 'con_stat':
                if pl_no == 0:
                    client.send(str(status[1]).encode(FORMAT))
                else:
                    client.send(str(status[0]).encode(FORMAT))

            if message == 'current_player':
                client.send(current_player_color.encode(FORMAT))

            if message == 'MOVED':
                client.send('ok'.encode(FORMAT))
                moves = client.recv(1024).decode(FORMAT)
                moves = read_moves(moves)
                print(moves, "ORIGINAL MOVES RECVEIVED")
                # for white new_moves are same moves
                new_moves = moves
                # FOR WHITE moves are all good but for black you need to change it then
                # check it then send back the commands accordingly

                if current_player_color == 'b':
                    new_moves = [i for i in moves]
                    new_moves[0] = 7 - new_moves[0]  # row of original move
                    new_moves[1] = 7 - new_moves[1]
                    new_moves[2] = 7 - new_moves[2]  # row of new move
                    new_moves[3] = 7 - new_moves[3]
                    print(new_moves,  " PASSING MOVES")
                    # NOW analise the move on servers board
                    # temp_move will contain the modified coordinate bor black or original for white
                piece_was_not_able_to_move, temp_move = bo.move_piece(new_moves[0], new_moves[1], new_moves[2], new_moves[3], current_player_color, 1)

                if piece_was_not_able_to_move:
                    client.send("1".encode(FORMAT))
                else:

                    # TURNING OFF EN PASANT STATUS OF ENEMY FALSE
                    for ti in range(8):
                        for tj in range(8):
                            if bo.board[ti][tj] != 0 and isinstance(bo.board[ti][tj], Pawn) and bo.board[ti][tj].color == current_player_color:
                                if bo.board[ti][tj].en_passant_left_status or bo.board[ti][tj].en_passant_right_status:
                                    bo.board[ti][tj].en_passant_left_status = False
                                    bo.board[ti][tj].en_passant_right_status = False

                    # TURNING EN_PASSANT STATUS OF ENEMY PAWN TRUE
                    if isinstance(bo.board[new_moves[2]][new_moves[3]], Pawn) and abs(new_moves[0] - new_moves[2]) == 2:
                        # FOR ENEMY PAWN ON LEFT
                        if new_moves[3] > 0:
                            if bo.board[new_moves[2]][new_moves[3] - 1] != 0 and isinstance(
                                    bo.board[new_moves[2]][new_moves[3] - 1], Pawn) and bo.board[new_moves[2]][new_moves[3] - 1].color != current_player_color:
                                bo.board[new_moves[2]][new_moves[3] - 1].en_passant_right_status = True
                                if current_player_color == 'b':
                                    temp_move += f' bo.board[{7-new_moves[2]}][{7-(new_moves[3]-1)}].en_passant_right_status=True'
                                else:
                                    temp_move += f' bo.board[{new_moves[2]}][{(new_moves[3] - 1)}].en_passant_left_status=True'
                        # FOR ENEMY PAWN ON RIGHT
                        if new_moves[3] < 7:
                            if bo.board[new_moves[2]][new_moves[3] + 1] != 0 and isinstance(
                                    bo.board[new_moves[2]][new_moves[3] + 1], Pawn) and bo.board[new_moves[2]][new_moves[3] + 1].color != current_player_color:
                                bo.board[new_moves[2]][new_moves[3] + 1].en_passant_left_status = True
                                if current_player_color == 'b':
                                    temp_move += f' bo.board[{7-new_moves[2]}][{7-(new_moves[3]+1)}].en_passant_left_status=True'
                                else:
                                    temp_move += f' bo.board[{new_moves[2]}][{(new_moves[3] + 1)}].en_passant_right_status=True'



                    client.send("0".encode(FORMAT))

            if message == 'new_board':
                payload = temp_move

                if payload == 'change_piece()':
                    client.send(payload.encode(FORMAT))
                    new_piece = client.recv(8).decode(FORMAT)

                    if current_player_color == 'w':
                        if new_piece == 'Q':
                            bo.board[new_moves[2]][new_moves[3]] = Queen(new_moves[2], new_moves[3], current_player_color)
                            bo.board[new_moves[0]][new_moves[1]] = 0
                            payload = f'bo.board[{new_moves[2]}][{new_moves[3]}]=Queen({new_moves[2]},{new_moves[3]},"{current_player_color}")'
                            payload += f' bo.board[{new_moves[0]}][{new_moves[1]}]=0'
                        if new_piece == 'B':
                            bo.board[new_moves[2]][new_moves[3]] = Bishop(new_moves[2], new_moves[3], current_player_color)
                            bo.board[new_moves[0]][new_moves[1]] = 0
                            payload = f'bo.board[{new_moves[2]}][{new_moves[3]}]=Bishop({new_moves[2]},{new_moves[3]},"{current_player_color}")'
                            payload += f' bo.board[{new_moves[0]}][{new_moves[1]}]=0'
                        if new_piece == 'R':
                            bo.board[new_moves[2]][new_moves[3]] = Rook(new_moves[2], new_moves[3], current_player_color)
                            bo.board[new_moves[0]][new_moves[1]] = 0
                            payload = f'bo.board[{new_moves[2]}][{new_moves[3]}]=Rook({new_moves[2]},{new_moves[3]},"{current_player_color}")'
                            payload += f' bo.board[{new_moves[0]}][{new_moves[1]}]=0'
                        if new_piece == 'K':
                            bo.board[new_moves[2]][new_moves[3]] = Knight(new_moves[2], new_moves[3], current_player_color)
                            bo.board[new_moves[0]][new_moves[1]] = 0
                            payload = f'bo.board[{new_moves[2]}][{new_moves[3]}]=Knight({new_moves[2]},{new_moves[3]},"{current_player_color}")'
                            payload += f' bo.board[{new_moves[0]}][{new_moves[1]}]=0'

                    else:
                        if new_piece == 'Q':
                            bo.board[new_moves[2]][new_moves[3]] = Queen(new_moves[2], new_moves[3],current_player_color)
                            bo.board[new_moves[0]][new_moves[1]] = 0
                            payload = f'bo.board[{7-new_moves[2]}][{7-new_moves[3]}]=Queen({7-new_moves[2]},{7-new_moves[3]},"{current_player_color}")'
                            payload += f' bo.board[{7-new_moves[0]}][{7-new_moves[1]}]=0'
                        if new_piece == 'B':
                            bo.board[new_moves[2]][new_moves[3]] = Bishop(new_moves[2], new_moves[3], current_player_color)
                            bo.board[new_moves[0]][new_moves[1]] = 0
                            payload = f'bo.board[{7-new_moves[2]}][{7-new_moves[3]}]=Bishop({7-new_moves[2]},{7-new_moves[3]},"{current_player_color}")'
                            payload += f' bo.board[{7-new_moves[0]}][{7-new_moves[1]}]=0'
                        if new_piece == 'R':
                            bo.board[new_moves[2]][new_moves[3]] = Rook(new_moves[2], new_moves[3], current_player_color)
                            bo.board[new_moves[0]][new_moves[1]] = 0
                            payload = f'bo.board[{7-new_moves[2]}][{7-new_moves[3]}]=Rook({7-new_moves[2]},{7-new_moves[3]},"{current_player_color}")'
                            payload += f' bo.board[{7-new_moves[0]}][{7-new_moves[1]}]=0'
                        if new_piece == 'K':
                            bo.board[new_moves[2]][new_moves[3]] = Knight(new_moves[2], new_moves[3], current_player_color)
                            bo.board[new_moves[0]][new_moves[1]] = 0
                            payload = f'bo.board[{7-new_moves[2]}][{7-new_moves[3]}]=Knight({7-new_moves[2]},{7-new_moves[3]},"{current_player_color}")'
                            payload += f' bo.board[{7-new_moves[0]}][{7-new_moves[1]}]=0'


                last_move = payload
                print(payload, "SENDING TO CURRENT PLAYER")
                client.send(payload.encode(FORMAT))
                total_moves += 1

                # CHANGE PLAYER
                if current_player_color == 'w':
                    current_player_color = 'b'
                    other_player_color = 'w'
                else:
                    current_player_color = 'w'
                    other_player_color = 'b'

                # CHECK FOR CHECKMATE
                a = bo.checkmate('w')
                b = bo.checkmate('b')

                if a:
                    end_payload = 'loosing_screen("BLACK",Player)'
                    end = '1'
                elif b:
                    end_payload = 'loosing_screen("WHITE",Player)'
                    end = '1'
                # CHECK FOR STALEMATE
                c = bo.stalemate('w')
                d = bo.stalemate('b')

                if not a and not b:
                    if c:
                        end_payload = 'stalemate_screen("STALEMATE",Player) '
                        end = '1'
                        print(1)
                    elif d:
                        end_payload = 'stalemate_screen("STALEMATE",Player)'
                        end = '1'
                        print(2)
                    if total_moves >= 100:
                        end = '1'
                        end_payload = 'stalemate_screen("STALEMATE",Player)'
                        print(3)
                    if not c and not d:
                        count = 0
                        for i in range(8):
                            for j in range(8):
                                if bo.board[i][j] == 0:
                                    count += 1

                        # IF ONLY THE 2 PIECES ARE LEFT, THEY ARE KINGS THEN
                        if count == 62:
                            end = '1'
                            end_payload = 'stalemate_screen("STALEMATE",Player)'
                            print(4)
                        elif count == 61:
                            for i in range(8):
                                for j in range(8):
                                    if bo.board[i][j] != 0 and (isinstance(bo.board[i][j], Knight) or isinstance(bo.board[i][j], Bishop)):
                                        end = '1'
                                        end_payload = 'stalemate_screen("STALEMATE",Player)'
                                        print(5)


            if message == 'last_move':
                if current_player_color == my_color:
                    modified_last_move = last_move.replace('d[', 'd[7-')
                    modified_last_move = modified_last_move.replace('ve(', 've(7-')
                    modified_last_move = modified_last_move.replace('][', '][7-')
                    modified_last_move = modified_last_move.replace(',', ',7-')
                    modified_last_move = modified_last_move.replace('7-"w"', '"w"')
                    modified_last_move = modified_last_move.replace('7-"b"', '"b"')
                    modified_last_move = modified_last_move.replace('n(', 'n(7-')
                    modified_last_move = modified_last_move.replace('k(', 'k(7-')
                    modified_last_move = modified_last_move.replace('p(', 'p(7-')
                    modified_last_move = modified_last_move.replace('t(', 't(7-')
                    print(modified_last_move, "SENDING TO OTHER PLAYER")
                    client.send(modified_last_move.encode(FORMAT))
                    last_move = '0'
                else:
                    client.send('0'.encode(FORMAT))


            if message == 'end':
                client.send(end.encode(FORMAT))

            if message == 'winner':
                final_payload = ''
                final_payload += 'screen.fill((0,0,0))'
                final_payload += ' screen.blit(board_image,(0,0))'
                final_payload += ' bo.draw(screen,1)'
                final_payload += ' pygame.display.update() '
                final_payload += end_payload
                client.send(final_payload.encode(FORMAT))

            if message == 'check':
                client.send('color'.encode(FORMAT))
                color = client.recv(8).decode(FORMAT)
                if bo.check(color):
                    client.send('1'.encode(FORMAT))
                else:
                    client.send('0'.encode(FORMAT))


            #  DISCONNECTION
            if message == '!D':
                status[pl_no] = 0
                print(f"PLAYER {pl_no} DISCONNECTED")
                player_no -= 1
                status[pl_no] = 0
                break

            if not message:
                status[pl_no] = 0
                print(f"PLAYER {pl_no} DISCONNECTED")
                player_no -= 1
                break

        except Exception as e:
            player_no -= 1
            status[pl_no] = 0
            print(e)
            print(f"PLAYER {pl_no} DISCONNECTED")
            break




player_no = 0

while True:
    print("LISTENING...")
    client, addr = server.accept()
    if player_no < 2:
        print(f"CONNECTION ESTABLISHED WITH {addr}")
        client.send('Connection Established'.encode(FORMAT))
        if player_no == 0:
            current_player_color = 'w'
            other_player_color = 'b'

            status = [0, 0]  # player 1 and 2 online status

            total_moves = 0
            has_played_move = 0
            move_played = 0, 0, 0, 0
            bo = Board(8, 8, 0, 'w')
            last_move = '0'
            new_moves = '0'
            end = '0'
            end_payload = ''
        thread = threading.Thread(target=receive, args=(client, player_no))
        thread.start()
        player_no += 1
        print(player_no)
    else:
        client.send('full'.encode(FORMAT))
