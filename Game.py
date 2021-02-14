import pygame
from CONSTANTS import *
from Snake import Snake
from Fruit import Fruit


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Snake")
        self.fps = FPS
        self.frames_left = starting_moves
        self.window = pygame.display.set_mode((cell_size * cell_number, cell_size * cell_number))
        self.clock = pygame.time.Clock()
        self.score = 0
        self.run = True
        self.snake = Snake(self.window)
        self.fruit = Fruit(self.window, self.snake.body)

    def reset(self):
        self.score = 0
        self.run = True
        self.snake = Snake(self.window)
        self.fruit = Fruit(self.window, self.snake.body)

    def update(self, action=straight):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False
            if event.type == pygame.KEYDOWN:
                self.snake.change_direction(event.key)
                if event.key == pygame.K_w:
                    self.fps = self.fps * 2
                    print(self.fps)
                if event.key == pygame.K_s:
                    self.fps = self.fps / 2
                    print(self.fps)

        self.snake.change_by_action(action)
        self.snake.update_snake(self.fruit.pos)

        if self.snake.head == self.fruit.pos:
            self.fruit = Fruit(self.window, self.snake.body)

        if self.snake.dead():
            self.reset()

    def draw(self):
        self.window.fill(Black)
        self.fruit.draw_fruit()
        self.snake.draw_snake()
        pygame.display.update()

    def delay(self):
        self.clock.tick(self.fps)

    @staticmethod
    def end_game():
        pygame.quit()

    def is_running(self):
        return self.run
