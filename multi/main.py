import pygame
import threading
import socket

HEIGHT = 800
WIDTH = 1400


HOST = '127.0.0.1'
PORT = 9101

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()
print("LISTENING..")
client, addr = server.accept()
print(f"CONNECTED WiTH {addr}")
try:
    msg = client.recv(1024).decode()
    print(f"MESSAGE FROM {addr}: {msg}")
except:
    client.close()
