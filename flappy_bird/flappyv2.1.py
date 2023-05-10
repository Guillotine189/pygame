import sys

import pygame

pygame.init()
pygame.font.init()


# SET SCREEN
SET_WIDTH = 1400
SET_HEIGHT = 800
screen = pygame.display.set_mode((SET_WIDTH, SET_HEIGHT))


# SET FONTS
font_menu = pygame.font.SysFont('monospace', 50)


# IMAGES PLAYER
player_base_image = pygame.image.load('./images/base.png').convert_alpha()
player_base_image_flip = pygame.image.load('./images/base_flip.png').convert_alpha()
player_gameplay_base = pygame.image.load('./images/base.png')

# PLAYER RECTANGLES
player_base_image_rect = player_base_image.get_rect(midleft=(50, 300))
player_base_image_flip_rect = player_base_image_flip.get_rect(midright=(750, 300))
player_gameplay_base_rect = player_gameplay_base.get_rect(midleft=(50, 150))


# BACKGROUND IMAGES
background_menu = pygame.image.load('./images/menu_1400x800.png').convert_alpha()
background_play = pygame.image.load('./images/main_1400x800.png').convert_alpha()



class player:
    def __init__(self, x, y):
        self.x = x

    def move(self, a):
        player_gameplay_base_rect.top += a

    def draw(self, z):
        screen.blit(z, player_gameplay_base_rect)


# class wall:
#     def __init__(self, up_x,up_y,down_x,down_y):
#         self.up_y = up_y
#         self.up_x = up_x
#         self.down_x = down_x
#         self.down_y = down_y
#
#     def move(self, speed):
#         self.speed = speed

gravity = 0


def second():
    print("Main")
    global gravity
    while True:

        screen.fill('black')
        screen.blit(background_play, (0, 0))
        p1 = player(50, 150)


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    main_menu()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    gravity = -4.8
                if event.key == pygame.K_ESCAPE:
                    main_menu()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # event.button = 1 - left , 2-right, 3-middle,  4-wheel up, 5-wheel down
                    gravity = -4.8

        gravity += 0.1
        p1.move(gravity)
        if player_gameplay_base_rect.bottom >= SET_HEIGHT + 50:
            player_gameplay_base_rect.bottom = SET_HEIGHT + 50
        if player_gameplay_base_rect.top <= -50:
            player_gameplay_base_rect.top = -50


        p1.draw(player_gameplay_base)
        pygame.display.update()



def main_menu():
    global gravity
    print("MENU")
    menu_text = font_menu.render('MENU', False, 'black')
    direction = 'right'
    while True:
        #   FILL SCREEN
        screen.fill('black')

        # SCREEN MENU + TEXT
        screen.blit(background_menu, (0, 0))
        screen.blit(menu_text, (950, 200))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player_gameplay_base_rect.top = 150
                    gravity = 0
                    second()
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()


        if direction == 'right' and player_base_image_rect.right < 750:
            player_base_image_rect.left += 1
            screen.blit(player_base_image, player_base_image_rect)
        if direction == 'right' and player_base_image_rect.right >= 750:
            direction = 'left'
            screen.blit(player_base_image_flip, player_base_image_flip_rect)
            player_base_image_rect.left = 50
        if direction == 'left' and player_base_image_flip_rect.left > 50:
            player_base_image_flip_rect.left -= 1
            screen.blit(player_base_image_flip, player_base_image_flip_rect)
        if direction == 'left' and player_base_image_flip_rect.left <= 50:
            direction = 'right'
            screen.blit(player_base_image, player_base_image_rect)
            player_base_image_flip_rect.right = 750

        pygame.display.update()






main_menu()
