import pygame
from CONSTANTS import *
from Snake import Snake
from Fruit import Fruit


def change_random(agent):
    agent.is_random = not agent.is_random
    if agent.is_random:
        print('random is now turned on')
    else:
        print('random is now turned off')


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
        self.font = pygame.font.SysFont('arial', 30, True, False)
        self.scoreText = self.font.render(str(self.score), False, White, Black)
        self.run = True
        self.snake = Snake(self.window)
        self.fruit = Fruit(self.window, self.snake.body)
        self.previous_dist = self.snake.head.distance_to(self.fruit.pos)

    def reset(self):
        self.score = 0
        self.game_over = False
        self.snake = Snake(self.window)
        self.fruit = Fruit(self.window, self.snake.body)
        self.previous_dist = self.snake.head.distance_to(self.fruit.pos)
        self.frame_iteration = 0
        self.scoreText = self.font.render(str(self.score), True, White)

    def update(self, agent, action=straight):
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
                if event.key == pygame.K_q:
                    change_random(agent)

        self.frame_iteration += 1
        self.snake.change_by_action(action)
        current_length = len(self.snake.body)
        self.snake.update_snake(self.fruit.pos)
        if len(self.snake.body) > current_length:
            self.score += 1
            self.scoreText = self.font.render(str(self.score), True, White)
        reward = 0
        distance = self.snake.head.distance_to(self.fruit.pos)

        if self.frame_iteration > move_amount * len(self.snake.body):
            self.snake.is_dead = True

        if self.snake.is_dead:
            self.game_over = True
            reward = -100
            return reward, self.game_over, self.score

        if self.snake.head == self.fruit.pos:
            self.fruit = Fruit(self.window, self.snake.body)
            self.previous_dist = self.snake.head.distance_to(self.fruit.pos)
            reward = 50
            return reward, self.game_over, self.score

        if self.previous_dist < distance:
            reward = -1
            self.previous_dist = distance
            return reward, self.game_over, self.score

        if self.previous_dist > distance:
            reward = 1
            self.previous_dist = distance
            return reward, self.game_over, self.score

        return reward, self.game_over, self.score

    def draw(self):
        self.window.fill(Black)
        self.fruit.draw_fruit()
        self.snake.draw_snake()
        self.draw_score()
        pygame.display.update()

    def delay(self):
        self.clock.tick(self.fps)

    @staticmethod
    def end_game():
        pygame.quit()

    def is_running(self):
        return self.run

    def draw_score(self):
        self.window.blit(self.scoreText, self.scoreText.get_rect())
