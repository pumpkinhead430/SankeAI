import random
import threading
import pygame
from pygame.math import Vector2
from CONSTANTS import *


def all_clear_positions(snake_body):
    free_pos = []
    for i in range(0, cell_number):
        for j in range(0, cell_number):
            if Vector2(j * cell_size, i * cell_size) not in snake_body:
                free_pos.append(Vector2(j * cell_size, i * cell_size))
    return free_pos


class Fruit:
    def __init__(self, win, snake_body, place):
        free_pos = all_clear_positions(snake_body)
        self.pos = free_pos[random.randint(0, len(free_pos) - 1)]
        # self.pos = Vector2(cell_size * random.randint(0, cell_number - 1), cell_size * random.randint(0, cell_number - 1))
        '''
        if place:
            self.pos = Vector2(3 * cell_size, 5 * cell_size)
        else:
            self.pos = Vector2(5 * cell_size, 3 * cell_size)
        '''
        self.win = win

    def draw_fruit(self):
        fruit_rect = pygame.Rect(int(self.pos.x), int(self.pos.y), cell_size, cell_size)
        pygame.draw.rect(self.win, Green, fruit_rect)

    def make_position(self, snake_body):
        free_pos = all_clear_positions(snake_body)
        self.pos = free_pos[random.randint(0, len(free_pos))]
