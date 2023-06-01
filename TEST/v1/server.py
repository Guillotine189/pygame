import socket
import threading


HOST = '127.0.0.1'
PORT = 9901

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

FORMAT = 'utf-8'

clients = []
player_number = []

player_count = 0


def read(string):
    string = string.split(',')
    return int(string[0]), int(string[1])


def make(tup):
    return str(tup[0]) + "," + str(tup[1])


def broadcast(msg, cli):
    for person in clients:
        if person != cli:
            person.send(msg.encode(FORMAT))


pl = [(0, 0), (0, 0)]


def receive(cli, player):
    cli.send(make(pl[player]).encode(FORMAT))
    # global player_count
    while True:
        try:
            message = cli.recv(1024).decode()
            if message == '!D':
                cli.send('DISCONNECTED'.encode(FORMAT))
                cli.close()
                cli.remove(client)
                # player_count -= 1
                break
            else:
                if player == 0:
                    reply = pl[1]
                else:
                    reply = pl[0]

                pl[player] = read(message)
                cli.send(make(reply).encode(FORMAT))

        except:
            print("ERROR")
            cli.close()
            cli.remove(client)
            # player_count -= 1
            break




while True:
    print("LISTENING..")
    client, addr = server.accept()
    clients.append(client)
    cli_thread = threading.Thread(target=receive, args=(client, player_count))
    cli_thread.start()
    player_count += 1
    print(f"Players Connected: {player_count}")
