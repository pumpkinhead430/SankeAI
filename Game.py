import pygame
from CONSTANTS import *
from Snake import Snake
from Fruit import Fruit
from  pygame import Vector2
import numpy as np

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Snake")
        self.fps = FPS
        self.board = np.zeros((cell_number + 1, cell_number + 1))
        self.put_borders(self.board)
        self.frame_iteration = 0
        self.window = pygame.display.set_mode((cell_size * cell_number, cell_size * cell_number))
        self.clock = pygame.time.Clock()
        self.score = 0
        self.game_over = False
        self.run = True
        self.snake = Snake(self.window)
        self.fruit = Fruit(self.window, self.snake.body)
        self.put_snake_fruit(self.board)

    def reset(self):
        self.score = 0
        self.board = np.zeros((cell_number, cell_number))
        self.put_borders(self.board)
        self.game_over = False
        self.snake = Snake(self.window)
        self.fruit = Fruit(self.window, self.snake.body)
        self.put_snake_fruit(self.board)
        self.frame_iteration = 0

    @staticmethod
    def put_borders(board):
        for i in range(board.shape[1]):
            board[0][i] = -1

        for i in range(board.shape[1]):
            board[board.shape[0] - 1][i] = -1

        for i in range(board.shape[0]):
            board[i][0] = -1

        for i in range(board.shape[0]):
            board[i][board.shape[1] - 1] = -1

    def put_snake_fruit(self, board):
        for point in self.snake.body:
            board[int(point.y / cell_size)][int(point.x / cell_size)] = -1
        board[int(self.fruit.pos.y / cell_size)][int(self.fruit.pos.x / cell_size)] = 1

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
        tail = Vector2(self.snake.body[-1].x / cell_size, self.snake.body[-1].y / cell_size)
        self.board[int(tail.y)][int(tail.x)] = 0
        self.snake.update_snake(self.fruit.pos)
        self.board[int(self.snake.head.y / cell_size)][int(self.snake.head.x / cell_size)] = -1

        if len(self.snake.body) > current_length:
            self.board[int(tail.y)][int(tail.x)] = -1
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
            self.board[int(self.fruit.pos.y / cell_size)][int(self.fruit.pos.x / cell_size)] = 0
            self.fruit = Fruit(self.window, self.snake.body)
            self.board[int(self.fruit.pos.y / cell_size)][int(self.fruit.pos.x / cell_size)] = 1
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
