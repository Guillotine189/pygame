import sys
import random
import pygame
from pygame import mixer

pygame.init()
pygame.font.init()
mixer.init()

# GAME SOUNDS
menu_sound = mixer.Sound('./sounds/main_menu.ogg')
game_music = mixer.Sound('./sounds/gameplay_sound.ogg')
flap = mixer.Sound('./sounds/flap.wav')
score_s = mixer.Sound('./sounds/point.wav')
die = mixer.Sound('./sounds/diesound.wav')
hit = mixer.Sound('./sounds/hit.wav')
exit_screen_sound = mixer.Sound('./sounds/exit_sound.ogg')
button_sound = mixer.Sound('./sounds/button.wav')
escape_sound = mixer.Sound('./sounds/escape_sound.ogg')

# SET SCREEN
SET_WIDTH = 1400
SET_HEIGHT = 800
screen = pygame.display.set_mode((SET_WIDTH, SET_HEIGHT))


# SET FONTS
font_menu = pygame.font.SysFont('monospace', 50, 30)
bird_font_menu = pygame.font.SysFont('monospace', 30, 20)
pause_font = pygame.font.SysFont('arial.ttf', 120, 20)


# IMAGES PLAYER
player_base_image = pygame.image.load('./images/base_mid.png').convert_alpha()
player_base_image_up = pygame.image.load('./images/base_up.png').convert_alpha()
player_base_image_down = pygame.image.load('./images/base_down.png').convert_alpha()

player_gameplay_base = pygame.image.load('./images/base.png').convert_alpha()
dead_image = pygame.image.load('./images/dead_final_60.png').convert_alpha()
dead_image_up = pygame.image.load('./images/bottom.png').convert_alpha()

player_base_image_flip = pygame.image.load('./images/base_mid_flip.png').convert_alpha()
player_base_image_flip_up = pygame.image.load('./images/base_up_flip.png').convert_alpha()
player_base_image_flip_down = pygame.image.load('./images/base_down_flip.png').convert_alpha()


# BACKGROUND IMAGES
background_menu = pygame.image.load('./images/background_menu_1400x800.png').convert_alpha()
background_play = pygame.image.load('./images/main_1400x800.png').convert_alpha()
base_image = pygame.image.load('./images/base_.png').convert_alpha()
game_over1 = pygame.image.load('./images/game_over1.png').convert_alpha()
game_over2 = pygame.image.load('./images/game_over2.png').convert_alpha()
rip = pygame.image.load('./images/rip.png').convert_alpha()
logo = pygame.image.load('./images/LOGO.png').convert_alpha()

logo_scaled = pygame.transform.scale(logo, (450, 150))


# SCALING IMAGES
X = 120
Y = 80
player_base_image_scaled = pygame.transform.scale(player_base_image, (X, Y))
player_base_image_up_scaled = pygame.transform.scale(player_base_image_up, (X, Y))
player_base_image_down_scaled = pygame.transform.scale(player_base_image_down, (X, Y))

player_base_image_flip_scaled = pygame.transform.scale(player_base_image_flip, (X, Y))
player_base_image_flip_up_scaled = pygame.transform.scale(player_base_image_flip_up, (X, Y))
player_base_image_flip_down_scaled = pygame.transform.scale(player_base_image_flip_down, (X, Y))
dead_image_up_scaled = pygame.transform.scale(dead_image_up, (120, 120))


base_image_scaled = pygame.transform.scale(base_image, (1600, 100))
game_over1_scaled = pygame.transform.scale2x(game_over1)
game_over2_scaled = pygame.transform.scale2x(game_over2)



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


class player(pygame.sprite.Sprite):

    def __init__(self, x, y, img):
        super().__init__()
        self.sprites = []
        self.current_sprite = 0
        self.append(img)
        self.image = self.sprites[self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.hitbox = self.rect


    def update(self):
        self.current_sprite += 1
        if self.current_sprite >= len(self.sprites):
            self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]

    def movex(self, speed):
        self.rect.left += speed

    def movey(self, speed):
        self.rect.top += speed

    def append(self, image):
        self.sprites.append(image)

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
        pygame.draw.rect(screen, 'white', ((self.x, self.y), (self.w, self.h)))
        pygame.draw.line(screen, (200, 190, 140), (self.x, self.y,), (self.x + self.w, self.y), 4)
        pygame.draw.line(screen, (200, 190, 140), (self.x, self.y,), (self.x, self.y + self.h), 4)
        pygame.draw.line(screen, (200, 190, 140), (self.x + self.w, self.y), (self.x + self.w, self.y + self.h), 4)
        pygame.draw.line(screen, (200, 190, 140), (self.x, self.y + self.h), (self.x + self.w, self.y + self.h), 4)
        if self.check_hover():
            pygame.draw.rect(screen, 'dark orange', ((self.x + 8, self.y + 5), (self.w - 14, self.h - 8)), 0, 5)
        else:
            pygame.draw.rect(screen, 'orange', ((self.x + 8, self.y + 5), (self.w - 14, self.h - 8)), 0, 5)
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

    clock = pygame.time.Clock()

    print("MENU")
    menu_text = font_menu.render('MENU', False, 'brown').convert_alpha()
    direction = 'right'

    # RENDERING TEXT
    leave_alone_text = bird_font_menu.render('LEAVE ME ALONE', True, 'black').convert_alpha()
    help_text = bird_font_menu.render('SOMEONE HELP ME!', True, 'black').convert_alpha()
    high_score_text = font_menu.render('HIGH SCORE : ' + str(HIGH_SCORE), True, 'black').convert_alpha()
    high_score_text_rect = high_score_text.get_rect()


    # INITIALIZE BIRD
    bird = player(50, 300, player_base_image_scaled)
    flip_bird = player(750, 300, player_base_image_flip_scaled)

    # ADDING SPRITES
    ### BIRD
    bird.append(player_base_image_down_scaled)
    bird.append(player_base_image_scaled)
    bird.append(player_base_image_up_scaled)
    ### FLIP BIRD
    flip_bird.append(player_base_image_flip_down_scaled)
    flip_bird.append(player_base_image_flip_scaled)
    flip_bird.append(player_base_image_flip_up_scaled)

    # MAKING SPRITE GROUP
    animate_bird = pygame.sprite.Group()
    animate_flip_bird = pygame.sprite.Group()

    # ADDING PLAYER TO GROUP
    animate_bird.add(bird)
    animate_flip_bird.add(flip_bird)

    while True:

        # FILL SCREEN
        screen.fill('black')

        # SCREEN MENU
        screen.blit(background_menu, (0, 0))
        screen.blit(menu_text, (900, 300))
        pygame.draw.rect(screen, 'black', (895, 305, 132, 40), 1)  # rectangle around menu
        screen.blit(logo_scaled, (750, 100))

        # pygame.draw.line(screen, 'black', (900, 345), (1017, 345), 2)

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
                    gameplay_screne()
                if event.key == pygame.K_ESCAPE:
                    print("EXITING")
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button1.check_click():
                    menu_sound.stop()
                    gameplay_screne()
                if button2.check_click():
                    print("EXITING")
                    pygame.quit()
                    sys.exit()

        # MOUSE ON BIRD
        if bird.rect.collidepoint(m_pos) and direction == 'right':
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                bird.movey(-80)
                screen.blit(help_text, (bird.rect.left - 40, bird.rect.top - 40))
            else:
                screen.blit(leave_alone_text, (bird.rect.left - 40, bird.rect.top - 40))

        if flip_bird.rect.collidepoint(m_pos) and direction == 'left':
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                flip_bird.movey(80)
                screen.blit(help_text, (flip_bird.rect.left - 40, flip_bird.rect.top - 40))
            else:
                screen.blit(leave_alone_text, (flip_bird.rect.left - 40, flip_bird.rect.top - 40))

        # MOVING BIRD L->R and R->L
        if direction == 'right' and bird.rect.left <= 600:
            bird.movex(6)
            animate_bird.draw(screen)
            animate_bird.update()
        if direction == 'right' and bird.rect.right > 600:
            direction = 'left'
            flip_bird.rect.top = bird.rect.top
            flip_bird.rect.right = 600
            animate_flip_bird.draw(screen)
            animate_flip_bird.update()
        if direction == 'left' and flip_bird.rect.left > 50:
            flip_bird.movex(-6)
            animate_flip_bird.draw(screen)
            animate_flip_bird.update()
        if direction == 'left' and flip_bird.rect.left <= 50:
            direction = 'right'
            bird.rect.top = flip_bird.rect.top
            bird.rect.left = 50
            animate_bird.draw(screen)
            animate_bird.update()


        bird.rect.bottom = 300
        flip_bird.rect = bird.rect



        button1.draw()
        button2.draw()
        high_score_text_rect.right = 1200
        high_score_text_rect.bottom = 570
        screen.blit(high_score_text, high_score_text_rect)
        pygame.display.update()
        clock.tick(30)


gravity = 0

def gameplay_screne():
    clock = pygame.time.Clock()
    score_rangex = 49
    score_rangey = 51
    score = 0
    pygame.display.set_caption('FLAPPY BIRD')
    print("Main")

    #GAME MUSIC
    game_music.play(-1)


    # GET RANDOM COORDINATE FOR Y AXIS
    rand1 = random.randint(100, 200)
    rand2 = random.randint(100, 200)
    rand3 = random.randint(100, 200)
    rand4 = random.randint(100, 200)
    rand5 = random.randint(100, 200)
    rand6 = random.randint(0, 100)
    rand7 = random.randint(0, 100)
    rand8 = random.randint(0, 100)
    rand9 = random.randint(0, 100)
    rand10 = random.randint(0, 100)

    # INITIALIZE OBSTACLE COORDINATE
    # PIPE FACING DOWN CAN COME DOWN MAX = 215 FROM Y AXIS BEFORE IT ENDS
    # PIPE FACING UP CAN COME UP MAX = 590 BELOW Y AXIS BEFORE IT ENDS

    obs1_up_co = (1650, rand1 + 550)
    obs2_up_co = (2150, rand2 + 550)
    obs3_up_co = (2650, rand3 + 550)
    obs4_up_co = (3150,  rand4 + 550)
    obs5_up_co = (3650, rand5 + 550)

    obs1_down_co = (1650, rand1 - 1.5*rand6)
    obs2_down_co = (2150, rand2 - 1.5*rand7)
    obs3_down_co = (2650, rand3 - 1.5*rand8)
    obs4_down_co = (3150, rand4 - 1.5*rand9)
    obs5_down_co = (3650, rand5 - 1.5*rand10)

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

    # PLAYER
    p1 = player(50, 300, player_base_image_scaled)

    # ADDING SPRITE TO GROUP
    p1.append(player_base_image_down_scaled)
    p1.append(player_base_image_scaled)
    p1.append(player_base_image_up_scaled)

    # MAKING SPRITE GROUP
    animate_player = pygame.sprite.Group()

    # ADDING PLAYER TO SPRITE GROUP
    animate_player.add(p1)

    # BUTTONS
    pause_button = button('PAUSE', 50, 50, 180, 50)

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



        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("EXITING")
                pygame.quit()
                sys.exit()


            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    gravity = -2.8
                    flap.play()
                if event.key == pygame.K_ESCAPE:
                    state = True
                    while state:
                        animate_player.draw(screen)
                        pause(score)
                        state = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # event.button = 1 - left , 2-right, 3-middle,  4-wheel up, 5-wheel down
                    gravity = -2.8
                    flap.play()
                if pause_button.check_click():
                    animate_player.draw(screen)
                    run = True
                    while run:
                        pause(score)
                        run = False

        if p1.hitbox.colliderect(OB1.hitbox_up) or p1.hitbox.colliderect(OB2.hitbox_up) or p1.hitbox.colliderect(OB3.hitbox_up):
            print("COLLIDE1")
            game_music.stop()
            intermediate(p1, score)
        if p1.hitbox.colliderect(OB4.hitbox_up) or p1.hitbox.colliderect(OB5.hitbox_up) or p1.hitbox.colliderect(OB6.hitbox_down):
            print("COLLIDE2")
            game_music.stop()
            intermediate(p1, score)
        if p1.hitbox.colliderect(OB7.hitbox_down) or p1.hitbox.colliderect(OB8.hitbox_down) or p1.hitbox.colliderect(OB9.hitbox_down) or p1.hitbox.colliderect(OB10.hitbox_down):
            print("COLLIDE3")
            game_music.stop()
            intermediate(p1, score)

        if OB1.hitbox_up.right in range(score_rangex, score_rangey) or OB2.hitbox_up.right in range(score_rangex, score_rangey) or OB3.hitbox_up.right in range(score_rangex, score_rangey) \
                or OB4.hitbox_up.right in range(score_rangex, score_rangey) or OB5.hitbox_up.right in range(score_rangex, score_rangey):
            score += 1
            score_s.play()


        gravity += 0.08
        p1.movey(gravity)

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

        if p1.rect.top >= SET_HEIGHT - 130:
            p1.rect.bottom = SET_HEIGHT - 130
            game_music.stop()
            intermediate(p1, score)
        if p1.rect.top <= 0:
            p1.rect.top = 0
            game_music.stop()
            intermediate(p1, score)

        score_text = font_menu.render(str(score), True, 'black')
        score_text_rect = score_text.get_rect()
        score_text_rect.right = SET_WIDTH-50
        score_text_rect.top = 15

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

        animate_player.draw(screen)
        animate_player.update()
        screen.blit(score_text, (score_text_rect.left, score_text_rect.top))
        screen.blit(base_image_scaled, (0, 750))
        pause_button.draw()
        pygame.display.update()
        clock.tick(150)

def pause(score):

    escape_sound.play()
    print('PAUSE')
    run = True
    largetext = pause_font.render('PAUSED', True, 'black')
    screen.blit(largetext, (500, 200))
    score_text = font_menu.render('SCORE : ' + str(score), True, 'black')
    score_text_rect = score_text.get_rect()
    score_text_rect.center = (670, 350)
    con_but = button('CONTINUE', 200, 540, 275, 50)
    menu_but = button('MAIN MENU', 880, 540, 300, 50)

    while run:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("EXITING")
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if con_but.check_click():
                    run = False
                if menu_but.check_click():
                    game_music.stop()
                    main_menu()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    escape_sound.play()
                    run = False

        con_but.draw()
        menu_but.draw()
        screen.blit(base_image_scaled, (0, 750))
        screen.blit(score_text, score_text_rect)
        pygame.display.update()

    print("Main")


HIGH_SCORE = 0


def intermediate(p1, score):

    g = 0
    initial_height = p1.rect.top
    pygame.display.set_caption('BETTER LUCK NEXT TIME')
    touch = 0

    while True:

        screen.blit(background_play, (0, 0))
        screen.blit(base_image_scaled, (0, 750))
        screen.blit(dead_image_up_scaled, (p1.rect.left + 60, p1.rect.top + 10))
        new_height = p1.rect.top


        p1.rect.left += 2
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

        p1.movey(g)
        g += 0.06

        if new_height >= 1500:
            exit_screen(score)
        pygame.display.update()


def exit_screen(x):
    global HIGH_SCORE

    exit_screen_sound.play(-1)

    b1 = button('TRY AGAIN', 200, 340, 300, 50)
    b2 = button('MAIN MENU', 880, 340, 300, 50)
    b3 = button('EXIT', 1220, 700, 150, 50)

    print('LOOSE')
    pygame.display.set_caption('BETTER LUCK NEXT TIME')


    if x > HIGH_SCORE:
        score = font_menu.render("NEW HIGH SCORE : " + str(x), 1, (0, 0, 0))
        HIGH_SCORE = x
    else:
        score = font_menu.render("SCORE :  " + str(x), 1, (0, 0, 0))

    while True:

        screen.fill('black')
        screen.blit(background_play, (0, 0))
        score_rect = score.get_rect()
        score_rect.center = (700, 250)
        screen.blit(score, score_rect)
        screen.blit(rip, (500, 420))
        screen.blit(game_over1_scaled, (380, -190))
        screen.blit(game_over2_scaled, (400, -190))

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
                    gameplay_screne()
                if b2.check_click():
                    exit_screen_sound.stop()
                    main_menu()
                if b3.check_click():
                    print("EXITING")
                    pygame.quit()
                    sys.exit()
        screen.blit(base_image_scaled, (0, 750))
        b1.draw()
        b2.draw()
        b3.draw()
        pygame.display.update()


main_menu()
