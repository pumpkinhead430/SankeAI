import torch
import random
import numpy as np
from collections import deque
from Game import Game
import pygame
from pygame import Vector2
from CONSTANTS import cell_size, look_size, move_amount
from model import linearQnet, QTrainer
import math
import time

MAX_MEMORY = 100_000
BATCH_SIZE = 500
LR = 0.002
movement_dict = {pygame.K_RIGHT: Vector2(cell_size, 0),
                 pygame.K_LEFT: Vector2(-cell_size, 0),
                 pygame.K_DOWN: Vector2(0, cell_size),
                 pygame.K_UP: Vector2(0, -cell_size)}


class Agent:
    def __init__(self):
        self.n_games = 1
        self.epsilon = 40  # randomness
        self.gamma = 0.6  # discount rate
        self.memory = deque(maxlen=MAX_MEMORY)  # popleft()
        self.model = linearQnet(83, 256, 3)
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)

    @staticmethod
    def get_state(game):
        head = game.snake.head
        '''
        vision = np.zeros(21)
        i = 0
        directions = [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1)] # left, down-left, down...
        for direction in directions:
            direction = Vector2(direction[0], direction[1]) * cell_size
            cur_pos = Vector2(head.x, head.y)

            if direction != game.snake.real_dir.rotate(180):
                while not vision[i]:
                    cur_pos += direction
                    if game.snake.snake_out_of_bounds(cur_pos):
                        vision[i] = (cur_pos.distance_to(head) / cell_size)
                    if cur_pos in game.snake.body:
                        vision[i + 1] = (cur_pos.distance_to(head) / cell_size)
                    if cur_pos == game.fruit.pos:
                        vision[i + 2] = (cur_pos.distance_to(head) / cell_size)
            i = i + 3
        return vision
        '''

        state = np.zeros((look_size, look_size))

        state[int(look_size / 2)][int(look_size / 2)] = 2
        for i in range(state.shape[0]):
            physical_y = i * cell_size + head.y - int(look_size / 2) * cell_size
            for j in range(state.shape[1]):
                physical_x = j * cell_size + head.x - int(look_size / 2) * cell_size
                physical_pos = Vector2(physical_x, physical_y)
                if physical_pos == game.fruit.pos:
                    state[i][j] = 1
                elif game.snake.snake_out_of_bounds(physical_pos):
                    state[i][j] = -1
                elif game.snake.snake_inside(physical_pos):
                    state[i][j] = -1
        life_left = max(move_amount * len(game.snake.body) - game.frame_iteration, 1)

        state = state.flatten()
        state = np.append(state, [head.x - game.fruit.pos.x, head.y - game.fruit.pos.y])

        return np.asarray(state)
        '''
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

        return np.array(state, dtype='int')
        '''

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
        self.epsilon = 100 / math.pow(1.001, self.n_games - 1)
        #self.epsilon = 80 - self.n_games
        self.epsilon = max(5, self.epsilon)

        # self.epsilon -= 1 / 200
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
        if not game_over:
            game.draw()
        game.delay()
        if game_over:
            game.reset()
            agent.n_games += 1
            t0 = time.time()
            agent.train_long_memory()
            print("time passed:", time.time() - t0)
            print('epsilon:', agent.epsilon)
            if record < score:
                record = score
            print(f'Game: {agent.n_games}\nScore: {score}\n record: {record}')


if __name__ == '__main__':
    train()
