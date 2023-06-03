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
starting_text = font_.render('STARTING GAME', True, 'white')
starting_text_rec = starting_text.get_rect()
kills_server = font_.render("KILL SERVER", True, 'white')
kills_server_rec = kills_server.get_rect()




class Network:

    def __init__(self):
        self.host = '127.0.0.1'
        self.port = 9900
        self.format = 'utf-8'
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.status = False
        self.first_message = self.connect()


    def connect(self):
        try:
            self.client.connect((self.host, self.port))
            message = self.client.recv(1024).decode(self.format)
            if message != '0':
                self.status = True
                return message
            else:
                return 0
        except:
            print("ERROR IN INITIAL CONNECTION")
            return 0


    def close(self):
        try:
            self.client.send("!D".encode(self.format))
            self.client.close()
            self.status = False
            print("DISCONNECTED")
        except:
            print("SERVER DOWN")
            self.status = False
    def close_all(self):
        try:
            self.client.send("!SD".encode(self.format))
            self.client.close()
            self.status = False
            print("DISCONNECTED")
        except:
            print("SERVER DOWN")
            self.status = False

    def send(self, msg):
        try:
            self.client.send(msg.encode(self.format))
            return self.client.recv(1024).decode(self.format)
        except:
            print("ERROR IN FUNCTION 'Send' ")
            self.status = False



# Takes a touple and converts it into a string

def make_msg(msg):
    pass

# Takes the string and convert it into touple

def read_msg(msg):
    pass





def server_down():
    while True:
        screen.fill('black')
        screen.blit(font_.render('SERVER DOWN', True, 'white'), (WIDTH/2 - 200, HEIGHT/2))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    start()

        pygame.display.update()


def second():
    Player = Network()
    connection_status = Player.first_message
    print(connection_status)

    if connection_status == 0:
        server_down()

    while Player.status:
        screen.fill('black')
        connected_text_rec.center = (WIDTH/2, HEIGHT/2)
        screen.blit(connected_text, connected_text_rec)
        starting_text_rec.center = (WIDTH/2, HEIGHT/2 + 60)
        screen.blit(starting_text, starting_text_rec)
        kills_server_rec.center = (WIDTH/2, HEIGHT/2 + 150)
        screen.blit(kills_server, kills_server_rec)

        mpos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    Player.close()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if kills_server_rec.collidepoint(mpos):
                    Player.close_all()

        pygame.display.update()




def start():

    while True:
        screen.fill('black')
        to_connect_text_rec.center = (WIDTH/2, HEIGHT/2)
        screen.blit(to_connect_text, to_connect_text_rec)

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
                        second()
                        break
                    except:
                        print("COULD NOT CONNECT..")



        pygame.display.update()

start()