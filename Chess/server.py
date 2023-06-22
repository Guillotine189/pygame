import socket
import threading

HOST, PORT = '10.0.0.238', 9999

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()
FORMAT = 'utf-8'

player_color = 'w'

status = [0, 0]  # player 1 and 2 online status

def receive(client, pl_no):

    global status, player_no

    status[pl_no] = 1

    if pl_no == 0:
        my_color = 'w'
    else:
        my_color = 'b'

    while True:
        try:
            message = client.recv(1024).decode(FORMAT)

            if message == 'init':
                print('init received')
                client.send(my_color.encode(FORMAT))

            if message == 'con_stat':
                if pl_no == 0:
                    client.send(str(status[1]).encode(FORMAT))
                else:
                    client.send(str(status[0]).encode(FORMAT))

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
    thread = threading.Thread(target=receive, args=(client, player_no))
    thread.start()
    player_no += 1
    print(player_no)
