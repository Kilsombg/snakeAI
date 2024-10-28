import pygame
import random
from enum import Enum
from collections import namedtuple

class Direction(Enum):
    RIGHT = 0
    DOWN = 1
    LEFT = 2
    UP = 3

Point = namedtuple('Point', 'x, y')
BLOCK_SIZE = 20
SPEED = 15

# rgb colors
WHITE = (255, 255, 255)
RED = (200,0,0)
Green = (0, 200, 0)
Green2 = (0, 255, 100)
BLACK = (0,0,0)

pygame.init()
font = pygame.font.Font('arial.ttf', 25)

class SnakeGame():
    def __init__(self):
        self.w = 640
        self.h = 480
        
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('Snake')
        self.clock = pygame.time.Clock()

        self.direction = Direction.RIGHT
        self.prev_direction = self.direction

        self.head = Point(self.w/2, self.h/2)
        self.snake = [self.head, 
                      Point(self.head.x-BLOCK_SIZE, self.head.y),
                      Point(self.head.x-(2*BLOCK_SIZE), self.head.y)]

        self.score = 0
        self.food = None
        self.__create_food()
    
    def __create_food(self):
        x = random.randint(0, (self.w-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE 
        y = random.randint(0, (self.h-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE
        self.food = Point(x, y)
        if self.food in self.snake:
            self.__create_food()


    def play_step(self):
        # handle events
        self.__handle_input()

        # update snake
        self.__move()
        self.snake.insert(0, self.head)

        # check for collision
        game_over = False
        if self.__is_collision():
            game_over = True
            return game_over, self.score

        # update food
        if self.head == self.food:
            self.score += 1
            self.__create_food()
        else:
            self.snake.pop()

        # render
        self.__render()
        self.clock.tick(SPEED)

        return game_over, self.score

    
    def __handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    self.direction = Direction.RIGHT
                elif event.key == pygame.K_DOWN:
                    self.direction = Direction.DOWN
                elif event.key == pygame.K_LEFT:
                    self.direction = Direction.LEFT
                elif event.key == pygame.K_UP:
                    self.direction = Direction.UP

    
    def __is_collision(self):
        # hits boundary
        if self.head.x > self.w - BLOCK_SIZE or self.head.x < 0 or self.head.y > self.h - BLOCK_SIZE or self.head.y < 0:
            return True
            
        # hits itself
        if self.head in self.snake[1:]:
            return True
        
        return False


    def __move(self):
        # hit opposite direction
        if abs(self.prev_direction.value - self.direction.value) == 2:
            self.direction = self.prev_direction

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
        self.prev_direction = self.direction


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

if __name__ == '__main__':
    game = SnakeGame()

    while True:
        game_over, score = game.play_step()
        
        if game_over == True:
            break
        
    print('Final Score', score)

    pygame.quit()
