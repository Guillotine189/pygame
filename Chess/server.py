import socket
import threading
from board import Board
from Pieces import *

HOST, PORT = '10.0.0.238', 9991


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


# GAME
bo = Board(8, 8, 0, 'w')



def make_moves(tup):
    return str(tup[0]) + " " + str(tup[1]) + " " + str(tup[2]) + " " + str(tup[3])

def read_moves(moves):
    moves_ = moves.split(" ")
    return int(moves_[0]), int(moves_[1]), int(moves_[2]), int(moves_[3])

last_move = '0'

def receive(client, pl_no):

    global status, player_no, current_player_color, other_player_color, move_played, has_played_move, last_move

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
                print(moves)
                # for white new_moves are same moves
                new_moves = moves
                # FOR WHITE moves are all good but for black you need to change it then
                # check it then send back the commands accordingly

                if current_player_color == 'b':
                    new_moves = [i for i in moves]
                    print(new_moves)
                    new_moves[0] = 7 - new_moves[0]  # row of original move
                    new_moves[2] = 7 - new_moves[2]  # row of new move
                    print(new_moves)
                    # NOW analise the move on servers board
                    # temp_move will contain the modified coordinate bor black or original for white
                piece_was_not_able_to_move, temp_move = bo.move_piece(new_moves[0], new_moves[1], new_moves[2], new_moves[3], current_player_color, 1)

                if piece_was_not_able_to_move:
                    client.send("1".encode(FORMAT))
                else:
                    client.send("0".encode(FORMAT))

            if message == 'new_board':
                payload = temp_move
                last_move = temp_move
                # payload = f'{bo.board[0]}'

                print(payload)
                client.send(payload.encode(FORMAT))
                # CHANGE PLAYER
                if current_player_color == 'w':
                    current_player_color = 'b'
                    other_player_color = 'w'
                else:
                    current_player_color = 'w'
                    other_player_color = 'b'


            if message == 'last_move':
                if current_player_color == my_color:
                    modified_last_move = last_move.replace('d[', 'd[7-')
                    modified_last_move = modified_last_move.replace('ve(', 've(7-')
                    print(modified_last_move, "MODIFIED")
                    client.send(modified_last_move.encode(FORMAT))
                    last_move = '0'
                else:
                    client.send('0'.encode(FORMAT))

            #  UNUSED
            if message == 'played?':
                client.send(str(has_played_move).encode(FORMAT))
                if has_played_move:
                    has_played_move = 0

            if message == 'move_played':
                payload = make_moves(move_played)
                client.send(payload.encode(FORMAT))

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
    print(f"CONNECTION ESTABLISHED WITH {addr}")
    client.send('Connection Established'.encode(FORMAT))
    if player_no == 0:
        current_player_color = 'w'
        other_player_color = 'b'

        status = [0, 0]  # player 1 and 2 online status

        has_played_move = 0
        move_played = 0, 0, 0, 0
        bo = Board(8, 8, 0, 'w')
    thread = threading.Thread(target=receive, args=(client, player_no))
    thread.start()
    player_no += 1
    print(player_no)
