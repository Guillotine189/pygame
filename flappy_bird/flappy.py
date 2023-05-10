import sys

import pygame
pygame.font.init()
pygame.init()


SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 800

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
player_image = pygame.image.load('./images/images.png')
p1 = pygame.image.load('./images/top.png')
p2 = pygame.image.load('./images/down.png')


upper_limit = SCREEN_HEIGHT - 146  # meaning THE BOTTOM
lower_limit = -50       # MEANING THE TOP

text = pygame.font.SysFont("monospace", 50)

class Button:
    def __init__(self,x,y,text,l,h):
        self.x = x
        self.y = y
        self.text = text
        self.l = l
        self.h = h
        self.draw()

    def draw(self):
        button_text = text.render(self.text, 1, 'black')
        button_rect = pygame.rect.Rect((self.x, self.y), (self.l, self.h)) # first 2 are x and y coordinates and the next 2 are the size of the box
        if self.check_clicekd():
            pygame.draw.rect(screen, 'dark grey', button_rect, 0, 5)
        else:
            pygame.draw.rect(screen, 'light grey', button_rect, 0, 5)

        screen.blit(button_text, (self.x + 15, self.y))


    def check_clicekd(self):
        m_pos = pygame.mouse.get_pos()
        left_cl = pygame.mouse.get_pressed()[0]
        button_rect = pygame.rect.Rect((self.x, self.y), (self.l, self.h))
        if left_cl and button_rect.collidepoint(m_pos):
            return True
        else:
            return False

def player(z, x, y):

    screen.blit(z, (x, y))

def main_menu():
    print("MENU")
    pygame.display.set_caption("MENU")
    menu_bg = pygame.image.load('./images/manu_1400x800.png')
    textbgd = text.render("MENU", 1, (255, 255, 255))

    while True:

        screen.fill("black")
        screen.blit(menu_bg, (0, 0))
        screen.blit(textbgd, (912, 300))

        button1 = Button(800, 400, "PLAY", 150, 50)
        button2 = Button(1000, 400, "EXIT", 150, 50)
        button3 = Button(840, 500, "controls", 275, 50)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("EXITING..")
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    screen2()
                if event.key == pygame.K_ESCAPE:
                    print("EXITING..")
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button1.check_clicekd():
                    screen2()
                if button2.check_clicekd():
                    print("EXITING..")
                    pygame.quit()
                    sys.exit()
                if button3.check_clicekd():
                    controls()


        playerX = 0
        playerY = 200
        player(player_image,playerX, playerY)
        pygame.display.update()

def controls():

    print("CONTROLS")
    pygame.display.set_caption("Controls")
    control_text1 = text.render("CONTROLS", True, (0, 0, 0))
    control_text2 = text.render("LEFT CLICK OR PRESS SPACE BAR TO FLY", True, (0, 0, 0))
    control_text3 = text.render("PRESS ESCAPE TO GO BACK ", True, (0, 0, 0))

    back = pygame.image.load('./images/manu_1400x800.png')
    while True:

        screen.fill("black")
        screen.blit(back, (0, 0))
        screen.blit(control_text1, (580, 230))
        screen.blit(control_text2, (150, 300))
        screen.blit(control_text3, (360, 370))
        goback = Button(600, 450, "GO BACK", 250, 50)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("EXITING..")
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if goback.check_clicekd():
                    main_menu()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    main_menu()

        pygame.display.update()
HIGH_SCORE = 0

def third(x):
    global HIGH_SCORE
    print("LOOSE")
    back = pygame.image.load("./images/flappy_1400x800.png")
    image = pygame.image.load('./images/dead_final_60.png')


    if x > HIGH_SCORE:
        score = text.render("NEW HIGH SCORE : " + str(x), 1, (0, 0, 0))
        HIGH_SCORE = x
        y = 430
        z = 200
    else:
        score = text.render("SCORE :  " + str(x), 1, (0, 0, 0))
        y = 500
        z = 200

    while True:
        screen.fill("black")
        screen.blit(back, (0, 0))
        screen.blit(score, (y, z))

        screen.blit(image, (630, 350))

        button1 = Button(200, 340, "Try again", 300, 50)
        button2 = Button(880, 340, "Main menu", 300, 50)
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                print("EXITING..")
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if button1.check_clicekd():
                    screen2()
                if button2.check_clicekd():
                    main_menu()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    main_menu()


        pygame.display.update()

def screen2():
    print("Screen2")
    up_speed = 7
    gravity = 0.1
    pygame.display.set_caption("FLAPPY BIRD")
    background = pygame.image.load("./images/flappy_1400x800.png")

    count = 0
    playerX = 0
    playerY = 200
    playerX_ch = 0
    playerY_ch = 0
    while True:

        screen.fill("black")
        screen.blit(background, (0, 0))
        back = Button(SCREEN_WIDTH - 330, SCREEN_HEIGHT - 60, 'MAIN MENU', 300, 50)
        score_text = text.render(str(count), 1, (0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("EXITING..")
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    playerY_ch -= up_speed
                    count = count + 1
                if event.key == pygame.K_ESCAPE:
                    main_menu()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # event.button = 1 - left , 2-right, 3-middle,  4-wheel up, 5-wheel down
                    playerY_ch -= up_speed
                    count = count + 1
                if back.check_clicekd():
                    main_menu()


        playerY += playerY_ch
        playerX += playerX_ch
        playerY_ch += gravity

        if playerY >= upper_limit:
            playerY = upper_limit
            # playerY_ch -= gravity
            playerY_ch = 0
            third(count)

        if playerY < lower_limit:
            playerY = lower_limit
            # playerY_ch += gravity
            playerY_ch = 0
            third(count)


        player(player_image, playerX, playerY)
        screen.blit(score_text, (SCREEN_WIDTH - 60, 30))
        pygame.display.update()




main_menu()