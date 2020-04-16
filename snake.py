import sys
from pygame.locals import *

import pygame
import time
import random
import copy

def main():
    pygame.init()
    # set up the window
    WIDTH = 1280
    HEIGHT = 720
    DISPLAYSURF = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
    pygame.display.set_caption('Snake BoOOY')
    # set up the colors

    BLACK = (  0,   0,   0)
    WHITE = (255, 255, 255)
    RED = (255,   0,   0)
    GREEN = (  0, 255,   0)
    BLUE = (  0,   0, 255)
    FPS = 5
    fpsClock = pygame.time.Clock()
    # New snake object
    snake = Snake(WIDTH, HEIGHT)
    # New food object
    food = Food(WIDTH, HEIGHT)
    """
    # sound
    #pygame.mixer.init()
    #beep = pygame.mixer.Sound("beep-03.wav")
    # Loading and playing background music:
    pygame.mixer.music.load('backgroundmusic.mp3')
    pygame.mixer.music.play(-1, 0.0)
    # ...some more of your code goes here...
    pygame.mixer.music.stop()
    """
    # run the game loop

    while True:
        DISPLAYSURF.fill(WHITE)
        for i in range(0, WIDTH, 40):
            for j in range(0, HEIGHT, 40):
                pygame.draw.line(DISPLAYSURF, BLACK, (i,j), (i, j), 4)
        DISPLAYSURF.blit(snake.head, (snake.body[0][0], snake.body[0][1]))
        for part in snake.body:
            if part == 0:
                pass
            else:
                DISPLAYSURF.blit(snake.segment, (snake.body[part][0], snake.body[part][1]))
        DISPLAYSURF.blit(food.food, (food.x, food.y))

        for event in pygame.event.get():

            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYUP:
                snake.move(event)
                food.eaten(snake)
                print(snake.body)
        pygame.display.update()
        fpsClock.tick(FPS)

class Snake():
    def __init__(self, WIDTH, HEIGHT):
        self.head = pygame.transform.scale(pygame.image.load("img/snake.png"), (40, 40))
        self.segment = pygame.transform.scale(pygame.image.load("img/kiwi.png"), (40, 40))
        self.body = {0:[120, 120], 1:[80, 120], 2:[40, 120]}
        self.WIDTH, self.HEIGHT = WIDTH, HEIGHT
    #when u move, check if you coincide- if so the grow -> then update coordinates

    def move(self, event):
        temp = copy.deepcopy(self.body)
        if (event.key in (K_LEFT, K_a)) and self.body[0][0]-40 >=0:
            for keys in self.body:
                if keys != 0:
                    self.body[keys] = temp[keys-1]  # figure out a way to pass coordinates from one seg to the next ne
            self.body[0][0] -= 40
        if (event.key in (K_RIGHT, K_d)) and self.body[0][0]+80 <= self.WIDTH:
            for keys in self.body:
                if keys != 0:
                    self.body[keys] = temp[keys-1]
            self.body[0][0] += 40
        if (event.key in (K_UP, K_w)) and self.body[0][1]-40 >= 0:
            for keys in self.body:
                if keys != 0:
                    self.body[keys] = temp[keys-1]
            self.body[0][1] -= 40
        if (event.key in (K_DOWN, K_s)) and self.body[0][1]+80 <= self.HEIGHT:
            for keys in self.body:
                if keys != 0:
                    self.body[keys] = temp[keys-1]
            self.body[0][1] += 40
        if event.key == K_q:
            self.grow()

    def grow(self):
        self.body[len(self.body)] = self.body[len(self.body)-1]

class Food():
    def __init__(self, WIDTH, HEIGHT):
        self.WIDTH, self.HEIGHT = WIDTH, HEIGHT
        self.food = pygame.transform.scale(pygame.image.load("img/poo.png"), (40, 40))
        #self.x, self.y = (380, 110)#(random.choice(range(WIDTH)), random.choice(range(HEIGHT)))
        self.x, self.y = (random.choice(range(0, self.WIDTH, 40)), random.choice(range(0, self.HEIGHT, 40)))

    def eaten(self, snake):
        if [self.x, self.y] == snake.body[0]:
            print("Eaten!!!")
            snake.grow()
            self.x, self.y = (random.choice(range(0, self.WIDTH, 40)), random.choice(range(0, self.HEIGHT, 40)))


if __name__ == "__main__":
    main()


    