import threading
import socket

HEIGHT = 800
WIDTH = 1400


HOST = '127.0.0.1'
PORT = 9102

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

clients = []
nicknames = []


def broadcast(message):
    for client in clients:
        client.send(message.encode())


def remove(client):
    index = clients.index(client)
    clients.remove(client)
    nickname2 = nicknames[index]
    nicknames.remove(nickname2)


def receive(client, nickname):
    count = 0
    while True:
        try:
            msg = client.recv(1024).decode()
            if msg == '!D':
                client.send(msg.encode())
                client.close()
                remove(client)
                print(f"{nickname} DISCONNECTED")
                break
            else:
                print(f"MESSAGE FROM {nickname}: {msg}")
                broadcasting_msg = f'{nickname}: ' + msg
                broadcast(broadcasting_msg)
                count += 1
        except:
            client.send("!D".encode())
            client.close()
            remove(client)
        if count >= 30:
            client.send("!D".encode())
            client.close()
            remove(client)
            print(f"{nickname} DISCONNECTED")
            break


def start2():
    total = 0
    while True:
        print("LISTENING..")
        client, addr = server.accept()
        print(f"CONNECTED WiTH {addr}")
        client.send("NICK".encode())
        nickname = client.recv(1024).decode()
        nicknames.append(nickname)
        clients.append(client)
        receive_thread = threading.Thread(target=receive, args=(client, nickname))
        receive_thread.start()
        total += 1

        if total >= 5:
            receive_thread.join()
            break

start2()
