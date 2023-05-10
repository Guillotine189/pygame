import sys

import pygame

pygame.init()
pygame.font.init()


# SET SCREEN
SET_WIDTH = 1400
SET_HEIGHT = 800
screen = pygame.display.set_mode((SET_WIDTH, SET_HEIGHT))


# SET FONTS
font_menu = pygame.font.Font(None, 50)


# IMAGES PLAYER
player_base_image = pygame.image.load('./images/base.png')
player_base_image_flip = pygame.image.load('./images/base_flip.png')


# BACKGROUND IMAGES
background_menu = pygame.image.load('./images/menu_1400x800.png')
background_play = pygame.image.load('./images/main_1400x800.png')


# PLAYER RECTANGLES
player_base_image_rect = player_base_image.get_rect(midbottom=(150, 400))
player_base_image_flip_rect = player_base_image_flip.get_rect(midbottom=(450, 400))


class player:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move(self, a, b):
        self.x += a
        self.y += b

    def draw(self, z):
        screen.blit(z, (self.x, self.y))


def second():
    print("Main")

    while True:

        screen.fill('black')
        screen.blit(background_play, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    main_menu()

        pygame.display.update()



def main_menu():

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
                    second()
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()


        if direction == 'right' and player_base_image_rect.right < 550:
            player_base_image_rect.left += 1
            screen.blit(player_base_image, player_base_image_rect)
        if direction == 'right' and player_base_image_rect.right >= 550:
            direction = 'left'
            screen.blit(player_base_image_flip, player_base_image_flip_rect)
            player_base_image_rect.left = 50
        if direction == 'left' and player_base_image_flip_rect.left > 50:
            player_base_image_flip_rect.left -= 1
            screen.blit(player_base_image_flip, player_base_image_flip_rect)
        if direction == 'left' and player_base_image_flip_rect.left <= 50:
            direction = 'right'
            screen.blit(player_base_image, player_base_image_rect)
            player_base_image_flip_rect.right = 550

        pygame.display.update()






main_menu()
