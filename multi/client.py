import sys

import pygame
import threading
import socket

HOST = '127.0.0.1'
PORT = 9101
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


pygame.init()
pygame.font.init()
HEIGHT = 800
WIDTH = 1400
screen = pygame.display.set_mode((WIDTH, HEIGHT))

font_ = pygame.font.SysFont('monospace', 50)
text = font_.render('CLICK TO CONNECT', 1, 'white')
text_rec = text.get_rect()
text2 = font_.render('CONNECTED!', 1, 'white')
text2_rec = text.get_rect()
text3 = font_.render('SEND MESSAGE', 1, 'white')
text3_rec = text.get_rect()

text_rec.center = (WIDTH/2, HEIGHT/2)
text2_rec.center = (WIDTH/2, HEIGHT/2)
text3_rec.center = (WIDTH/2, HEIGHT/2 + 100)


def broadcast(message):
    client.send(message.encode())


def third():
    third_run = True
    user_input = ''
    enter_text = font_.render("ENTER TEXT", True, 'white')
    enter_text_rect = enter_text.get_rect()
    enter_text_rect.center = (WIDTH/2, HEIGHT/2 - 200)
    while third_run:
        screen.fill('black')
        user_text = font_.render(user_input, True, 'White')
        user_text_rect = user_text.get_rect()
        user_text_rect.center = (WIDTH/2, HEIGHT/2)
        screen.blit(user_text, user_text_rect)
        pygame.draw.rect(screen, 'white', user_text_rect, 1)
        screen.blit(enter_text, enter_text_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    broadcast(user_input)
                    third_run = False
                if event.key == pygame.K_BACKSPACE:
                    user_input = user_input[0:-1]
                else:
                    user_input += event.unicode

        pygame.display.update()


def conn():
    screen.fill('black')
    run = True
    while run:
        screen.blit(text2, text2_rec)
        screen.blit(text3, text3_rec)
        pygame.draw.rect(screen, 'white', text3_rec, 1)

        mpos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
               if text3_rec.collidepoint(mpos):
                    third()
                    run = False

        pygame.display.update()

def start():
    global client, HOST, PORT
    pygame.display.set_caption('TEST')
    start_run = True
    while start_run:
        screen.fill('black')
        screen.blit(text, text_rec)
        mpos = pygame.mouse.get_pos()
        pygame.draw.rect(screen, 'white', text_rec, 1)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
               if text_rec.collidepoint(mpos):
                   client.connect((HOST, PORT))
                   conn()
                   start_run = False

        pygame.display.update()


start()
