import pygame
import itertools
from pygame.math import Vector2
import numpy as np
from CONSTANTS import *
from Brain import Brain
from Fruit import Fruit
import time

movement_dict = {pygame.K_RIGHT: Vector2(cell_size, 0),
                 pygame.K_LEFT: Vector2(-cell_size, 0),
                 pygame.K_DOWN: Vector2(0, cell_size),
                 pygame.K_UP: Vector2(0, -cell_size)}
num_to_key = {0: pygame.K_RIGHT,
              1: pygame.K_LEFT,
              2: pygame.K_DOWN,
              3: pygame.K_UP}


def get_quarter(point):
    if point.x >= 0 and point.y >= 0:
        return 0
    if point.x <= 0 and point.y >= 0:
        return 1
    if point.x <= 0 and point.y <= 0:
        return 2
    if point.x >= 0 and point.y <= 0:
        return 3
    return -1


class Snake:

    def __init__(self, win):
        self.body = [Vector2(cell_size * cell_number / 2, cell_size * cell_number / 2),
                     Vector2(cell_size * cell_number / 2 - 1, cell_size * cell_number / 2 - 1)]

        self.current_place = 0
        self.score = 1
        self.life_time = 0
        self.moves_left = starting_moves
        self.brain = Brain()
        self.fitness = 0
        self.fruit = Fruit(win, self.body, 0)
        self.is_dead = False
        self.win = win
        self.dir = pygame.K_RIGHT
        self.real_dir = self.dir

    def draw_snake(self):
        block_rect = pygame.Rect(int(self.body[0].x), int(self.body[0].y), cell_size, cell_size)

        for block in self.body:
            block_rect.x = block.x
            block_rect.y = block.y
            pygame.draw.rect(self.win, Red, block_rect)

    def update_snake(self):
        if self.dead():
            self.is_dead = True
            return -1
        if self.check_direction(self.dir):
            self.real_dir = self.dir

        for i in range(len(self.body) - 1, 0, -1):
            self.body[i].x = self.body[i - 1].x
            self.body[i].y = self.body[i - 1].y

        self.body[0] += movement_dict[self.real_dir]
        self.life_time += 1
        self.moves_left -= 1
        if self.moves_left == 0:
            self.is_dead = True
            return -1
        return 0

    def change_direction(self, key):

        if movement_dict.get(key):
            self.dir = key
            return

    def enlarge_snake(self):
        new_block = Vector2()
        new_block.xy = self.body[-1].xy

        self.body.append(new_block)

    def check_direction(self, key):
        return movement_dict[key] + movement_dict[self.real_dir] != Vector2(0, 0)

    def on_fruit(self):
        snake_rect = pygame.Rect(self.body[0].x, self.body[0].y, cell_size, cell_size)
        fruit_rect = pygame.Rect(self.fruit.pos.x, self.fruit.pos.y, cell_size, cell_size)
        return snake_rect.colliderect(fruit_rect)

    def new_fruit(self):
        if self.current_place:
            self.current_place = 0
        else:
            self.current_place = 1
        self.fruit = Fruit(self.win, self.body, self.current_place)
        self.moves_left += 50

    def dead(self):
        if self.snake_out_of_bounds(self.body[0]):
            return True

        for i in range(1, len(self.body)):
            if self.body[0] == self.body[i]:
                return True

        return False

    def think(self):
        self.brain.think()
        temp_lst = list(self.brain.output_layer.output)
        temp = max(temp_lst)
        direction = temp_lst.index(temp)
        self.dir = num_to_key[direction]

    def reset(self):
        self.body = [Vector2(cell_size * cell_number / 2, cell_size * cell_number / 2),
                     Vector2(cell_size * cell_number / 2 - 1, cell_size * cell_number / 2 - 1)]

        self.current_place = 0
        self.fruit = Fruit(self.win, self.body, 0)
        self.is_dead = False
        self.moves_left = starting_moves
        self.life_time = 0
        self.score = 1
        self.dir = pygame.K_RIGHT
        self.real_dir = pygame.K_RIGHT

    def inc_score(self):
        self.score += 1
        self.fitness += pow(self.moves_left, 2)

    def calculate_fitness(self):
        self.fitness = 0
        if self.score < risk_rate:
            self.fitness += pow(self.score, 3) * self.life_time
        else:
            self.fitness += pow(2, 10) * pow(self.life_time, 2) * (self.score - risk_rate - 1)

        if self.moves_left <= 0:
            self.fitness -= 10

    def look(self):
        input_lst = []
        '''
        for i in range(round(self.body[0].y - (look_size * cell_size)), round(self.body[0].y + look_size * cell_size), cell_size):
            for j in range(round(self.body[0].x - (look_size * cell_size)), round(self.body[0].x + look_size * cell_size), cell_size):
                vec = Vector2(j, i)
                if vec == self.fruit.pos:
                    input_lst.append(1)
                elif vec in self.body:
                    input_lst.append(-1)
                elif self.snake_out_of_bounds(vec):
                    input_lst.append(-1)
                else:
                    input_lst.append(0)
        arr = np.array(input_lst)
        arr.shape = (2 * look_size, 2 * look_size)

        input_lst.append(10 / self.body[0].distance_to(self.fruit.pos))
        input_lst.append(self.body[0].angle_to(self.fruit.pos))
        '''
        input_lst.extend(self.info_in_direction(self.body[0], Vector2(0, cell_size)))
        input_lst.extend(self.info_in_direction(self.body[0], Vector2(0, -cell_size)))
        input_lst.extend(self.info_in_direction(self.body[0], Vector2(cell_size, cell_size)))
        input_lst.extend(self.info_in_direction(self.body[0], Vector2(cell_size, -cell_size)))
        input_lst.extend(self.info_in_direction(self.body[0], Vector2(-cell_size, cell_size)))
        input_lst.extend(self.info_in_direction(self.body[0], Vector2(-cell_size, -cell_size)))
        input_lst.extend(self.info_in_direction(self.body[0], Vector2(cell_size, 0)))
        input_lst.extend(self.info_in_direction(self.body[0], Vector2(-cell_size, 0)))

        self.brain.inputs = np.array(input_lst)

    def get_food_direction_index(self):
        fruit_direction = self.fruit.pos - self.body[0]
        if fruit_direction.x == 0:
            if fruit_direction.y > 0:
                return 0
            return 1

        if fruit_direction.y == 0:
            if fruit_direction.x > 0:
                return 2
            return 3

        if fruit_direction.x == fruit_direction.y:
            if fruit_direction.x < 0:
                return 4
            return 5

        if fruit_direction.x == -fruit_direction.y:
            if fruit_direction.x < 0:
                return 6
            return 7
        return -1

    @staticmethod
    def snake_out_of_bounds(pos):
        head_rect = pygame.Rect(int(pos.x), int(pos.y), cell_size, cell_size)
        if head_rect.x < 0 or head_rect.y < 0:
            return True

        if head_rect.x + head_rect.width > cell_size * cell_number or \
                head_rect.y + head_rect.height > cell_size * cell_number:
            return True
        return False

    def info_in_direction(self, pos, direction):
        copy_pos = Vector2(0, 0)
        copy_pos.x = pos.x
        copy_pos.y = pos.y
        distance = 0
        food_found = False
        body_found = False
        vision = np.zeros(3)
        while not self.snake_out_of_bounds(copy_pos):
            copy_pos += direction
            distance += 1
            if not food_found and copy_pos == self.fruit.pos:
                food_found = True
                vision[0] = 1

            if not body_found and copy_pos in self.body:
                body_found = True
                vision[1] = -1
        if distance == 0:
            distance = 1
        vision[2] = 10 / distance
        return vision

