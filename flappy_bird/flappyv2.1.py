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
player_gameplay_base = pygame.image.load('./images/base.png').convert_alpha()

# PLAYER RECTANGLES
player_base_image_rect = player_base_image.get_rect(midleft=(50, 300))
player_base_image_flip_rect = player_base_image_flip.get_rect(midright=(750, 300))
player_gameplay_base_rect = player_gameplay_base.get_rect(midleft=(50, 150))


# BACKGROUND IMAGES
background_menu = pygame.image.load('./images/menu_1400x800.png').convert_alpha()
background_play = pygame.image.load('./images/main_1400x800.png').convert_alpha()


#3 OBSTACLE INITIAL POSITION
obs1_up_co = (550, 700)
obs2_up_co = (850, 750)
obs3_up_co = (1150, 800)
obs4_up_co = (1450, 720)
obs5_up_co = (1750, 600)

obs1_down_co = (550, 0)
obs2_down_co = (850, 0)
obs3_down_co = (1150, 0)
obs4_down_co = (1450, 0)
obs5_down_co = (1750, 0)



# OBSTACLE IMAGES
obs_down1 = pygame.image.load('./images/tube_down.png').convert_alpha()
obs_up1 = pygame.image.load('./images/tube_up.png').convert_alpha()
obs_down2 = pygame.image.load('./images/tube_down.png').convert_alpha()
obs_up2 = pygame.image.load('./images/tube_up.png').convert_alpha()
obs_down3 = pygame.image.load('./images/tube_down.png').convert_alpha()
obs_up3 = pygame.image.load('./images/tube_up.png').convert_alpha()
obs_down4 = pygame.image.load('./images/tube_down.png').convert_alpha()
obs_up4 = pygame.image.load('./images/tube_up.png').convert_alpha()
obs_down5 = pygame.image.load('./images/tube_down.png').convert_alpha()
obs_up5 = pygame.image.load('./images/tube_up.png').convert_alpha()


# OBSTACLE RECTANGLE
obs_up1_rect = obs_up1.get_rect(midright=obs1_up_co)
obs_up2_rect = obs_up2.get_rect(midright=obs2_up_co)
obs_up3_rect = obs_up3.get_rect(midright=obs3_up_co)
obs_up4_rect = obs_up4.get_rect(midright=obs4_up_co)
obs_up5_rect = obs_up5.get_rect(midright=obs5_up_co)
obs_down1_rect = obs_down1.get_rect(midright=obs1_down_co)
obs_down2_rect = obs_down1.get_rect(midright=obs2_down_co)
obs_down3_rect = obs_down1.get_rect(midright=obs3_down_co)
obs_down4_rect = obs_down1.get_rect(midright=obs4_down_co)
obs_down5_rect = obs_down1.get_rect(midright=obs5_down_co)


class player:
    def __init__(self, x,y):
        self.x = x
        self.y = y

    def move(self, a):
        player_gameplay_base_rect.top += a

    def draw(self, z):
        screen.blit(z, player_gameplay_base_rect)


class tube:
    def __init__(self, obstacle, obstacle_rect):
        self.obstacle = obstacle
        self.obstacle_rect = obstacle_rect
        screen.blit(self.obstacle, self.obstacle_rect)

    def move(self, obstacle_rect, speed):
        obstacle_rect.left += speed

    def position(self, rect_midright_pos):
        self.obstacle_rect.right = rect_midright_pos

    def check(self, obstacle_rect):
        if obstacle_rect.right < 0:
            return 1
        else:
            return 0


gravity = 0


def second():
    print("Main")
    global gravity

    tubespeed = -2
    obs_new_pos_up = 1600
    obs_new_pos_down = 1600

    while True:

        screen.fill('black')
        screen.blit(background_play, (0, 0))

        # OBSTACLE

        OB1 = tube(obs_up1, obs_up1_rect)
        OB2 = tube(obs_up2, obs_up2_rect)
        OB3 = tube(obs_up3, obs_up3_rect)
        OB4 = tube(obs_up4, obs_up4_rect)
        OB5 = tube(obs_up5, obs_up5_rect)
        OB6 = tube(obs_down1, obs_down1_rect)
        OB7 = tube(obs_down2, obs_down2_rect)
        OB8 = tube(obs_down3, obs_down3_rect)
        OB9 = tube(obs_down4, obs_down4_rect)
        OB10 = tube(obs_down5, obs_down5_rect)

        # PLAYER

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
                    gravity = -3.8
                if event.key == pygame.K_ESCAPE:
                    main_menu()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # event.button = 1 - left , 2-right, 3-middle,  4-wheel up, 5-wheel down
                    gravity = -3.8

        gravity += 0.08
        p1.move(gravity)

        OB1.move(obs_up1_rect, tubespeed)
        OB2.move(obs_up2_rect, tubespeed)
        OB3.move(obs_up3_rect, tubespeed)
        OB4.move(obs_up4_rect, tubespeed)
        OB5.move(obs_up5_rect, tubespeed)
        OB6.move(obs_down1_rect, tubespeed)
        OB7.move(obs_down2_rect, tubespeed)
        OB8.move(obs_down3_rect, tubespeed)
        OB9.move(obs_down4_rect, tubespeed)
        OB10.move(obs_down5_rect, tubespeed)

        if OB1.obstacle_rect.right < 0:
            OB1.position(obs_new_pos_up)
        if OB2.obstacle_rect.right < 0:
            OB2.position(obs_new_pos_up)
        if OB3.obstacle_rect.right < 0:
            OB3.position(obs_new_pos_up)
        if OB4.obstacle_rect.right < 0:
            OB4.position(obs_new_pos_up)
        if OB5.obstacle_rect.right < 0:
            OB5.position(obs_new_pos_up)

        if OB6.obstacle_rect.right < 0:
            OB6.position(obs_new_pos_down)
        if OB7.obstacle_rect.right < 0:
            OB7.position(obs_new_pos_down)
        if OB8.obstacle_rect.right < 0:
            OB8.position(obs_new_pos_down)
        if OB9.obstacle_rect.right < 0:
            OB9.position(obs_new_pos_down)
        if OB10.obstacle_rect.right < 0:
            OB10.position(obs_new_pos_down)

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
