import socket
import threading

HOST = '127.0.0.1'
PORT = 9901

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

FORMAT = 'utf-8'

clients = []


# def read(string):
#     string = string.split(',')
#     return int(string[0]), int(string[1])
#
#
# def make(tup):
#     return str(tup[0]) + "," + str(tup[1])

running = True

def DISCONNECT(client, addr):
    clients.remove(client)
    print(f"{addr} DISCONNECTED")
    # print("LISTENING...")



def receive(client, addr):
    global running
    while True:
        try:
            message = client.recv(1024).decode(FORMAT)

            if message == "!D":
                print(message)
                DISCONNECT(client, addr)
                break
            elif message == "!SD":
                print(message)
                print(f"Command to switch off server received {addr}")
                DISCONNECT(client, addr)
                running = False
                break
            else:
                pass
        except:
            print(f"DISCONNECTED FROM {addr}")
            clients.remove(client)
            break





while running:
    print("LISTENING...")
    client, addr = server.accept()
    print(running)
    print(f"connected to {addr}")
    if not running:
        print("TURNING OFF SERVER..")
        client.send('0'.encode(FORMAT))
        break
    clients.append(client)
    client.send('200 status - CONNECTED'.encode(FORMAT))

    client_thread = threading.Thread(target=receive, args=(client, addr))
    client_thread.start()
