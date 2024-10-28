import pygame
import random
from enum import Enum
from collections import namedtuple
import numpy as np

class Direction(Enum):
    RIGHT = 0
    DOWN = 1
    LEFT = 2
    UP = 3

Point = namedtuple('Point', 'x, y')
BLOCK_SIZE = 20
SPEED = 40

# rgb colors
WHITE = (255, 255, 255)
RED = (200,0,0)
Green = (0, 200, 0)
Green2 = (0, 255, 100)
BLACK = (0,0,0)

pygame.init()
font = pygame.font.Font('arial.ttf', 25)


class SnakeGameAI:

    def __init__(self, w=640, h=480):
        self.w = w
        self.h = h

        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('SnakeAI')
        self.clock = pygame.time.Clock()
        self.reset()


    def reset(self):
        self.direction = Direction.RIGHT

        self.head = Point(self.w/2, self.h/2)
        self.snake = [self.head,
                      Point(self.head.x-BLOCK_SIZE, self.head.y),
                      Point(self.head.x-(2*BLOCK_SIZE), self.head.y)]

        self.score = 0
        self.food = None
        self.__create_food()
        self.frame_iteration = 0


    def __create_food(self):
        x = random.randint(0, (self.w-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE
        y = random.randint(0, (self.h-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE
        self.food = Point(x, y)
        if self.food in self.snake:
            self.__create_food()


    def play_step(self, action):
        self.frame_iteration += 1

       # handle quit event
        self.__handle_input()
        
       # update snake
        self._move(action)
        self.snake.insert(0, self.head)
        
        # check for collision
        reward = 0
        game_over = False
        if self.is_collision() or self.frame_iteration > 100*len(self.snake):
            game_over = True
            reward = -10
            return reward, game_over, self.score

        # update food
        if self.head == self.food:
            self.score += 1
            reward = 10
            self.__create_food()
        else:
            self.snake.pop()
        
        # render
        self.__render()
        self.clock.tick(SPEED)
        
        return reward, game_over, self.score

    def __handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            

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


    def _move(self, action):
        # [straight, right, left]

        clock_wise = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
        idx = clock_wise.index(self.direction)

        if np.array_equal(action, [1, 0, 0]):
            new_dir = clock_wise[idx] # no change
        elif np.array_equal(action, [0, 1, 0]):
            next_idx = (idx + 1) % 4
            new_dir = clock_wise[next_idx] # right turn r -> d -> l -> u
        else: # [0, 0, 1]
            next_idx = (idx - 1) % 4
            new_dir = clock_wise[next_idx] # left turn r -> u -> l -> d

        self.direction = new_dir

        x = self.head.x
        y = self.head.y
        if self.direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif self.direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif self.direction == Direction.DOWN:
            y += BLOCK_SIZE
        elif self.direction == Direction.UP:
            y -= BLOCK_SIZE

        self.head = Point(x, y)


    def __render(self):
        self.display.fill(BLACK)

        self.__draw_snake()
            
        pygame.draw.rect(self.display, RED, pygame.Rect(self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE))
        
        text = font.render("Score: " + str(self.score), True, WHITE)
        self.display.blit(text, [0, 0])
        pygame.display.flip()


    def __draw_snake(self):
        for i, pt in enumerate(self.snake):
            dx = dy = 4
            w = h = BLOCK_SIZE - 8

            if i > 0 and i < len(self.snake)-1:
                dx, dy, w, h = self.__compare_snake_parts(pt, self.snake[i-1], dx, dy, w, h)
                dx, dy, w, h = self.__compare_snake_parts(pt, self.snake[i+1], dx, dy, w, h)
            elif i == 0:
                dx, dy, w, h = self.__compare_snake_parts(pt, self.snake[i+1], dx, dy, w, h)
            else: # i < len(self.snake)
                dx, dy, w, h = self.__compare_snake_parts(pt, self.snake[i-1], dx, dy, w, h)
            
            pygame.draw.rect(self.display, Green, pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(self.display, Green2, pygame.Rect(pt.x+dx, pt.y+dy, w, h))


    def __compare_snake_parts(self, pt1, pt2, dx, dy, w, h):

        # check where is pt2 and draw pt1
        # left adjacent
        if pt1.x > pt2.x:
            dx -= 4
            w += 4
        
        # right adjacent
        if pt1.x < pt2.x:
            w += 4
        
        # top adjacent
        if(pt1.y > pt2.y):
            dy -= 4
            h += 4
        
        # down adjacent
        if(pt1.y < pt2.y):
            h += 4

        return dx, dy, w, h