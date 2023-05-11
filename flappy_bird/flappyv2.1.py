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
bird_font_menu = pygame.font.SysFont('monospace', 30)


# IMAGES PLAYER
player_base_image = pygame.image.load('./images/base.png').convert_alpha()
player_base_image_flip = pygame.image.load('./images/base_flip.png').convert_alpha()
player_gameplay_base = pygame.image.load('./images/base.png').convert_alpha()


# BACKGROUND IMAGES
background_menu = pygame.image.load('./images/menu_1400x800.png').convert_alpha()
background_play = pygame.image.load('./images/main_1400x800.png').convert_alpha()


# OBSTACLE INITIAL POSITION
obs1_up_co = (1550, 700)
obs2_up_co = (1850, 750)
obs3_up_co = (2150, 800)
obs4_up_co = (2450, 720)
obs5_up_co = (2750, 600)

obs1_down_co = (1550, 0)
obs2_down_co = (1850, 0)
obs3_down_co = (2150, 0)
obs4_down_co = (2450, 0)
obs5_down_co = (2750, 0)

# PIPE FACING DOWN CAN COME DOWN MAX = 215 FROM Y AXIS BEFORE IT ENDS

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


class player:

    def __init__(self, player, player_rect):
        self.player = player
        self.player_rect = player_rect
        self.hitbox = pygame.Rect(player_rect.left + 60, player_rect.top + 50, 135, 95)# top left, top right, width, height

    def move(self, a):
        self.player_rect.top += a

    def draw(self):
        screen.blit(self.player, self.player_rect)

class tube:

    def __init__(self, obstacle, obstacle_rect):
        self.obstacle = obstacle
        self.obstacle_rect = obstacle_rect
        self.hitbox_up = pygame.Rect(obstacle_rect.left + 60, obstacle_rect.top + 30, 110, 1000) # top left, top right, width, height
        self.hitbox_down = pygame.Rect(obstacle_rect.left + 60, obstacle_rect.top + 5, 110, 418)  # top left, top right, width, height
        screen.blit(self.obstacle, self.obstacle_rect)

    def move(self, obstacle_rect, speed):
        obstacle_rect.left += speed

    def position(self, rect_midright_pos):
        self.obstacle_rect.right = rect_midright_pos

    def check(self, value):
        if self.obstacle_rect.right < value:
            return 1
        else:
            return 0


gravity = 0


def second():
    count = 0
    pygame.display.set_caption('FLAPPY BIRD')
    print("Main")

    # INITIALIZE PLAYER RECTANGLES
    player_gameplay_base_rect = player_gameplay_base.get_rect(midleft=(50, 300))

    # INITIALIZE OBSTACLE RECTANGLE
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

    global gravity

    gravity = 0
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
        p1 = player(player_gameplay_base, player_gameplay_base_rect)

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
                    count += 1
                if event.key == pygame.K_ESCAPE:
                    main_menu()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # event.button = 1 - left , 2-right, 3-middle,  4-wheel up, 5-wheel down
                    gravity = -3.8
                    count += 1

        if p1.hitbox.colliderect(OB1.hitbox_up) or p1.hitbox.colliderect(OB2.hitbox_up) or p1.hitbox.colliderect(OB3.hitbox_up):
            print("COLLIDE1")
            third(count)
        if p1.hitbox.colliderect(OB4.hitbox_up) or p1.hitbox.colliderect(OB5.hitbox_up) or p1.hitbox.colliderect(OB6.hitbox_down):
            print("COLLIDE2")
            third(count)
        if p1.hitbox.colliderect(OB7.hitbox_down) or p1.hitbox.colliderect(OB8.hitbox_down) or p1.hitbox.colliderect(OB8.hitbox_down) or p1.hitbox.colliderect(OB10.hitbox_down):
            print("COLLIDE3")
            third(count)

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

        if OB1.check(0):
            OB1.position(obs_new_pos_up)
        if OB2.check(0):
            OB2.position(obs_new_pos_up)
        if OB3.check(0):
            OB3.position(obs_new_pos_up)
        if OB4.check(0):
            OB4.position(obs_new_pos_up)
        if OB5.check(0):
            OB5.position(obs_new_pos_up)

        if OB6.check(0):
            OB6.position(obs_new_pos_down)
        if OB7.check(0):
            OB7.position(obs_new_pos_down)
        if OB8.check(0):
            OB8.position(obs_new_pos_down)
        if OB9.check(0):
            OB9.position(obs_new_pos_down)
        if OB10.check(0):
            OB10.position(obs_new_pos_down)

        if player_gameplay_base_rect.bottom >= SET_HEIGHT + 50:
            player_gameplay_base_rect.bottom = SET_HEIGHT + 50
        if player_gameplay_base_rect.top <= -50:
            player_gameplay_base_rect.top = -50


        p1.draw()
        pygame.draw.rect(screen, 'black', p1.hitbox, 2)
        pygame.draw.rect(screen, 'black', OB1.hitbox_up, 2)
        pygame.draw.rect(screen, 'black', OB2.hitbox_up, 2)
        pygame.draw.rect(screen, 'black', OB3.hitbox_up, 2)
        pygame.draw.rect(screen, 'black', OB4.hitbox_up, 2)
        pygame.draw.rect(screen, 'black', OB5.hitbox_up, 2)
        pygame.draw.rect(screen, 'black', OB6.hitbox_down, 2)
        pygame.draw.rect(screen, 'black', OB7.hitbox_down, 2)
        pygame.draw.rect(screen, 'black', OB8.hitbox_down, 2)
        pygame.draw.rect(screen, 'black', OB9.hitbox_down, 2)
        pygame.draw.rect(screen, 'black', OB10.hitbox_down, 2)

        pygame.display.update()


HIGH_SCORE = 0

def third(x):
    global HIGH_SCORE

    print('LOOSE')
    pygame.display.set_caption('BETTER LUCK NEXT TIME')
    dead_image = pygame.image.load('./images/dead_final_60.png').convert_alpha()

    if x > HIGH_SCORE:
        score = font_menu.render("NEW HIGH SCORE : " + str(x), 1, (0, 0, 0))
        HIGH_SCORE = x
        y = 430
        z = 200
    else:
        score = font_menu.render("SCORE :  " + str(x), 1, (0, 0, 0))
        y = 500
        z = 200

    while True:

        screen.fill('black')
        screen.blit(background_play, (0, 0))
        screen.blit(score, (y, z))
        screen.blit(dead_image, (630, 350))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    main_menu()

        pygame.display.update()



def main_menu():

    # INITIALIZE PLAYER RECTANGLES
    player_base_image_rect = player_base_image.get_rect(midleft=(50, 300))
    player_base_image_flip_rect = player_base_image_flip.get_rect(midright=(750, 300))

    pygame.display.set_caption('MENU')

    print("MENU")
    menu_text = font_menu.render('MENU', False, 'black')
    direction = 'right'
    while True:
        # FILL SCREEN
        screen.fill('black')

        # SCREEN MENU
        screen.blit(background_menu, (0, 0))
        screen.blit(menu_text, (950, 200))

        # BIRD
        bird = player(player_base_image, player_base_image_rect)
        flip_bird = player(player_base_image_flip, player_base_image_flip_rect)

        # TEXT AND THEIR RECTANGLES
        leave_alone_text = bird_font_menu.render('LEAVE ME ALONE', True, 'black').convert_alpha()
        help_text = bird_font_menu.render('SOMEONE HELP ME !', True, 'black').convert_alpha()

        # mouse
        m_pos = pygame.mouse.get_pos()

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

        # MOUSE ON BIRD
        if bird.hitbox.collidepoint(m_pos) and direction == 'right':
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                screen.blit(help_text, bird.player_rect.topleft)
            else:
                screen.blit(leave_alone_text, bird.player_rect.topleft)

        if flip_bird.hitbox.collidepoint(m_pos) and direction == 'left':
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                screen.blit(help_text, flip_bird.player_rect.topleft)
            else:
                screen.blit(leave_alone_text, flip_bird.player_rect.topleft)


        # MOVING BIRD L->R and R->L
        if direction == 'right' and bird.player_rect.left <= 750:
            bird.player_rect.left += 1
            bird.draw()
        if direction == 'right' and bird.player_rect.right > 750:
            direction = 'left'
            flip_bird.draw()
            bird.player_rect.left = 50
        if direction == 'left' and flip_bird.player_rect.left > 50:
            flip_bird.player_rect.left -= 1
            flip_bird.draw()
        if direction == 'left' and flip_bird.player_rect.left <= 50:
            direction = 'right'
            bird.draw()
            flip_bird.player_rect.right = 750

        pygame.display.update()



main_menu()
