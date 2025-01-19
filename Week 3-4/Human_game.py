import pygame
from pygame import mixer
import random
from enum import Enum
from collections import namedtuple

pygame.init()
font = pygame.font.Font('Week 3-4\resources\Bahnschrift.ttf',36)

class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4
    
Point = namedtuple('Point', 'x, y')

# rgb colors
TEXT_COLOR = (255, 255, 255)
BACK_GROUND = (221, 227, 52)


BLOCK_SIZE = 20
SPEED = 20

class SnakeGame:
    
    def __init__(self, w=640, h=480):
        self.w = w
        self.h = h
        # init display
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('Snake')
        self.clock = pygame.time.Clock()
        
        # init game state
        self.direction = Direction.RIGHT
        
        self.head = Point(self.w/2, self.h/2)
        self.snake = [self.head, 
                      Point(self.head.x-BLOCK_SIZE, self.head.y),
                      Point(self.head.x-(2*BLOCK_SIZE), self.head.y)]
        
        # graphics
        pygame.display.set_icon(pygame.image.load('Week 3-4/resources/icon.png'))
        self.head_down = pygame.transform.scale(pygame.image.load('Week 3-4/resources/head.png'),(BLOCK_SIZE*1.8,BLOCK_SIZE*1.8))
        self.head_right = pygame.transform.rotate(self.head_down,90)
        self.head_up = pygame.transform.rotate(self.head_down,180)
        self.head_left = pygame.transform.rotate(self.head_down,-90)
        self.block = pygame.transform.scale(pygame.image.load('Week 3-4/resources/block.png'),(BLOCK_SIZE,BLOCK_SIZE))
        self.apple = pygame.transform.scale(pygame.image.load('Week 3-4/resources/apple.png'),(BLOCK_SIZE,BLOCK_SIZE))
        # audios
        mixer.music.load('Week 3-4/resources/music.mp3')
        self.eat_sound = mixer.Sound('Week 3-4/resources/eat.mp3')
        mixer.music.play(-1)

        self.score = 0
        self.food = None
        self._place_food()
        
    def _place_food(self):
        x = random.randint(0, (self.w-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE 
        y = random.randint(0, (self.h-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE
        self.food = Point(x, y)
        if self.food in self.snake:
            self._place_food()
        
    def play_step(self):
        # 1. collect user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()
                elif event.key == pygame.K_LEFT:
                    self.direction = Direction.LEFT
                elif event.key == pygame.K_RIGHT:
                    self.direction = Direction.RIGHT
                elif event.key == pygame.K_UP:
                    self.direction = Direction.UP
                elif event.key == pygame.K_DOWN:
                    self.direction = Direction.DOWN
        
        # 2. move
        self._move(self.direction) # update the head
        self.snake.insert(0, self.head)
        
        # 3. check if game over
        game_over = False
        if self._is_collision():
            game_over = True
            return game_over, self.score
            
        # 4. place new food or just move
        if self.head == self.food:
            mixer.Sound.play(self.eat_sound)
            self.score += 1
            self._place_food()
        else:
            self.snake.pop()
        
        # 5. update ui and clock
        self._update_ui()
        self.clock.tick(SPEED)
        # 6. return game over and score
        return game_over, self.score
    
    def _is_collision(self):
        # hits boundary
        if self.head.x > self.w - BLOCK_SIZE or self.head.x < 0 or self.head.y > self.h - BLOCK_SIZE or self.head.y < 0:
            return True
        # hits itself
        if self.head in self.snake[1:]:
            return True
        
        return False
        
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
       
        text = font.render("Score: " + str(self.score), True, TEXT_COLOR)
        self.display.blit(text, [0, 0])
        pygame.display.flip()
        
    def _move(self, direction):
        x = self.head.x
        y = self.head.y
        if direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif direction == Direction.DOWN:
            y += BLOCK_SIZE
        elif direction == Direction.UP:
            y -= BLOCK_SIZE
            
        self.head = Point(x, y)
            

if __name__ == '__main__':
    game = SnakeGame()
    game_over = False
    # game loop
    while True:
        game_over, score = game.play_step()
        
        if game_over:
            break   
    print('Final Score', score)
    pygame.quit()
