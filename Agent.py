import torch
import random
import numpy as np
from collections import deque
from Game import Game
import pygame
from pygame import Vector2
from CONSTANTS import cell_size, straight, turn_right, turn_left
from model import linearQnet, QTrainer
import math
import time
MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001
movement_dict = {pygame.K_RIGHT: Vector2(cell_size, 0),
                 pygame.K_LEFT: Vector2(-cell_size, 0),
                 pygame.K_DOWN: Vector2(0, cell_size),
                 pygame.K_UP: Vector2(0, -cell_size)}


class Agent:
    def __init__(self):
        self.n_games = 1
        self.epsilon = 40  # randomness
        self.gamma = 0.9  # discount rate
        self.memory = deque(maxlen=MAX_MEMORY)  # popleft()
        self.model = linearQnet(11, 256, 3)
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)

    @staticmethod
    def get_state(game):
        head = game.snake.head

        state = [
            game.snake.dead(head + game.snake.real_dir),  # check if danger straight
            game.snake.dead(head + game.snake.real_dir.rotate(90)),  # check if danger right
            game.snake.dead(head + game.snake.real_dir.rotate(-90)),  # check if danger left

            game.snake.real_dir == movement_dict[pygame.K_LEFT],
            game.snake.real_dir == movement_dict[pygame.K_RIGHT],
            game.snake.real_dir == movement_dict[pygame.K_UP],
            game.snake.real_dir == movement_dict[pygame.K_DOWN],

            game.fruit.pos.x < game.snake.head.x,
            game.fruit.pos.x > game.snake.head.x,
            game.fruit.pos.y < game.snake.head.y,
            game.fruit.pos.y > game.snake.head.y,

        ]

        return np.array(state, dtype=int)

    def remember(self, state, action, reward, next_state, game_over):
        self.memory.append((state, action, reward, next_state, game_over))

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE)  # list of tuples
        else:
            mini_sample = self.memory
        states, actions, rewards, next_states, game_overs = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, game_overs)

    def train_short_memory(self, state, action, reward, next_state, game_over):
        self.trainer.train_step(state, action, reward, next_state, game_over)

    def get_action(self, state):
        self.epsilon = 100 / math.pow(1.01, self.n_games - 5)
        action = [0, 0, 0]
        if random.uniform(0, 100) < self.epsilon:
            move = random.randint(0, 2)
            action[move] = 1
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()
            action[move] = 1
        return action


def train():
    plot_mean_score = []
    record = 0
    agent = Agent()
    game = Game()
    while game.is_running():

        state_old = agent.get_state(game)

        action = agent.get_action(state_old)
        reward, game_over, score = game.update(action)
        state_new = agent.get_state(game)
        agent.train_short_memory(state_old, action, reward, state_new, game_over)
        agent.remember(state_old, action, reward, state_new, game_over)

        game.draw()
        game.delay()
        if game_over:
            game.reset()
            agent.n_games += 1
            t0 = time.time()
            agent.train_long_memory()
            print("time passed:", time.time() - t0)
            if record < score:
                record = score
            print(f'Game: {agent.n_games}\nScore: {score}\n record: {record}')


if __name__ == '__main__':
    train()