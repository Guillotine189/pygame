import sys

import pygame
import threading
import socket

HOST = '127.0.0.1'
PORT = 9102

pygame.init()
pygame.font.init()
HEIGHT = 800
WIDTH = 1400
screen = pygame.display.set_mode((WIDTH, HEIGHT))

font_ = pygame.font.SysFont('monospace', 50)
text = font_.render('CLICK TO CONNECT', True, 'white')
text_rec = text.get_rect()
text2 = font_.render('CONNECTED!', True, 'white')
text2_rec = text.get_rect()
text3 = font_.render('SEND MESSAGE', True, 'white')
text3_rec = text.get_rect()

text_rec.center = (WIDTH / 2, HEIGHT / 2)
text2_rec.center = (WIDTH / 2, HEIGHT / 2)
text3_rec.center = (WIDTH / 2, HEIGHT / 2 + 100)
connected = False

nickname = ""


msg_t = font_.render('', True, 'black')


def receive(client):
    global connected, msg_t
    while connected:
        try:
            msg = client.recv(1024).decode()
            if msg == "!D":
                disconnected_text = font_.render("DISCONNECTED FROM SERVER!", True, 'white')
                screen.blit(disconnected_text, (WIDTH/2 - 200, HEIGHT/2))
                client.close()
                connected = False
            elif msg == "NICK":
                client.send(nickname.encode())
            else:
                msg_t = font_.render(msg, True, 'white')
        except:
            client.close()
            connected = False


def broadcast(message, client):
    client.send(message.encode())


def third(client):
    global connected, msg_t
    user_input = ""
    enter_text = font_.render("ENTER TEXT", True, 'white')
    enter_text_rect = enter_text.get_rect()
    enter_text_rect.center = (WIDTH / 2, HEIGHT / 2 - 200)
    msg_t_rec = msg_t.get_rect()

    while connected:
        screen.fill('black')

        user_text = font_.render(user_input, True, 'White')
        user_text_rect = user_text.get_rect()
        user_text_rect.center = (WIDTH / 2, HEIGHT / 2)
        screen.blit(user_text, user_text_rect)
        pygame.draw.rect(screen, 'white', user_text_rect, 1)
        screen.blit(enter_text, enter_text_rect)
        screen.blit(msg_t, msg_t_rec)


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                client.send('!D'.encode())
                client.close()
                connected = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    user_input = user_input[:-1]
                elif event.key == pygame.K_RETURN:
                    broadcast(user_input, client)
                    user_input = ''
                elif event.key == pygame.K_ESCAPE:
                    conn(client)
                else:
                    user_input += event.unicode

        pygame.display.update()


def conn(client):
    global connected
    screen.fill('black')
    while connected:
        screen.blit(text2, text2_rec)
        screen.blit(text3, text3_rec)
        pygame.draw.rect(screen, 'white', text3_rec, 1)

        mpos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                client.send("!D".encode())
                connected = False
                client.close()
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    client.send("!D".encode())
                    client.close()
                    connected = False
                    start2()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if text3_rec.collidepoint(mpos):
                    third(client)

        pygame.display.update()


def start2():
    global screen, HOST, PORT, connected, msg_t
    pygame.display.set_caption('TEST')

    tee2 = 'NOT CONNECTED'
    not_active_text = font_.render(tee2, True, 'white')
    while True:
        screen.fill('black')
        screen.blit(text, text_rec)
        screen.blit(not_active_text, (WIDTH - 900, 310))
        mpos = pygame.mouse.get_pos()
        pygame.draw.rect(screen, 'white', text_rec, 1)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    start()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if text_rec.collidepoint(mpos):
                    try:
                        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        client.connect((HOST, PORT))
                        connected = True
                        msg_t = font_.render('', True, 'black')
                        rec = threading.Thread(target=receive, args=(client,))
                        rec.start()
                        conn(client)
                    except:
                        connected = False

        pygame.display.update()


def start():
    global nickname
    text0 = font_.render("ENTER YOUR NICKNAME: ", True, 'white')
    text0_rec = text0.get_rect()
    text0_rec.center = (WIDTH / 2, HEIGHT / 2 - 300)
    temp = ''
    while True:
        screen.fill('black')
        screen.blit(text0, text0_rec)
        temp_text = font_.render(temp, True, 'white')
        temp_text_rec = temp_text.get_rect()
        temp_text_rec.center = (WIDTH / 2, HEIGHT / 2 - 200)
        screen.blit(temp_text, temp_text_rec)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    temp = temp[0:-1]
                elif event.key == pygame.K_RETURN:
                    nickname = temp
                    start2()
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                else:
                    temp += event.unicode

        pygame.display.update()



start()