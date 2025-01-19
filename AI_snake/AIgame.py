import pygame
from pygame import mixer
import random
from enum import Enum
from collections import namedtuple
import numpy as np

pygame.init()
font = pygame.font.Font('resources\Bahnschrift.ttf',36)

class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4

Point = namedtuple('Point','x, y')

# RGB colors
WHITE = (255,255,255)
RED = (200,0,0)
BLUE1 = (0,0,255)
BLUE2 = (0,100,255)
BLACK = (0,0,0)
BACK_GROUND = (221, 227, 52)

BLOCK_SIZE = 20
SPEED = 80

class SnakeGameAI:

    def __init__(self, w = 640, h=480):
        self.w = w
        self.h = h
        # initializing display
        self.display = pygame.display.set_mode((self.w,self.h))
        pygame.display.set_caption('Snake')
        # graphics
        pygame.display.set_icon(pygame.image.load('resources/icon.png'))
        self.head_down = pygame.transform.scale(pygame.image.load('resources/head.png'),(BLOCK_SIZE*1.8,BLOCK_SIZE*1.8))
        self.head_right = pygame.transform.rotate(self.head_down,90)
        self.head_up = pygame.transform.rotate(self.head_down,180)
        self.head_left = pygame.transform.rotate(self.head_down,-90)
        self.block = pygame.transform.scale(pygame.image.load('resources/block.png'),(BLOCK_SIZE,BLOCK_SIZE))
        self.apple = pygame.transform.scale(pygame.image.load('resources/apple.png'),(BLOCK_SIZE,BLOCK_SIZE))
        # audios
        mixer.music.load('resources/music.mp3')
        self.eat_sound = mixer.Sound('resources/eat.mp3')
        mixer.music.play(-1)
        
        self.clock = pygame.time.Clock()
        self.reset()

    def reset(self):
        # initializing game state
        self.direction = Direction.RIGHT

        self.head = Point(self.w/2,self.h/2)
        self.snake = [self.head, Point(self.head.x - BLOCK_SIZE, self.head.y),Point(self.head.x - 2*BLOCK_SIZE, self.head.y)]

        self.score = 0
        self.food = None
        self._place_food()
        self.frame_iteration = 0
        self.food_dis = self.man_dis(self.head,self.food)


    def _place_food(self):
        x = random.randint(0,(self.w-BLOCK_SIZE)//BLOCK_SIZE)*BLOCK_SIZE
        y = random.randint(0,(self.h-BLOCK_SIZE)//BLOCK_SIZE)*BLOCK_SIZE
        self.food = Point(x,y)
        if self.food in self.snake:
            self._place_food()

    def play_step(self,action):
        self.frame_iteration+=1

        # collect user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                
        # move
        self._move(action) # update the head
        self.snake.insert(0,self.head)

        # checking game over
        game_over = False
        if self.is_collision() or self.frame_iteration > 100*len(self.snake):
            game_over = True
            reward = -10
            return reward, game_over, self.score
        
        # place new food or just move
        if self.head == self.food:
            self.score += 1
            reward = 10
            self._place_food()
            mixer.Sound.play(self.eat_sound)
        else:
            reward = 10/self.man_dis(self.head,self.food) - 10/self.food_dis 
            self.food_dis = self.man_dis(self.head,self.food) 
            self.snake.pop()

        # update user interface
        self._update_ui()
        self.clock.tick(SPEED)

        # return game over, score and reward
        return reward, game_over, self.score

    def is_collision(self, pt=None):
        if pt is None:
            pt = self.head
        # hits boundary
        if pt.x > self.w - BLOCK_SIZE or pt.x < 0 or pt.y > self.h - BLOCK_SIZE or pt.y < 0:
            return True
        # hits itself
        if pt in self.snake[1:]:
            return True

        return False
    
    def man_dis(self, pt1, pt2): # calculates manhatten distance
        delta_x = abs(pt1.x - pt2.x)
        delta_y = abs(pt1.y - pt2.y)
        return delta_x+delta_y
    
    def _update_ui(self):
        self.display.fill(BACK_GROUND)
        for pt in self.snake[1:]:
            self.display.blit(self.block,pt)
        headx = self.snake[0].x - BLOCK_SIZE*0.4
        heady = self.snake[0].y - BLOCK_SIZE*0.4
        if self.direction==Direction.RIGHT:
            self.display.blit(self.head_right,(headx,heady))
        if self.direction==Direction.LEFT:
            self.display.blit(self.head_left,(headx,heady))
        if self.direction==Direction.UP:
            self.display.blit(self.head_up,(headx,heady))
        if self.direction==Direction.DOWN:
            self.display.blit(self.head_down,(headx,heady))
        self.display.blit(self.apple,self.food)

        text = font.render(f'Score: {self.score}', True, WHITE)
        self.display.blit(text,[0,0])
        pygame.display.update()

    def _move(self, action):
        # [straight, right, left]

        clock_wise = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
        idx = clock_wise.index(self.direction)

        if np.array_equal(action, [1,0,0]):
            new_dir = clock_wise[idx] # no change
        elif np.array_equal(action,[0,1,0]):
            next_idx = (idx+1) % 4
            new_dir = clock_wise[next_idx] # turn right r -> d -> l -> u
        else: # [0,0,1]
            next_idx = (idx-1) % 4
            new_dir = clock_wise[next_idx] # turn left r -> u -> l -> d
        
        self.direction = new_dir

        x = self.head.x
        y = self.head.y
        if self.direction == Direction.RIGHT:
            x += BLOCK_SIZE
        if self.direction == Direction.LEFT:
            x -= BLOCK_SIZE
        if self.direction == Direction.UP:
            y -= BLOCK_SIZE
        if self.direction == Direction.DOWN:
            y += BLOCK_SIZE

        self.head = Point(x,y)