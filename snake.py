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
    FPS = 30
    speed = 200 # 1000ms
    fpsClock = pygame.time.Clock()
    score = 0
    # New snake object
    snake = Snake(WIDTH, HEIGHT)
    # New food object
    food = Food(WIDTH, HEIGHT)
    glider = pygame.USEREVENT+1
    pygame.time.set_timer(glider, speed)

    score = Score(GREEN, BLUE)

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
            for j in range(40, HEIGHT, 40):
                pygame.draw.line(DISPLAYSURF, BLACK, (i,j), (i, j), 4)
        DISPLAYSURF.blit(snake.head, (snake.body[0][0], snake.body[0][1]))
        for part in snake.body:
            if part == 0:
                pass
            else:
                DISPLAYSURF.blit(snake.segment, (snake.body[part][0], snake.body[part][1]))
        DISPLAYSURF.blit(food.food, (food.x, food.y))
        DISPLAYSURF.blit(score.text_surface_obj, score.text_rect_obj)
        #snake.glide(snake.drxn)

        for event in pygame.event.get():

            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYUP:
                snake.drxn = snake.move(event)
            elif event.type == glider:
                snake.glide(snake.drxn)
                food.eaten(snake, score)
                
                if not len(snake.body) % 5:
                    pygame.time.set_timer(glider, speed//(len(snake.body))*2)
                print(snake.body)
        pygame.display.update()
        fpsClock.tick(FPS)

class Snake():
    def __init__(self, WIDTH, HEIGHT):
        self.head = pygame.transform.scale(pygame.image.load("img/snake.png"), (40, 40))
        self.segment = pygame.transform.scale(pygame.image.load("img/kiwi.png"), (40, 40))
        self.body = {0:[120, 120], 1:[80, 120], 2:[40, 120]}
        self.WIDTH, self.HEIGHT = WIDTH, HEIGHT
        self.drxn = "right"
    #when u move, check if you coincide- if so the grow -> then update coordinates

    def glide(self, drxn):
        temp = copy.deepcopy(self.body)
        if drxn == "left" and self.body[0][0]-40 >=0:
            for keys in self.body:
                if keys != 0:
                    self.body[keys] = temp[keys-1]  # figure out a way to pass coordinates from one seg to the next ne
            self.body[0][0] -= 40
        if drxn == "right" and self.body[0][0]+80 <= self.WIDTH:
            for keys in self.body:
                if keys != 0:
                    self.body[keys] = temp[keys-1]
            self.body[0][0] += 40
        if drxn == "up" and self.body[0][1]-40 >= 40:
            for keys in self.body:
                if keys != 0:
                    self.body[keys] = temp[keys-1]
            self.body[0][1] -= 40
        if drxn == "down" and self.body[0][1]+80 <= self.HEIGHT:
            for keys in self.body:
                if keys != 0:
                    self.body[keys] = temp[keys-1]
            self.body[0][1] += 40
        
    def move(self, event):
        if (event.key in (K_LEFT, K_a)) and self.body[0][0]-40 >=0:
            return "left"
        if (event.key in (K_RIGHT, K_d)) and self.body[0][0]+80 <= self.WIDTH:
            return "right"
        if (event.key in (K_UP, K_w)) and self.body[0][1]-40 >= 0:
            return "up"
        if (event.key in (K_DOWN, K_s)) and self.body[0][1]+80 <= self.HEIGHT:
            return "down"

    def grow(self):
        self.body[len(self.body)] = self.body[len(self.body)-1]

class Food():
    def __init__(self, WIDTH, HEIGHT):
        self.WIDTH, self.HEIGHT = WIDTH, HEIGHT
        self.food = pygame.transform.scale(pygame.image.load("img/poo.png"), (40, 40))
        #self.x, self.y = (380, 110)#(random.choice(range(WIDTH)), random.choice(range(HEIGHT)))
        self.x, self.y = (random.choice(range(0, self.WIDTH, 40)), random.choice(range(40, self.HEIGHT, 40)))
    
    def eaten(self, snake, score):
        if [self.x, self.y] == snake.body[0]:
            print("Eaten!!!")
            snake.grow()
            self.x, self.y = (random.choice(range(0, self.WIDTH, 40)), random.choice(range(40, self.HEIGHT, 40)))
            score.hit()

class Score():
    def __init__(self, GREEN, BLUE):
        self.score = 0
        self.font_obj = pygame.font.Font('freesansbold.ttf', 40)
        self.text_surface_obj = self.font_obj.render('Score: ' + str(self.score), True, GREEN, BLUE)
        self.text_rect_obj = self.text_surface_obj.get_rect()
        self.text_rect_obj.center = (320, 20)
        self.GREEN, self.BLUE = GREEN, BLUE

    def hit(self):
        self.score += 1 
        self.text_surface_obj = self.font_obj.render('Score: ' + str(self.score), True, self.GREEN, self.BLUE)
    

if __name__ == "__main__":
    main()


    