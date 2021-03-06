import numpy as np
import pygame
from pygame.math import Vector2

from CONSTANTS import *

movement_dict = {pygame.K_RIGHT: Vector2(cell_size, 0),
                 pygame.K_LEFT: Vector2(-cell_size, 0),
                 pygame.K_DOWN: Vector2(0, cell_size),
                 pygame.K_UP: Vector2(0, -cell_size)}


class Snake:

    def __init__(self, win):
        self.head = Vector2(cell_size * cell_number / 2, cell_size * cell_number / 2)

        self.body = [Vector2(self.head), self.head - Vector2(cell_size, 0),
                     self.head - Vector2(2 * cell_size, 0)]

        self.is_dead = False
        self.win = win
        self.dir = movement_dict[pygame.K_RIGHT]  # input of where the snake wants to go
        self.real_dir = self.dir  # checks if he really go there

    def draw_snake(self):
        inner_block = pygame.Rect(int(self.body[0].x), int(self.body[0].y), cell_size - 10, cell_size - 10)
        block_rect = pygame.Rect(int(self.body[0].x), int(self.body[0].y), cell_size, cell_size)
        pygame.draw.rect(self.win, Blue, block_rect)  # drawing head of snake in blue
        for block in [x for x in self.body if x != self.body[0]]:
            block_rect.x = block.x
            block_rect.y = block.y
            pygame.draw.rect(self.win, Red, block_rect)  # drawing the rest of the snake in red
            inner_block.x = block.x + 5
            inner_block.y = block.y + 5
            pygame.draw.rect(self.win, light_red, inner_block)

    def update_snake(self, food_pos):

        if self.check_direction(self.dir):
            self.real_dir = self.dir

        self.head += self.real_dir
        self.body.insert(0, Vector2(self.head))
        if food_pos != self.head:
            self.body.pop()

        if self.dead():
            self.is_dead = True
            return -1
        return 0

    def change_direction(self, key):

        if movement_dict.get(key):
            self.dir = movement_dict[key]

    def check_direction(self, direction):
        return direction + self.real_dir != Vector2(0, 0)

    def dead(self, pos=None):
        if pos:
            head = pos
        else:
            head = self.head
        if self.snake_out_of_bounds(head):
            return True

        return self.snake_inside(head)

    def snake_inside(self, pos):
        for point in self.body[1:]:
            if pos == point:
                return True
        return False

    @staticmethod
    def snake_out_of_bounds(pos):
        head_rect = pygame.Rect(int(pos.x), int(pos.y), cell_size, cell_size)
        if head_rect.x < 0 or head_rect.y < 0:
            return True

        if head_rect.x + head_rect.width > cell_size * cell_number or \
                head_rect.y + head_rect.height > cell_size * cell_number:
            return True
        return False

    def change_by_action(self, action):
        new_dir_vector = self.dir
        if np.array_equal(action, turn_right):
            new_dir_vector = self.dir.rotate(90)
        elif np.array_equal(action, turn_left):
            new_dir_vector = self.dir.rotate(-90)
        self.dir = new_dir_vector
