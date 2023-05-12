import os
import sys

import pygame

pygame.init()

S_X = 1400
S_Y = 800
screen = pygame.display.set_mode((S_X, S_Y))
pygame.display.set_caption('I HATE THIS')

player_base_image = pygame.image.load('./images/base_mid.png')
player_base_image_up = pygame.image.load('./images/base_up.png')
player_base_image_down = pygame.image.load('./images/base_down.png')

player_base_image_rect = player_base_image.get_rect()
player_base_image_up_rect = player_base_image_up.get_rect()
player_base_image_down_rect = player_base_image_down.get_rect()

class player(pygame.sprite.Sprite):

    def __init__(self, x, y):
        super().__init__()
        self.sprites = []
        self.sprites.append(player_base_image)
        self.sprites.append(player_base_image_down)
        self.sprites.append(player_base_image)
        self.sprites.append(player_base_image_up)
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)


    def update(self):
        self.current_sprite += 1
        if self.current_sprite >= len(self.sprites):
            self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]

    def move(self, speed):
        self.rect.left += speed

clock = pygame.time.Clock()

run = True
moving_player = pygame.sprite.Group()
p1 = player(player_base_image_rect.right, player_base_image_rect.bottom)
moving_player.add(p1)

# INITIALIZE BIRD
bird = player(50, 300)
flip_bird = player(750, 300)

# MAKING SPRITE GROUP
animate_bird = pygame.sprite.Group()
animate_flip_bird = pygame.sprite.Group()

# ADDING PLAYER TO GROUP
animate_bird.add(bird)
animate_flip_bird.add(flip_bird)

run = True
while run:
    screen.fill('black')


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

    bird.move(4)
    animate_bird.draw(screen)
    animate_bird.update()
    flip_bird.move(-1)
    animate_flip_bird.draw(screen)
    animate_flip_bird.update()
    pygame.display.update()
    clock.tick(40)
