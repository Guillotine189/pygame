import sys
import threading

import pygame

import socket

pygame.init()
pygame.font.init()

WIDTH = 1400
HEIGHT = 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))

font_ = pygame.font.SysFont('monospace', 50)
to_connect_text = font_.render('CLICK TO CONNECT', True, 'white')
to_connect_text_rec = to_connect_text.get_rect()
connected_text = font_.render('CONNECTED!', True, 'white')
connected_text_rec = connected_text.get_rect()


connected = False
to_connect = False



# def receive():
#     global connected, to_connect
#
#     while to_connect:
#         try:
#
#             if message == '200':
#                 print("CONNECTION ESTABLISHED!")
#             else:
#                 pass
#
#         except:
#             print("ERROR IN CONNECTION")
#             to_connect = False
#             connected = False
#             client.close()

class player:

    def __init__(self, x, y, height, width):
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.speed = 1
        self.rec = (self.x, self.y, self.width, self.height)

    def draw(self):
        pygame.draw.rect(screen, 'green', self.rec)

    def move(self):
        key = pygame.key.get_pressed()

        if key[pygame.K_RIGHT]:
            self.x += self.speed

        if key[pygame.K_LEFT]:
            self.x -= self.speed

        if key[pygame.K_UP]:
            self.y -= self.speed

        if key[pygame.K_DOWN]:
            self.y += self.speed

        self.update()

    def update(self):
        self.rec = (self.x, self.y, self.width, self.height)




class Network:
    def __init__(self):
        self.HOST = '127.0.0.1'
        self.PORT = 9900
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.FORMAT = 'utf-8'
        self.pos_start = self.connect()

    def connect(self):
        global connected
        try:
            self.client.connect((self.HOST, self.PORT))
            connected = True
            return self.client.recv(1024).decode(self.FORMAT)
        except:
            pass

    def close(self):
        self.client.close()

    def send(self, msg):
        try:
            self.client.send(msg.encode(self.FORMAT))
            return self.client.recv(1024).decode(self.FORMAT)
        except:
            pass


def read(string):
        string = string.split(',')
        return int(string[0]), int(string[1])


def make(tup):
        return str(tup[0]) + "," + str(tup[1])


def play():

    global connected

    client = Network()
    start_pos = read(client.pos_start)
    print(start_pos)
    print(connected)

    p2 = player(start_pos[0], start_pos[1], 70, 90)
    p1 = player(150, 250, 70, 90)

    while connected:
        screen.fill('white')

        p2_pos = read(client.send(make((p1.x, p1.y))))
        p2.x = p2_pos[0]
        p2.y = p2_pos[1]


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                connected = False
                temp = client.send('!D')
                print(temp)
                client.close()
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    connected = False
                    temp = client.send('!D')
                    print(temp)
                    client.close()
                    start()

        p1.move()

        if p1.x < 0:
            p1.x = 0
        if p1.x + 90 > WIDTH:
            p1.x = WIDTH - 90
        if p1.y + 70 > HEIGHT:
            p1.y = HEIGHT - 70
        if p1.y < 0:
            p1.y = 0

        p1.update()
        p2.update()
        p1.draw()
        p2.draw()
        pygame.display.update()



def start():
    global connected
    while True:

        screen.fill('black')
        to_connect_text_rec.center = (WIDTH/2, HEIGHT/2)
        screen.blit(to_connect_text, to_connect_text_rec)
        pygame.draw.rect(screen, 'white', to_connect_text_rec, 2)

        mpos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if to_connect_text_rec.collidepoint(mpos):
                    try:
                        # connected = True
                        # recv_thread = threading.Thread(target=receive)
                        # recv_thread.start()
                        play()
                    except:
                        print("ERROR")


        pygame.display.update()

start()

