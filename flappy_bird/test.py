import os
import sys

import pygame

pygame.init()
pygame.font.init()

temp_font = pygame.font.SysFont('monospace', 50)

S_X = 1400
S_Y = 800
screen = pygame.display.set_mode((S_X, S_Y))
pygame.display.set_caption('I HATE THIS')


class button:
    def __init__(self, text, x, y, w, h):
        self.text = text
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def draw(self):
        button_text = temp_font.render(self.text, True, 'black')
        pygame.draw.rect(screen, 'white', ((self.x, self.y), (self.w, self.h)))
        pygame.draw.line(screen, 'brown', (self.x, self.y,), (self.x + self.w, self.y), 4)
        pygame.draw.line(screen, 'brown', (self.x, self.y,), (self.x, self.y + self.h), 4)
        pygame.draw.line(screen, 'brown', (self.x + self.w, self.y), (self.x + self.w, self.y + self.h), 4)
        pygame.draw.line(screen, 'brown', (self.x, self.y + self.h), (self.x + self.w, self.y + self.h), 4)
        pygame.draw.rect(screen,'orange', ((self.x + 8, self.y + 5), (self.w - 14, self.h - 8)))
        screen.blit(button_text, (self.x + 15, self.y))





run = True
while run:
    screen.fill('blue')

    B1 = button('HELLO', 300, 200, 170, 50)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()


    B1.draw()
    pygame.display.update()
