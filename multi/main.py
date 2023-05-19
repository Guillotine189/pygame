import threading
import socket

HEIGHT = 800
WIDTH = 1400


HOST = '127.0.0.1'
PORT = 9102

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()


def receive(client, addr):
    count = 0
    while True:
        try:
            msg = client.recv(1024).decode()
            if msg == '!D':
                client.send(msg.encode())
                client.close()
                print(f"{addr} DISCONNECTED")
                break
            else:
                print(f"MESSAGE FROM {addr}: {msg}")
                count += 1
        except:
            client.send("!D".encode())
            client.close()
        if count >= 3:
            client.send("!D".encode())
            client.close()
            print(f"{addr} DISCONNECTED")
            break



def start():
    total = 0
    while True:
        print("LISTENING..")
        client, addr = server.accept()
        print(f"CONNECTED WiTH {addr}")

        receive_thread = threading.Thread(target=receive, args=(client, addr))
        receive_thread.start()
        total += 1

        if total >= 2:
            break

start()
