import sys
import random
import pygame
from pygame import mixer

pygame.init()
pygame.font.init()
mixer.init()

menu_sound = mixer.Sound('./sounds/main_menu.ogg')
game_music = mixer.Sound('./sounds/gameplay_sound.ogg')
flap = mixer.Sound('./sounds/flap.wav')
score_s = mixer.Sound('./sounds/point.wav')
die = mixer.Sound('./sounds/diesound.wav')
hit = mixer.Sound('./sounds/hit.wav')
exit_screen_sound = mixer.Sound('./sounds/exit_screen.wav')
button_sound = mixer.Sound('./sounds/button.wav')

# SET SCREEN
SET_WIDTH = 1400
SET_HEIGHT = 800
screen = pygame.display.set_mode((SET_WIDTH, SET_HEIGHT))


# SET FONTS
font_menu = pygame.font.SysFont('monospace', 50, 30)
bird_font_menu = pygame.font.SysFont('monospace', 30, 20)


# IMAGES PLAYER
player_base_image = pygame.image.load('./images/base.png').convert_alpha()
player_base_image_flip = pygame.image.load('./images/base_flip.png').convert_alpha()
player_gameplay_base = pygame.image.load('./images/base.png').convert_alpha()
dead_image = pygame.image.load('./images/dead_final_60.png').convert_alpha()
dead_image_up = pygame.image.load('./images/dead_final_60_up.png').convert_alpha()


# BACKGROUND IMAGES
background_menu = pygame.image.load('./images/background_menu_1400x800.png').convert_alpha()
background_play = pygame.image.load('./images/main_1400x800.png').convert_alpha()

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
        self.hitbox = pygame.rect.Rect(player_rect.left + 60, player_rect.top + 50, 135, 95)# top left, top right, width, height

    def move(self, a):
        self.player_rect.top += a

    def draw(self):
        screen.blit(self.player, self.player_rect)

class tube:

    def __init__(self, obstacle, obstacle_rect):
        self.obstacle = obstacle
        self.obstacle_rect = obstacle_rect
        self.hitbox_up = pygame.rect.Rect(obstacle_rect.left + 60, obstacle_rect.top + 30, 110, 1000) # top left, top right, width, height
        self.hitbox_down = pygame.rect.Rect(obstacle_rect.left + 60, obstacle_rect.top + 5, 110, 418)
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




class button:
    def __init__(self, text, x, y, w, h):
        self.text = text
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def draw(self):
        button_text = font_menu.render(self.text, True, 'black')
        button_rect = pygame.rect.Rect((self.x, self.y), (self.w, self.h))
        if self.check_hover():
            pygame.draw.rect(screen, 'dark grey', button_rect, 0, 5)
        else:
            pygame.draw.rect(screen, 'grey', button_rect, 0, 5)

        screen.blit(button_text, (self.x + 15, self.y))


    def check_click(self):
        left_button = pygame.mouse.get_pressed()[0]
        button_rect = pygame.rect.Rect((self.x, self.y), (self.w, self.h))
        mouse_pos = pygame.mouse.get_pos()
        if left_button and button_rect.collidepoint(mouse_pos):
            button_sound.play()
            return 1
        else:
            return 0

    def check_hover(self):
        mouse_pos = pygame.mouse.get_pos()
        button_rect = pygame.rect.Rect((self.x, self.y), (self.w, self.h))
        if button_rect.collidepoint(mouse_pos):
            return 1
        else:
            return 0

def main_menu():

    # INITIALIZE PLAYER RECTANGLES
    player_base_image_rect = player_base_image.get_rect(midleft=(50, 300))
    player_base_image_flip_rect = player_base_image_flip.get_rect(midright=(750, 300))

    pygame.display.set_caption('MENU')

    #PLAY SOUND
    menu_sound.play()

    print("MENU")
    menu_text = font_menu.render('MENU', False, (12, 130, 72))
    direction = 'right'
    while True:

        # FILL SCREEN
        screen.fill('black')

        # SCREEN MENU
        screen.blit(background_menu, (0, 0))
        screen.blit(menu_text, (900, 300))
        pygame.draw.rect(screen, 'black', (895, 305, 130, 40), 1)

        # pygame.draw.line(screen, 'black', (900, 345), (1017, 345), 2)

        # INITIALIZE BIRD
        bird = player(player_base_image, player_base_image_rect)
        flip_bird = player(player_base_image_flip, player_base_image_flip_rect)

        # RENDERING TEXT
        leave_alone_text = bird_font_menu.render('LEAVE ME ALONE', True, 'black').convert_alpha()
        help_text = bird_font_menu.render('SOMEONE HELP ME !', True, 'black').convert_alpha()

        # INITIALIZE BUTTON
        button1 = button('PLAY', 800, 400, 150, 50)
        button2 = button('EXIT', 1000, 400, 150, 50)

        # mouse
        m_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("EXITING")
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    menu_sound.stop()
                    second()
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button1.check_click():
                    menu_sound.stop()
                    second()
                if button2.check_click():
                    print("EXITING")
                    pygame.quit()
                    sys.exit()

        # MOUSE ON BIRD
        if bird.hitbox.collidepoint(m_pos) and direction == 'right':
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                screen.blit(help_text, (bird.player_rect.left + 10, bird.player_rect.top))
            else:
                screen.blit(leave_alone_text, (bird.player_rect.left + 10, bird.player_rect.top))

        if flip_bird.hitbox.collidepoint(m_pos) and direction == 'left':
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                screen.blit(help_text, (flip_bird.player_rect.left + 10, flip_bird.player_rect.top))
            else:
                screen.blit(leave_alone_text, (flip_bird.player_rect.left + 10, flip_bird.player_rect.top))

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


        button1.draw()
        button2.draw()
        pygame.display.update()






gravity = 0


def second():
    score_rangex = 49
    score_rangey = 51
    score = 0
    pygame.display.set_caption('FLAPPY BIRD')
    print("Main")

    #GAME MUSIC
    game_music.play(-1)


    # INITIALIZE PLAYER RECTANGLES
    player_gameplay_base_rect = player_gameplay_base.get_rect(midleft=(50, 300))

    # GET RANDOM COORDINATE FOR Y AXIS
    rand1 = random.randint(0, 150)
    rand2 = random.randint(0, 150)
    rand3 = random.randint(0, 150)
    rand4 = random.randint(0, 150)
    rand5 = random.randint(0, 150)
    rand6 = random.randint(0, 30)
    rand7 = random.randint(0, 30)
    rand8 = random.randint(0, 30)
    rand9 = random.randint(0, 30)
    rand10 = random.randint(0, 30)

    # INITIALIZE OBSTACLE COORDINATE
    # PIPE FACING DOWN CAN COME DOWN MAX = 215 FROM Y AXIS BEFORE IT ENDS
    # PIPE FACING UP CAN COME UP MAX = 590 BELOW Y AXIS BEFORE IT ENDS

    obs1_up_co = (1650, rand1 + 620 + rand6)
    obs2_up_co = (2150, rand2 + 620 + rand7)
    obs3_up_co = (2650, rand3 + 620 + rand8)
    obs4_up_co = (3150, rand4 + 620 + rand9)
    obs5_up_co = (3650, rand5 + 620 + rand10)

    obs1_down_co = (1650, rand1)
    obs2_down_co = (2150, rand2)
    obs3_down_co = (2650, rand3)
    obs4_down_co = (3150, rand4)
    obs5_down_co = (3650, rand5)

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
                print("EXITING")
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_music.stop()
                    main_menu()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    gravity = -3.8
                    flap.play()
                if event.key == pygame.K_ESCAPE:
                    main_menu()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # event.button = 1 - left , 2-right, 3-middle,  4-wheel up, 5-wheel down
                    gravity = -3.8
                    flap.play()

        if p1.hitbox.colliderect(OB1.hitbox_up) or p1.hitbox.colliderect(OB2.hitbox_up) or p1.hitbox.colliderect(OB3.hitbox_up):
            print("COLLIDE1")
            game_music.stop()
            intermidiate(p1, score)
        if p1.hitbox.colliderect(OB4.hitbox_up) or p1.hitbox.colliderect(OB5.hitbox_up) or p1.hitbox.colliderect(OB6.hitbox_down):
            print("COLLIDE2")
            game_music.stop()
            intermidiate(p1, score)
        if p1.hitbox.colliderect(OB7.hitbox_down) or p1.hitbox.colliderect(OB8.hitbox_down) or p1.hitbox.colliderect(OB9.hitbox_down) or p1.hitbox.colliderect(OB10.hitbox_down):
            print("COLLIDE3")
            game_music.stop()
            intermidiate(p1, score)

        if OB1.hitbox_up.right in range(score_rangex, score_rangey) or OB2.hitbox_up.right in range(score_rangex, score_rangey) or OB3.hitbox_up.right in range(score_rangex, score_rangey) \
                or OB4.hitbox_up.right in range(score_rangex, score_rangey) or OB5.hitbox_up.right in range(score_rangex, score_rangey):
            score += 1
            score_s.play()


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
            OB1.position(OB5.obstacle_rect.right + 500)
        if OB2.check(0):
            OB2.position(OB1.obstacle_rect.right + 500)
        if OB3.check(0):
            OB3.position(OB2.obstacle_rect.right + 500)
        if OB4.check(0):
            OB4.position(OB3.obstacle_rect.right + 500)
        if OB5.check(0):
            OB5.position(OB4.obstacle_rect.right + 500)

        if OB6.check(0):
            OB6.position(OB5.obstacle_rect.right + 500)
        if OB7.check(0):
            OB7.position(OB6.obstacle_rect.right + 500)
        if OB8.check(0):
            OB8.position(OB7.obstacle_rect.right + 500)
        if OB9.check(0):
            OB9.position(OB8.obstacle_rect.right + 500)
        if OB10.check(0):
            OB10.position(OB9.obstacle_rect.right + 500)

        if p1.player_rect.top >= SET_HEIGHT - 130:
            p1.player_rect.bottom = SET_HEIGHT - 130
            game_music.stop()
            intermidiate(p1, score)
        if p1.player_rect.top <= -50:
            p1.player_rect.top = -50
            game_music.stop()
            intermidiate(p1, score)

        score_text = font_menu.render(str(score), True, 'black')

        # pygame.draw.rect(screen, 'black', p1.hitbox, 2)
        # pygame.draw.rect(screen, 'black', OB1.hitbox_up, 2)
        # pygame.draw.rect(screen, 'black', OB2.hitbox_up, 2)
        # pygame.draw.rect(screen, 'black', OB3.hitbox_up, 2)
        # pygame.draw.rect(screen, 'black', OB4.hitbox_up, 2)
        # pygame.draw.rect(screen, 'black', OB5.hitbox_up, 2)
        # pygame.draw.rect(screen, 'black', OB6.hitbox_down, 2)
        # pygame.draw.rect(screen, 'black', OB7.hitbox_down, 2)
        # pygame.draw.rect(screen, 'black', OB8.hitbox_down, 2)
        # pygame.draw.rect(screen, 'black', OB9.hitbox_down, 2)
        # pygame.draw.rect(screen, 'black', OB10.hitbox_down, 2)

        p1.draw()
        screen.blit(score_text, (SET_WIDTH - 50, 15))
        pygame.display.update()


HIGH_SCORE = 0


def intermidiate(p1, score):

    g = 0
    initial_height = p1.player_rect.top
    initial_posx = p1.player_rect.left
    pygame.display.set_caption('BETTER LUCK NEXT TIME')
    touch = 0

    while True:
        screen.fill('black')
        screen.blit(background_play, (0, 0))
        screen.blit(dead_image_up, (p1.player_rect.left + 60, p1.player_rect.top + 10))
        new_height = p1.player_rect.top


        p1.player_rect.left += 2
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("EXITING")
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    main_menu()

        if touch == 0 and new_height == initial_height:
            hit.play()
            die.play()
            g = -2.8
            touch = 1

        p1.move(g)
        g += 0.06

        if new_height >= 1500:
            third(score)
        pygame.display.update()


def third(x):
    global HIGH_SCORE

    exit_screen_sound.play(-1)

    b1 = button('TRY AGAIN', 200, 340, 300, 50)
    b2 = button('MAIN MENU', 880, 340, 300, 50)
    b3 = button('EXIT', 620, 540, 150, 50)

    print('LOOSE')
    pygame.display.set_caption('BETTER LUCK NEXT TIME')



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
                print("EXITING")
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    exit_screen_sound.stop()
                    main_menu()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if b1.check_click():
                    exit_screen_sound.stop()
                    second()
                if b2.check_click():
                    exit_screen_sound.stop()
                    main_menu()
                if b3.check_click():
                    print("EXITING")
                    pygame.quit()
                    sys.exit()

        b1.draw()
        b2.draw()
        b3.draw()
        pygame.display.update()


main_menu()
