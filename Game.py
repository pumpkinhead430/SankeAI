import pygame
from CONSTANTS import *
from Snake import Snake
from Fruit import Fruit


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Snake")
        self.fps = FPS
        self.frame_iteration = 0
        self.window = pygame.display.set_mode((cell_size * cell_number, cell_size * cell_number))
        self.clock = pygame.time.Clock()
        self.score = 0
        self.game_over = False
        self.run = True
        self.snake = Snake(self.window)
        self.fruit = Fruit(self.window, self.snake.body)

    def reset(self):
        self.score = 0
        self.game_over = False
        self.snake = Snake(self.window)
        self.fruit = Fruit(self.window, self.snake.body)
        self.frame_iteration = 0

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

        self.frame_iteration += 1
        self.snake.change_by_action(action)
        current_length = len(self.snake.body)
        self.snake.update_snake(self.fruit.pos)
        if len(self.snake.body) > current_length:
            self.score += 1
        reward = 0

        if self.frame_iteration > move_amount * len(self.snake.body):
            self.snake.is_dead = True

        if self.snake.is_dead:
            self.game_over = True
            reward = -10
            if self.snake.snake_inside(self.snake.head):
                reward -= 10
            return reward, self.game_over, self.score

        if self.snake.head == self.fruit.pos:
            self.fruit = Fruit(self.window, self.snake.body)
            reward = 10
            return reward, self.game_over, self.score

        return reward, self.game_over, self.score

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
