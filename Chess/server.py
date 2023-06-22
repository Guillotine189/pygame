import socket
import threading

HOST, PORT = '10.0.0.238', 9999

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()


def receive(pl_no):
    pass




player_no = 0
while True:
    client, addr = server.accept()
    player_no += 1
    thread = threading.Thread(target=receive, args=(player_no))
    thread.start()
