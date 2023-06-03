import os
import sys
import random
import pygame
from pygame import mixer
import socket


pygame.init()
pygame.font.init()
mixer.init()

path = os.getcwd()
fpath = path
# GAME SOUNDS
pygame.mixer.music.load(os.path.join(path, '../sounds/main_menu.ogg'))

# os.path.join(path, '../sounds/
 
game_music = mixer.Sound(os.path.join(path, '../sounds/gameplay_sound.ogg'))
flap = mixer.Sound(os.path.join(path, '../sounds/flap.wav'))
score_s = mixer.Sound(os.path.join(path, '../sounds/point.wav'))
die = mixer.Sound(os.path.join(path, '../sounds/diesound.wav'))
hit = mixer.Sound(os.path.join(path, '../sounds/hit.wav'))
exit_screen_sound = mixer.Sound(os.path.join(path, '../sounds/exit_sound.ogg'))
button_sound = mixer.Sound(os.path.join(path, '../sounds/button.wav'))
escape_sound = mixer.Sound(os.path.join(path, '../sounds/escape_sound.ogg'))



# SET SCREEN
SET_WIDTH = 1400
SET_HEIGHT = 800
screen = pygame.display.set_mode((SET_WIDTH, SET_HEIGHT))


# SET FONTS
font_menu = pygame.font.SysFont('monospace', 50, 30)
bird_font_menu = pygame.font.SysFont('monospace', 30, 20)
pause_font = pygame.font.SysFont('arial.ttf', 120, 20)


# IMAGES PLAYER

# os.path.join(path, '../images/

player_base_image = pygame.image.load(os.path.join(path, '../images/base_mid.png')).convert_alpha()
player_base_image_up = pygame.image.load(os.path.join(path, '../images/base_up.png')).convert_alpha()
player_base_image_down = pygame.image.load(os.path.join(path, '../images/base_down.png')).convert_alpha()
player_gameplay_base = pygame.image.load(os.path.join(path, '../images/base.png')).convert_alpha()
dead_image = pygame.image.load(os.path.join(path, '../images/dead_final_60.png')).convert_alpha()
dead_image_up = pygame.image.load(os.path.join(path, '../images/bottom.png')).convert_alpha()
player_base_image_flip = pygame.image.load(os.path.join(path, '../images/base_mid_flip.png')).convert_alpha()
player_base_image_flip_up = pygame.image.load(os.path.join(path, '../images/base_up_flip.png')).convert_alpha()
player_base_image_flip_down = pygame.image.load(os.path.join(path, '../images/base_down_flip.png')).convert_alpha()


p2_up = pygame.image.load(os.path.join(path, '../images/bluebird-upflap.png')).convert_alpha()
p2_mid = pygame.image.load(os.path.join(path, '../images/bluebird-midflap.png')).convert_alpha()
p2_down = pygame.image.load(os.path.join(path, '../images/bluebird-downflap.png')).convert_alpha()


# BACKGROUND IMAGES
background_menu = pygame.image.load(os.path.join(path, '../images/background_menu_1400x800.png')).convert_alpha()
background_play = pygame.image.load(os.path.join(path, '../images/main_1400x800.png')).convert_alpha()
base_image = pygame.image.load(os.path.join(path, '../images/base_.png')).convert_alpha()
game_over1 = pygame.image.load(os.path.join(path, '../images/game_over1.png')).convert_alpha()
game_over2 = pygame.image.load(os.path.join(path, '../images/game_over2.png')).convert_alpha()
rip = pygame.image.load(os.path.join(path, '../images/rip.png')).convert_alpha()
logo = pygame.image.load(os.path.join(path, '../images/LOGO.png')).convert_alpha()
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

p2_mid_scaled = pygame.transform.scale(p2_mid, (X, Y))
p2_down_scaled = pygame.transform.scale(p2_down, (X, Y))
p2_up_scaled = pygame.transform.scale(p2_up, (X, Y))


base_image_scaled = pygame.transform.scale(base_image, (1600, 100))
game_over1_scaled = pygame.transform.scale2x(game_over1)
game_over2_scaled = pygame.transform.scale2x(game_over2)



# OBSTACLE IMAGES
obs_down1 = pygame.image.load(os.path.join(path, '../images/tube_down.png')).convert_alpha()
obs_up1 = pygame.image.load(os.path.join(path, '../images/tube_up.png')).convert_alpha()
obs_down2 = pygame.image.load(os.path.join(path, '../images/tube_down.png')).convert_alpha()
obs_up2 = pygame.image.load(os.path.join(path, '../images/tube_up.png')).convert_alpha()
obs_down3 = pygame.image.load(os.path.join(path, '../images/tube_down.png')).convert_alpha()
obs_up3 = pygame.image.load(os.path.join(path, '../images/tube_up.png')).convert_alpha()
obs_down4 = pygame.image.load(os.path.join(path, '../images/tube_down.png')).convert_alpha()
obs_up4 = pygame.image.load(os.path.join(path, '../images/tube_up.png')).convert_alpha()
obs_down5 = pygame.image.load(os.path.join(path, '../images/tube_down.png')).convert_alpha()
obs_up5 = pygame.image.load(os.path.join(path, '../images/tube_up.png')).convert_alpha()





gravity = 0
HIGH_SCORE = 0
online_score = 0



class Network:

    def __init__(self):
        self.host = '10.0.0.238'
        self.port = 9901
        self.format = 'utf-8'
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.status = False
        self.first_message = self.connect()


    def connect(self):
        try:
            self.client.connect((self.host, self.port))
            message = self.client.recv(2048).decode(self.format)
            if message != '0':
                self.status = True
                return message
            else:
                return 0
        except:
            print("ERROR IN INITIAL CONNECTION")
            return 0


    def close(self):
        try:
            self.client.send("!D".encode(self.format))
            self.client.close()
            self.status = False
            print("DISCONNECTED")
        except:
            print("SERVER DOWN")
            self.status = False
    def close_all(self):
        try:
            self.client.send("!SD".encode(self.format))
            self.client.close()
            self.status = False
            print("DISCONNECTED")
        except:
            print("SERVER DOWN")
            self.status = False

    def send(self, msg):
        try:
            self.client.send(msg.encode(self.format))
            return self.client.recv(4096).decode(self.format)
        except:
            print("ERROR IN FUNCTION 'Send' ")
            self.status = False








class player(pygame.sprite.Sprite):

    def __init__(self, x, y, img):
        super().__init__()
        self.x = x
        self.y = y
        self.sprites = []
        self.current_sprite = 0
        self.append(img)
        self.image = self.sprites[self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)
        self.hitbox = self.rect
        self.is_animating = False
    #
    # def update_once(self):
    #     if self.is_animating:
    #         self.current_sprite += 0.8
    #         if self.current_sprite == len(self.sprites):
    #             self.current_sprite = 0
    #             self.is_animating = False
    #         self.image = self.sprites[int(self.current_sprite)]

    def update(self, input):
        if input:
            self.current_sprite += 0.6
            if self.current_sprite >= len(self.sprites):
                self.current_sprite = 0
            self.image = self.sprites[int(self.current_sprite)]
        else:
            if self.is_animating:
                self.current_sprite += 0.4
                if self.current_sprite >= len(self.sprites):
                    self.current_sprite = 0
                    self.is_animating = False
                self.image = self.sprites[int(self.current_sprite)]

    def movex(self, speed):
        self.rect.left += speed

    def movey(self, speed):
        self.rect.top += speed

    def append(self, image):
        self.sprites.append(image)

    def animate(self):
        self.is_animating = True


class tube:

    def __init__(self, obstacle, obstacle_rect):
        self.obstacle = obstacle
        self.obstacle_rect = obstacle_rect
        self.hitbox_up = pygame.rect.Rect(self.obstacle_rect.left + 60, self.obstacle_rect.top + 30, 110, 1000) # top left, top right, width, height
        self.hitbox_down = pygame.rect.Rect(self.obstacle_rect.left + 60, self.obstacle_rect.top + 5, 110, 418)
        self.draw()

    def draw(self):
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
        #
        # pygame.draw.rect(screen, 'white', ((self.x, self.y), (self.w, self.h)))
        # pygame.draw.line(screen, (200, 190, 140), (self.x, self.y,), (self.x + self.w, self.y), 4)
        # pygame.draw.line(screen, (200, 190, 140), (self.x, self.y,), (self.x, self.y + self.h), 4)
        # pygame.draw.line(screen, (200, 190, 140), (self.x + self.w, self.y), (self.x + self.w, self.y + self.h), 4)
        # pygame.draw.line(screen, (200, 190, 140), (self.x, self.y + self.h), (self.x + self.w, self.y + self.h), 4)
        if self.check_hover():
            pygame.draw.rect(screen, 'white', ((self.x, self.y - 10), (self.w, self.h)))
            pygame.draw.line(screen, (200, 190, 140), (self.x, self.y - 10,), (self.x + self.w, self.y - 10), 4)
            pygame.draw.line(screen, (200, 190, 140), (self.x, self.y - 10,), (self.x, self.y - 10+ self.h), 4)
            pygame.draw.line(screen, (200, 190, 140), (self.x + self.w, self.y - 10), (self.x + self.w, self.y - 10 + self.h), 4)
            pygame.draw.line(screen, (200, 190, 140), (self.x, self.y - 10 + self.h), (self.x + self.w, self.y - 10 + self.h), 4)
            pygame.draw.rect(screen, 'dark orange', ((self.x + 8, self.y - 10 + 5), (self.w - 14, self.h - 8)), 0, 5)
            screen.blit(button_text, (self.x + 15, self.y - 10))
        else:
            pygame.draw.rect(screen, 'white', ((self.x, self.y), (self.w, self.h)))
            pygame.draw.line(screen, (200, 190, 140), (self.x, self.y,), (self.x + self.w, self.y), 4)
            pygame.draw.line(screen, (200, 190, 140), (self.x, self.y,), (self.x, self.y + self.h), 4)
            pygame.draw.line(screen, (200, 190, 140), (self.x + self.w, self.y), (self.x + self.w, self.y + self.h), 4)
            pygame.draw.line(screen, (200, 190, 140), (self.x, self.y + self.h), (self.x + self.w, self.y + self.h), 4)
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


def main_menu(x):

    # INITIALIZE PLAYER RECTANGLES
    player_base_image_rect = player_base_image.get_rect(midleft=(50, 300))
    player_base_image_flip_rect = player_base_image_flip.get_rect(midright=(750, 300))

    pygame.display.set_caption('MENU')

    # PLAY SOUND
    if x:
        pygame.mixer.music.play(-1)

    clock = pygame.time.Clock()

    print("MENU")
    menu_text = font_menu.render('MENU', False, 'brown').convert_alpha()
    direction = 'right'

    # RENDERING TEXT
    leave_alone_text = bird_font_menu.render('LEAVE ME ALONE', True, 'black').convert_alpha()
    help_text = bird_font_menu.render('SOMEONE HELP ME!', True, 'black').convert_alpha()
    aggh_text = bird_font_menu.render('AGGHH!!', True, 'black').convert_alpha()
    curse_text = bird_font_menu.render('#@$%@#!', True, 'black').convert_alpha()
    play_game_text = bird_font_menu.render('JUST PLAY THE GAME', True, 'black').convert_alpha()
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

    time = 0
    pressed_bird = 0
    timer_for_just_play_text = 0


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
        button3 = button("CONTROLS", 840, 500, 275, 50)

        # mouse
        m_pos = pygame.mouse.get_pos()


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("EXITING")
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    print("EXITING")
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button1.check_click():
                    choosing_screne()
                if button2.check_click():
                    print("EXITING")
                    pygame.quit()
                    sys.exit()
                if button3.check_click():
                    pygame.mixer.music.pause()
                    controls()

        # MOUSE ON BIRD
        if bird.rect.collidepoint(m_pos) and direction == 'right':
            time += 0.04
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                bird.movey(-80)
                bird.movex(2)
                pressed_bird += 1
                screen.blit(help_text, (bird.rect.left - 40, bird.rect.top - 40))
            else:
                if time < 3:
                    screen.blit(leave_alone_text, (bird.rect.left - 40, bird.rect.top - 40))
                elif time > 3 and time < 6:
                    screen.blit(aggh_text, (bird.rect.left + 15, bird.rect.top - 40))
                else:
                    screen.blit(curse_text, (bird.rect.left + 15, bird.rect.top - 40))
        elif flip_bird.rect.collidepoint(m_pos) and direction == 'left':
            time += 0.04
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                flip_bird.movey(80)
                bird.movex(-2)
                screen.blit(help_text, (flip_bird.rect.left - 40, flip_bird.rect.top - 40))
            else:
                if time < 3:
                    screen.blit(leave_alone_text, (flip_bird.rect.left - 40, flip_bird.rect.top - 40))
                elif time >3 and time < 6:
                    screen.blit(aggh_text, (flip_bird.rect.left + 15, flip_bird.rect.top - 40))
                else:
                    screen.blit(curse_text, (flip_bird.rect.left + 15, flip_bird.rect.top - 40))
        else:
            time = 0

        if pressed_bird > 6:
            screen.blit(play_game_text, (150, 50))
            timer_for_just_play_text += 0.1
            if timer_for_just_play_text >= 5:
                pressed_bird = 0
                timer_for_just_play_text = 0


        # MOVING BIRD L->R and R->L
        if direction == 'right' and bird.rect.left <= 600:
            bird.movex(6)
            animate_bird.draw(screen)
            animate_bird.update(1)
        if direction == 'right' and bird.rect.right > 600:
            direction = 'left'
            flip_bird.rect.top = bird.rect.top
            flip_bird.rect.right = 600
            animate_flip_bird.draw(screen)
            animate_flip_bird.update(1)
        if direction == 'left' and flip_bird.rect.left > 50:
            flip_bird.movex(-6)
            animate_flip_bird.draw(screen)
            animate_flip_bird.update(1)
        if direction == 'left' and flip_bird.rect.left <= 50:
            direction = 'right'
            bird.rect.top = flip_bird.rect.top
            bird.rect.left = 50
            animate_bird.draw(screen)
            animate_bird.update(1)


        bird.rect.bottom = 300
        flip_bird.rect = bird.rect



        button1.draw()
        button2.draw()
        button3.draw()
        high_score_text_rect.right = 1200
        high_score_text_rect.bottom = 630
        screen.blit(high_score_text, high_score_text_rect)
        pygame.display.update()
        clock.tick(30)






def choosing_screne():
    pygame.display.set_caption('CHOOSE MODE')
    print("CHOOSING SCRENE")

    online_button = button("ONLINE", 280, SET_HEIGHT/2 + 50, 210, 50)
    offline_button = button("OFFLINE", 900, SET_HEIGHT/2 - 100, 250, 50)
    menu_button = button('MAIN MENU', SET_WIDTH - 320, 20, 300, 50)

    size1 = 15, 800
    my_surface1 = pygame.Surface(size1)
    my_surface1.set_alpha(150)
    # my_surface1 = pygame.transform.rotate(my_surface1, 45)
    my_surface1.fill((255, 200, 0))
    size2 = 15, 800
    my_surface2 = pygame.Surface(size2)
    my_surface2.set_alpha(100)
    # my_surface2 = pygame.transform.rotate(my_surface2, 45)
    my_surface2.fill((0, 200, 255))

    size3 = 1400, 15
    my_surface3 = pygame.Surface(size3)
    my_surface3.set_alpha(150)
    # my_surface3 = pygame.transform.rotate(my_surface1, 45)
    my_surface3.fill((255, 200, 0))
    size4 = 1400, 15
    my_surface4 = pygame.Surface(size4)
    my_surface4.set_alpha(100)
    # my_surface4 = pygame.transform.rotate(my_surface2, 45)
    my_surface4.fill((0, 200, 255))




    while True:
        screen.fill('black')
        screen.blit(background_menu, (0, 0))

        # pygame.draw.polygon(screen, (255, 0, 0), ((0, 0), (0, SET_HEIGHT), (SET_WIDTH, SET_HEIGHT)), 0)
        # pygame.draw.polygon(screen, (255, 0, 0), ((150, 700), (100, 650), (50, 700)), 0)
        # pygame.draw.polygon(screen, (56, 135, 198), ((0, 0), (SET_WIDTH, 0), (SET_WIDTH, SET_HEIGHT)), 0)
        # pygame.draw.polygon(screen, (0, 0, 255), ((150, 700), (100, 750), (50, 700)), 0)
        #
        # pygame.draw.circle(screen, (255, 0, 0), (605, SET_HEIGHT/2 + 70), 107, 60)
        # pygame.draw.circle(screen, (0, 0, 255), (735, SET_HEIGHT/2 - 100), 107, 60)
        # draw_circle_alpha(screen, (255, 0, 0, 0), (400, SET_HEIGHT/2 + 50), 50)

        screen.blit(my_surface1, (0, 0))
        screen.blit(my_surface2, (0, 0))

        screen.blit(my_surface3, (0, 0))
        screen.blit(my_surface4, (0, 0))

        screen.blit(my_surface1, (1385, 0))
        screen.blit(my_surface2, (1385, 0))

        screen.blit(my_surface3, (0, 785))
        screen.blit(my_surface4, (0, 785))

        pygame.draw.line(screen, (100, 100, 40), (0, 0), (SET_WIDTH, SET_HEIGHT), 4)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    main_menu(0)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if menu_button.check_click():
                    main_menu(0)
                if online_button.check_click():
                    waiting_screne()
                if offline_button.check_click():
                    pygame.mixer.music.stop()
                    gameplay_offline_screne()

        screen.blit(p2_up_scaled, (60, 220))
        screen.blit(player_base_image_flip_scaled, (640, 570))
        screen.blit(player_base_image_down_scaled, (700, 100))
        menu_button.draw()
        online_button.draw()
        offline_button.draw()
        pygame.display.update()






def controls():
    pygame.display.set_caption('CONTROLS')
    print('CONTROLS')
    pygame.mixer.music.unpause()
    screen.fill('black')
    screen.blit(background_menu, (0, 0))
    text1 = font_menu.render("CONTROLS", True, (0, 0, 0))
    text2 = font_menu.render("LEFT CLICK OR PRESS SPACE BAR TO FLY", True, (0, 0, 0))
    text3 = font_menu.render("PRESS ESCAPE TO GO BACK ", True, (0, 0, 0))

    B1 = button("GO BACK", 595, 450, 250, 50)

    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print('EXITING')
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.mixer.pause()
                    main_menu(0)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if B1.check_click():
                    main_menu(0)


        screen.blit(text1, (580, 230))
        screen.blit(text2, (150, 300))
        screen.blit(text3, (360, 370))

        B1.draw()
        pygame.display.update()




def waiting_screne():
    print("WAITING SCRENE")

    Player = Network()
    if Player.status:
        pygame.display.set_caption('WAITING..')
    menu_button = button('MAIN MENU', SET_WIDTH - 320, 20, 300, 50)

    while Player.status:

        status = Player.send('con_stat')
        screen.fill('black')
        screen.blit(background_play, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if menu_button.check_click():
                    Player.client.send("!D".encode(Player.format))
                    main_menu(0)

        tex = font_menu.render('WAITING FOR PLAYER..', True, 'black').convert_alpha()

        screen.blit(tex, (SET_WIDTH/2 - 300, SET_HEIGHT/2))

        if int(status):
            pygame.mixer.music.stop()
            gameplay_screne(Player)

        menu_button.draw()
        pygame.display.update()







def read_obs_co(msg):
    message = msg.split(',')
    return float(message[0]), float(message[1])

def make(tup):
    message = str(tup[0]) + ',' + str(tup[1])
    return  message


0

def gameplay_screne(Player):
    alive = 1
    won = 0

    if Player.first_message == 0:
        main_menu(1)


    else:
        print(Player.first_message)
        print("SENDING INIT POS")
        tp = Player.send('INIT_POS')
        tp = Player.send('50,300')




        clock = pygame.time.Clock()
        score_rangex = 48
        score_rangey = 52
        score = 0
        pygame.display.set_caption('FLAPPY BIRD')
        print("Main")

        #GAME MUSIC
        game_music.play(-1)


        OBS_CO = []

        print("SENDING")
        Player.client.send('OBS_INIT'.encode(Player.format))
        # OBS_CO[0] = read_obs_co(ttmp)
        print("SENT")
        for j in range(0, 10):
            temp = Player.client.recv(1024).decode(Player.format)
            Player.client.send('?'.encode(Player.format))
            print(temp)
            OBS_CO.append(read_obs_co(temp))


        # INITIALIZE OBSTACLE RECTANGLE
        obs_up1_rect = obs_up1.get_rect(midright=OBS_CO[0])
        obs_up2_rect = obs_up2.get_rect(midright=OBS_CO[1])
        obs_up3_rect = obs_up3.get_rect(midright=OBS_CO[2])
        obs_up4_rect = obs_up4.get_rect(midright=OBS_CO[3])
        obs_up5_rect = obs_up5.get_rect(midright=OBS_CO[4])
        obs_down1_rect = obs_down1.get_rect(midright=OBS_CO[5])
        obs_down2_rect = obs_down1.get_rect(midright=OBS_CO[6])
        obs_down3_rect = obs_down1.get_rect(midright=OBS_CO[7])
        obs_down4_rect = obs_down1.get_rect(midright=OBS_CO[8])
        obs_down5_rect = obs_down1.get_rect(midright=OBS_CO[9])




        global gravity, online_score

        online_score = 0
        gravity = 0
        tubespeed = -5

        # PLAYER
        p1 = player(50, 300, player_base_image_scaled)
        p2 = player(50, 300, p2_mid_scaled)

        # ADDING SPRITE TO GROUP
        p1.append(player_base_image_down_scaled)
        p1.append(player_base_image_scaled)
        p1.append(player_base_image_up_scaled)

        p2.append(p2_down_scaled)
        p2.append(p2_mid_scaled)
        p2.append(p2_up_scaled)

        # MAKING SPRITE GROUP
        animate_player = pygame.sprite.Group()
        animate_player_2 = pygame.sprite.Group()

        # ADDING PLAYER TO SPRITE GROUP
        animate_player.add(p1)
        animate_player_2.add(p2)


    while Player.status:

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


        position = Player.send('POSITION?')
        my_pos = p1.rect.center
        pp = Player.send(make(my_pos))
        pos = read_obs_co(pp)
        p2.rect.center = int(pos[0]), int(pos[1])
        p2.animate()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("EXITING")
                pygame.quit()
                sys.exit()


            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    gravity = -5.8
                    p1.animate()
                    flap.play()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # event.button = 1 - left , 2-right, 3-middle,  4-wheel up, 5-wheel down
                    gravity = -5.8
                    p1.animate()
                    flap.play()


        if p1.hitbox.colliderect(OB1.hitbox_up) or p1.hitbox.colliderect(OB2.hitbox_up) or p1.hitbox.colliderect(OB3.hitbox_up):
            print("COLLIDE1")
            game_music.stop()
            alive = Player.send('dead')
        if p1.hitbox.colliderect(OB4.hitbox_up) or p1.hitbox.colliderect(OB5.hitbox_up) or p1.hitbox.colliderect(OB6.hitbox_down):
            print("COLLIDE2")
            game_music.stop()
            alive = Player.send('dead')
        if p1.hitbox.colliderect(OB7.hitbox_down) or p1.hitbox.colliderect(OB8.hitbox_down) or p1.hitbox.colliderect(OB9.hitbox_down) or p1.hitbox.colliderect(OB10.hitbox_down):
            print("COLLIDE3")
            game_music.stop()
            alive = Player.send('dead')

        if OB1.hitbox_up.right in range(score_rangex, score_rangey) or OB2.hitbox_up.right in range(score_rangex, score_rangey) or OB3.hitbox_up.right in range(score_rangex, score_rangey) \
                or OB4.hitbox_up.right in range(score_rangex, score_rangey) or OB5.hitbox_up.right in range(score_rangex, score_rangey):
            online_score += 1
            score_s.play()

        gravity += 0.4
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


        #
        # OB1.hitbox_up.right = OB1.hitbox_up.right - tubespeed
        # OB2.hitbox_up.right = OB2.hitbox_up.right - tubespeed
        # OB3.hitbox_up.right = OB3.hitbox_up.right - tubespeed
        # OB4.hitbox_up.right = OB4.hitbox_up.right - tubespeed
        # OB5.hitbox_up.right = OB5.hitbox_up.right - tubespeed
        # OB6.hitbox_down.right = OB6.hitbox_down.right - tubespeed
        # OB7.hitbox_down.right = OB7.hitbox_down.right - tubespeed
        # OB8.hitbox_down.right = OB8.hitbox_down.right - tubespeed
        # OB9.hitbox_down.right = OB9.hitbox_down.right - tubespeed
        # OB10.hitbox_down.right = OB10.hitbox_down.right - tubespeed

        if OB1.check(0):
            req2 = Player.send('OBS_1')
            print(f"UP CO REC {req2}")
            obs_down1_rect.bottom = int(req2)
            req3 = Player.send('OBS_2')
            print(f"DOWN CO REC {req3}")
            obs_up1_rect.top = int(req3)
            req = Player.send('OP')
            pos = Player.send(f'{OB5.obstacle_rect.right}')
            print(f"OBS POS REC - {int(pos)}")
            OB1.position(int(pos))
            OB6.position(int(pos))


        if OB2.check(0):
            req2 = Player.send('OBS_1')
            print(f"UP CO REC {req2}")
            obs_down2_rect.bottom = int(req2)
            req2 = Player.send('OBS_2')
            obs_up2_rect.top = int(req2)
            print(f"DOWN CO REC {req2}")
            req = Player.send('OP')
            pos = Player.send(f'{OB1.obstacle_rect.right}')
            OB2.position(int(pos))
            OB7.position(int(pos))
            print(f"OBS POS REC - {int(pos)}")

        if OB3.check(0):
            req2 = Player.send('OBS_1')
            print(f"UP CO REC {req2}")
            obs_down3_rect.bottom = int(req2)
            req2 = Player.send('OBS_2')
            print(f"DOwn CO REC {req2}")
            obs_up3_rect.top = int(req2)
            req = Player.send('OP')
            pos = Player.send(f'{OB2.obstacle_rect.right}')
            OB3.position(int(pos))
            OB8.position(int(pos))
            print(f"OBS POS REC - {int(pos)}")

        if OB4.check(0):
            req2 = Player.send('OBS_1')
            print(f"UP CO REC {req2}")
            obs_down4_rect.bottom = int(req2)
            req2 = Player.send('OBS_2')
            print(f"down CO REC {req2}")
            obs_up4_rect.top = int(req2)
            req = Player.send('OP')
            pos = Player.send(f'{OB3.obstacle_rect.right}')
            OB4.position(int(pos))
            OB9.position(int(pos))
            print(f"OBS POS REC - {int(pos)}")

        if OB5.check(0):
            req2 = Player.send('OBS_1')
            print(f"UP CO REC {req2}")
            obs_down5_rect.bottom = int(req2)
            req2 = Player.send('OBS_2')
            print(f"down CO REC {req2}")
            obs_up5_rect.top = int(req2)
            req = Player.send('OP')
            pos = Player.send(f'{OB4.obstacle_rect.right}')
            OB5.position(int(pos))
            OB10.position(int(pos))
            print(f"OBS POS REC - {int(pos)}")



        # if OB6.check(0):
        #     # req = Player.send('OP')
        #     # pos = Player.send(f'{OB5.obstacle_rect.right}')
        #     # OB6.position(int(pos))
        #     # print(f"OBS POS REC - {int(pos)}")
        #     req2 = Player.send('OBS_2')
        #     obs_down1_rect.midright = read_obs_co(req2)[0], read_obs_co(req2)[1]
        # if OB7.check(0):
        #     # req = Player.send('OP')
        #     # pos = Player.send(f'{OB6.obstacle_rect.right}')
        #     # OB7.position(int(pos))
        #     # print(f"OBS POS REC - {int(pos)}")
        #     req2 = Player.send('OBS_2')
        #     obs_down2_rect.midright = read_obs_co(req2)[0], read_obs_co(req2)[1]
        # if OB8.check(0):
        #     # req = Player.send('OP')
        #     # pos = Player.send(f'{OB7.obstacle_rect.right}')
        #     # OB8.position(int(pos))
        #     # print(f"OBS POS REC - {int(pos)}")
        #     req2 = Player.send('OBS_2')
        #     obs_down3_rect.midright = read_obs_co(req2)[0], read_obs_co(req2)[1]
        # if OB9.check(0):
        #     # req = Player.send('OP')
        #     # pos = Player.send(f'{OB8.obstacle_rect.right}')
        #     # OB9.position(int(pos))
        #     # print(f"OBS POS REC - {int(pos)}")
        #     req2 = Player.send('OBS_2')
        #     obs_down4_rect.midright = read_obs_co(req2)[0], read_obs_co(req2)[1]
        # if OB10.check(0):
        #     # req = Player.send('OP')
        #     # pos = Player.send(f'{OB9.obstacle_rect.right}')
        #     # OB10.position(int(pos))
        #     # print(f"OBS POS REC - {int(pos)}")
        #     req2 = Player.send('OBS_2')
        #     obs_down5_rect.midright = read_obs_co(req2)[0], read_obs_co(req2)[1]



        if p1.rect.top >= SET_HEIGHT - 100:
            p1.rect.bottom = SET_HEIGHT - 30
            game_music.stop()
            alive = Player.send('dead')
        if p1.rect.top <= 0:
            p1.rect.top = 0
            game_music.stop()
            alive = Player.send('dead')


        if not int(alive):
            Player.client.send('!D'.encode(Player.format))
            exit_online_screne(online_score)

        else:
            won = Player.send('winner?')
            if int(won):
                Player.client.send('RESET'.encode(Player.format))
                Player.client.send('!D'.encode(Player.format))
                game_music.stop()
                winning_screne(online_score)



        online_score_text = font_menu.render(str(score), True, 'black')
        online_score_rect = online_score_text.get_rect()
        online_score_rect.right = SET_WIDTH-50
        online_score_rect.top = 15

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
        #
        # pygame.draw.rect(screen, 'black', p1.rect, 2)
        # pygame.draw.rect(screen, 'black', OB1.obstacle_rect, 2)
        # pygame.draw.rect(screen, 'black', OB2.obstacle_rect, 2)
        # pygame.draw.rect(screen, 'black', OB3.obstacle_rect, 2)
        # pygame.draw.rect(screen, 'black', OB4.obstacle_rect, 2)
        # pygame.draw.rect(screen, 'black', OB5.obstacle_rect, 2)
        # pygame.draw.rect(screen, 'black', OB6.obstacle_rect, 2)
        # pygame.draw.rect(screen, 'black', OB7.obstacle_rect, 2)
        # pygame.draw.rect(screen, 'black', OB8.obstacle_rect, 2)
        # pygame.draw.rect(screen, 'black', OB9.obstacle_rect, 2)
        # pygame.draw.rect(screen, 'black', OB10.obstacle_rect, 2)

        # screen.blit(p2.image, p2.rect.center)

        animate_player_2.draw(screen)
        animate_player.draw(screen)
        animate_player.update(0)
        animate_player_2.update(1)
        screen.blit(online_score_text, (online_score_rect.left, online_score_rect.top))
        screen.blit(base_image_scaled, (0, 750))
        pygame.display.update()
        clock.tick(60)


def exit_online_screne(online_score):

    global HIGH_SCORE

    if online_score > HIGH_SCORE:
        score_text = font_menu.render("NEW HIGH SCORE : " + str(online_score), 1, (0, 0, 0))
        HIGH_SCORE = online_score
    else:
        score_text = font_menu.render("SCORE :  " + str(online_score), 1, (0, 0, 0))


    exit_screen_sound.play(-1)
    main_menu_button = button('MAIN MENU', SET_WIDTH/2-150, SET_HEIGHT/2+100, 300, 50)
    score_text_rect = score_text.get_rect()
    while True:
        screen.fill('black')
        screen.blit(background_menu, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if main_menu_button.check_click():
                    exit_screen_sound.stop()
                    main_menu(1)
        score_text_rect.center = SET_WIDTH/2, 200
        screen.blit(score_text, score_text_rect)
        screen.blit(pause_font.render('YOU LOOSE', True, 'black'), (SET_WIDTH/2 - 250, SET_HEIGHT/2 - 100))
        main_menu_button.draw()
        pygame.display.update()


def winning_screne(online_score):

    global HIGH_SCORE
    exit_screen_sound.play(-1)

    if online_score > HIGH_SCORE:
        score_text = font_menu.render("NEW HIGH SCORE : " + str(online_score), 1, (0, 0, 0))
        HIGH_SCORE = online_score
    else:
        score_text = font_menu.render("SCORE :  " + str(online_score), 1, (0, 0, 0))

    main_menu_button = button('MAIN MENU', SET_WIDTH/2-150, SET_HEIGHT/2+100, 300, 50)
    score_text_rect = score_text.get_rect()
    while True:
        screen.fill('black')
        screen.blit(background_menu, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if main_menu_button.check_click():
                    exit_screen_sound.stop()
                    main_menu(1)

        score_text_rect.center = SET_WIDTH/2, 200
        screen.blit(score_text, score_text_rect)
        screen.blit(pause_font.render('YOU WON', True, 'black'), (SET_WIDTH / 2 - 200, SET_HEIGHT / 2 - 100))
        main_menu_button.draw()
        pygame.display.update()






def gameplay_offline_screne():
    clock = pygame.time.Clock()
    score_rangex = 48
    score_rangey = 52
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
    tubespeed = -5

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


    arr = []

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

        arr.append(OB1)
        arr.append(OB2)
        arr.append(OB3)
        arr.append(OB4)
        arr.append(OB5)
        arr.append(OB6)
        arr.append(OB7)
        arr.append(OB8)
        arr.append(OB9)
        arr.append(OB10)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("EXITING")
                pygame.quit()
                sys.exit()


            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    gravity = -5.8
                    p1.animate()
                    flap.play()
                if event.key == pygame.K_ESCAPE:
                    state = True
                    while state:
                        animate_player.draw(screen)
                        pause(score, animate_player, arr)
                        state = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # event.button = 1 - left , 2-right, 3-middle,  4-wheel up, 5-wheel down
                    gravity = -5.8
                    p1.animate()
                    flap.play()
                if pause_button.check_click():
                    animate_player.draw(screen)
                    run = True
                    while run:
                        pause(score, animate_player, arr)
                        run = False

        if p1.hitbox.colliderect(OB1.hitbox_up) or p1.hitbox.colliderect(OB2.hitbox_up) or p1.hitbox.colliderect(OB3.hitbox_up):
            print("COLLIDE1")
            game_music.stop()
            intermediate(p1, score, arr)
        if p1.hitbox.colliderect(OB4.hitbox_up) or p1.hitbox.colliderect(OB5.hitbox_up) or p1.hitbox.colliderect(OB6.hitbox_down):
            print("COLLIDE2")
            game_music.stop()
            intermediate(p1, score, arr)
        if p1.hitbox.colliderect(OB7.hitbox_down) or p1.hitbox.colliderect(OB8.hitbox_down) or p1.hitbox.colliderect(OB9.hitbox_down) or p1.hitbox.colliderect(OB10.hitbox_down):
            print("COLLIDE3")
            game_music.stop()
            intermediate(p1, score, arr)

        if OB1.hitbox_up.right in range(score_rangex, score_rangey) or OB2.hitbox_up.right in range(score_rangex, score_rangey) or OB3.hitbox_up.right in range(score_rangex, score_rangey) \
                or OB4.hitbox_up.right in range(score_rangex, score_rangey) or OB5.hitbox_up.right in range(score_rangex, score_rangey):
            score += 1
            score_s.play()


        gravity += 0.4
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
            intermediate(p1, score, arr)
        if p1.rect.top <= 0:
            p1.rect.top = 0
            game_music.stop()
            intermediate(p1, score, arr)

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
        animate_player.update(0)
        screen.blit(score_text, (score_text_rect.left, score_text_rect.top))
        screen.blit(base_image_scaled, (0, 750))
        pause_button.draw()
        pygame.display.update()
        clock.tick(60)


def pause(score, animate_player, arr):

    escape_sound.play()
    print('PAUSE')
    run = True
    largetext = pause_font.render('PAUSED', True, 'black')
    score_text = font_menu.render('SCORE : ' + str(score), True, 'black')
    score_text_rect = score_text.get_rect()
    score_text_rect.center = (670, 350)
    con_but = button('CONTINUE', 200, 540, 275, 50)
    menu_but = button('MAIN MENU', 880, 540, 300, 50)

    while run:
        screen.fill('black')
        screen.blit(background_play, (0, 0))
        animate_player.draw(screen)

        for i in range(10):
            arr[i].draw()

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
                    main_menu(1)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    escape_sound.play()
                    run = False



        con_but.draw()
        menu_but.draw()
        screen.blit(base_image_scaled, (0, 750))
        screen.blit(largetext, (500, 200))
        screen.blit(score_text, score_text_rect)
        pygame.display.update()

    print("Main")



def intermediate(p1, score, arr):
    clock = pygame.time.Clock()
    g = 0
    initial_height = p1.rect.top
    pygame.display.set_caption('BETTER LUCK NEXT TIME')
    touch = 0

    while True:

        screen.blit(background_play, (0, 0))
        new_height = p1.rect.top

        for i in range(10):
            arr[i].draw()

        screen.blit(base_image_scaled, (0, 750))
        screen.blit(dead_image_up_scaled, (p1.rect.left + 60, p1.rect.top + 10))

        p1.rect.left += 4
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("EXITING")
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    main_menu(1)

        if touch == 0 and new_height == initial_height:
            hit.play()
            die.play()
            g = -1.5
            touch = 1

        p1.movey(g)
        g += 0.1

        if new_height >= 1500:
            exit_screen(score)
        pygame.display.update()
        clock.tick(150)


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
                    main_menu(1)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if b1.check_click():
                    exit_screen_sound.stop()
                    gameplay_offline_screne()
                if b2.check_click():
                    exit_screen_sound.stop()
                    main_menu(1)
                if b3.check_click():
                    print("EXITING")
                    pygame.quit()
                    sys.exit()
        screen.blit(base_image_scaled, (0, 750))
        b1.draw()
        b2.draw()
        b3.draw()
        pygame.display.update()


main_menu(1)
