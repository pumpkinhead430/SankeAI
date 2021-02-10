# this branch is the main branch - normal neural network

import pygame
from pygame.math import Vector2
import numpy as np
from Fruit import Fruit
import copy
import time
import random
from Snake import Snake
from CONSTANTS import *


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Snake")
        self.gen = 0
        self.best = 0
        self.best_fitness = 0
        self.fps = FPS
        self.run = True
        self.window = pygame.display.set_mode((cell_size * cell_number, cell_size * cell_number))
        self.best_snake = Snake(self.window)
        self.clock = pygame.time.Clock()
        self.snakes = []
        for i in range(snake_amount):
            self.snakes.append(Snake(self.window))
        self.alive = snake_amount
        self.SCREEN_UPDATE = pygame.USEREVENT
        pygame.time.set_timer(self.SCREEN_UPDATE, 20)

    @staticmethod
    def print_weights(brain):
        for layer in brain.hidden_layers:
            print(layer.weights)
        print('\n')

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    self.fps = round(self.fps * 2)
                if event.key == pygame.K_s:
                    self.fps = round(self.fps / 2)

        self.update_snakes()
        if self.alive == 0:
            self.new_gen()

    def new_gen(self):
        self.best_snake.calculate_fitness()
        print(f'best fitness: {self.best_snake.fitness}')
        print(f'best score: {self.best_snake.score}')

        for snake in self.snakes:
            snake.calculate_fitness()
            snake.reset()

        self.snakes = sorted(self.snakes, key=lambda y: y.fitness, reverse=True)
        if self.best_snake is self.snakes[0]:
            self.best += 1
        else:
            self.best_snake = self.snakes[0]
            self.best = 0

        if self.best >= 3:
            print('help')
            self.snakes[1].brain.copy(self.best_snake.brain)
            self.snakes[1].brain.mutate(mutation_rate / 5)
            self.best = 0

        new_snakes = []
        for i in range(round(len(self.snakes) * 0.1)):
            new_snakes.append(self.snakes[i])
        print('\n')

        for i in range(round(len(self.snakes) * 0.2)):
            new_snake = Snake(self.window)
            new_snake.brain.copy(self.snakes[0].brain)
            new_snake.brain.mutate(mutation_rate)
            new_snakes.append(new_snake)

        for i in range(0, round(len(self.snakes) * 0.2) - 1, 2):
            cross_snake1 = Snake(self.window)
            cross_snake2 = Snake(self.window)
            cross_snake1.brain, cross_snake2.brain = self.snakes[i].brain.crossover(self.snakes[i + 1].brain)
            new_snakes.extend([cross_snake1, cross_snake2])

        for i in range(len(new_snakes)):
            new_snake = Snake(self.window)
            new_snake.brain.copy(new_snakes[i].brain)
            new_snake.brain.mutate(mutation_rate)
            new_snakes.append(new_snake)

        self.snakes = new_snakes

        self.alive = snake_amount
        self.gen += 1
        print('starting gen number:', self.gen)

    def update_snakes(self):
        for snake in self.snakes:
            if not snake.is_dead:
                if snake.on_fruit():
                    snake.enlarge_snake()
                    snake.new_fruit()
                    snake.inc_score()

                snake.look()
                snake.think()

                self.alive += snake.update_snake()

    def draw(self):
        self.window.fill(Black)
        self.snakes[0].fruit.draw_fruit()
        self.snakes[0].draw_snake()
        pygame.display.update()

    def delay(self):
        self.clock.tick(self.fps)

    @staticmethod
    def end_game():
        pygame.quit()

    def is_running(self):
        return self.run


def main():
    game = Game()
    while game.is_running():
        game.update()
        game.draw()
        game.delay()


if __name__ == '__main__':
    main()
