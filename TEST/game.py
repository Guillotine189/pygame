import sys
import pygame

import socket

pygame.init()

WIDTH = 1400
HEIGHT = 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))


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

        self.rec = (self.x, self.y, self.width, self.height)



p = player(50, 50, 70, 90)
while True:
    screen.fill('white')

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

    p.move()
    p.draw()
    pygame.display.update()