import sys

import pygame

pygame.init()
pygame.font.init()

SET_HEIGHT = 800
SET_WIDTH = 1400

new_font = pygame.font.Font(None, 80)

screen = pygame.display.set_mode((SET_WIDTH, SET_HEIGHT))
background = pygame.image.load('./images/main_1400x800.png').convert_alpha()
image_up = pygame.image.load("./images/tube_up.png").convert_alpha()
image_up_rect = image_up.get_rect(midtop=(800, 450))
image_up_x = 500
image_up_y = 500
image_down = pygame.image.load('./images/tube_down.png').convert_alpha()
image_down_rect = image_down.get_rect(topright=(1000, 0))
image_down_x = 500
image_down_y = -80
pygame.display.set_caption("LEARN")
player_image = pygame.image.load('./images/base.png').convert_alpha()
player_rect = player_image.get_rect(bottomright=(image_down_x + 70, 520))

text = new_font.render('Flappy bird', True, 'green')

# print(image_up_rect)

gravity = 0
clock = pygame.time.Clock()

while True:

    screen.fill('black')
    screen.blit(background, (0, 0))
    screen.blit(image_up, image_up_rect)
    screen.blit(image_down, image_down_rect)
    screen.blit(text, (50, 210))
    screen.blit(player_image, player_rect)
    mouse_pos = pygame.mouse.get_pos()


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # if event.type == pygame.MOUSEMOTION:
        #     if player_rect.collidepoint(event.pos):
        #         print('colission')
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                gravity = -4.8

    gravity += 0.1
    player_rect.top += gravity
    if image_up_rect.left <= -150:
        image_up_rect.left = 500
    if player_rect.right >= 1200:
        player_rect.right = 500
    if player_rect.bottom >= SET_HEIGHT + 50:
        player_rect.bottom = SET_HEIGHT + 50
    if player_rect.top <= -52:
        player_rect.top = -52
    pygame.display.update()
    clock.tick(150)