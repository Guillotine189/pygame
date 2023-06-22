import socket
import threading
from board import Board
from Pieces import *

HOST, PORT = '10.0.0.238', 9999

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


def receive(client, pl_no):

    global status, player_no, current_player_color, other_player_color, move_played, has_played_move

    status[pl_no] = 1

    if pl_no == 0:
        my_color = 'w'
    else:
        my_color = 'b'

    while True:
        try:
            message = client.recv(1024).decode(FORMAT)

            if message == 'init':
                client.send(my_color.encode(FORMAT))

            if message == 'con_stat':
                if pl_no == 0:
                    client.send(str(status[1]).encode(FORMAT))
                else:
                    client.send(str(status[0]).encode(FORMAT))

            if message == 'current_player':
                client.send(current_player_color.encode(FORMAT))

            if message == 'played?':
                client.send(str(has_played_move).encode(FORMAT))
                if has_played_move:
                    has_played_move = 0

            if message == 'move_played':
                payload = make_moves(move_played)
                client.send(payload.encode(FORMAT))

            if message == '!D':
                status[pl_no] = 0
                print(f"PLAYER {pl_no} DISCONNECTED")
                player_no -= 1
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
    thread = threading.Thread(target=receive, args=(client, player_no))
    thread.start()
    player_no += 1
    print(player_no)
