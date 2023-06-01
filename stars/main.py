import sys
import random
import pygame


width = 1400
height = 800
screen = pygame.display.set_mode((width, height))

arr = []
total_stars = 450


class Stars:

    def __init__(self):
        self.x = random.randint(0, width)
        self.y = random.randint(0, height/2)
        self.z = random.uniform(0.1, 1)
        self.dx = self.x
        self.dy = self.y

    def move(self):
        self.z -= 0.002    # SPEED
        if self.z <= 0 or self.x < 0 or self.x > width or self.y > height:
            self.x = random.randint(0, width)
            self.y = random.randint(0, height/2)
            self.z = random.uniform(0.1, 1)

    def update(self):
        if self.x <= width/2:
            self.dx = width/2 - self.x / self.z
            self.dy = self.y / self.z
        else:
            self.dx = self.x/self.z
            self.dy = self.y / self.z

    def draw(self):
        pygame.draw.circle(screen, 'white', (self.dx, self.dy), 3)


def setup():
    global arr
    for it in range(total_stars):
        # print(it)
        obj = Stars()
        arr.append(obj)


setup()


while True:

    screen.fill('black')

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

    for i in arr:
        i.move()
        i.update()
        i.draw()

    pygame.display.update()
