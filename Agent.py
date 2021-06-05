import torch
import random
import numpy as np
from collections import deque
from Game import Game
import pygame
import sys
from pygame import Vector2
from CONSTANTS import cell_size, AI_FPS
from Mode import Mode
from model import linearQnet, QTrainer
import matplotlib.pyplot as plt
import time

MAX_MEMORY = 100_000
BATCH_SIZE = 500
LR = 0.002
movement_dict = {pygame.K_RIGHT: Vector2(cell_size, 0),
                 pygame.K_LEFT: Vector2(-cell_size, 0),
                 pygame.K_DOWN: Vector2(0, cell_size),
                 pygame.K_UP: Vector2(0, -cell_size)}


class Agent:
    def __init__(self, decay_rate=80):
        self.n_games = 1
        self.is_random = True
        self.epsilon = 100  # randomness
        self.decay_rate = 100 / decay_rate
        self.gamma = 0.6  # discount rate
        self.memory = deque(maxlen=MAX_MEMORY)  # popleft()
        self.model = linearQnet(11, 256, 3)
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)

    @staticmethod
    def get_state(game):
        """
        makes the vision of the snake
        :param game: the main game
        :return: the vision of the snake
        """
        head = game.snake.head
        state = [
            game.snake.dead(head + game.snake.real_dir),  # check if danger straight
            game.snake.dead(head + game.snake.real_dir.rotate(90)),  # check if danger right
            game.snake.dead(head + game.snake.real_dir.rotate(-90)),  # check if danger left

            # -----------------------------------------------------
            game.snake.real_dir == movement_dict[pygame.K_LEFT],
            game.snake.real_dir == movement_dict[pygame.K_RIGHT],  # shows the snake witch direction he is in
            game.snake.real_dir == movement_dict[pygame.K_UP],
            game.snake.real_dir == movement_dict[pygame.K_DOWN],
            # ----------------------------------------------------
            game.fruit.pos.x < game.snake.head.x,
            game.fruit.pos.x > game.snake.head.x,
            game.fruit.pos.y < game.snake.head.y,  # shows the snake where the fruit is
            game.fruit.pos.y > game.snake.head.y,

        ]

        return np.array(state, dtype='int')

    def remember(self, state, action, reward, next_state, game_over):
        self.memory.append((state, action, reward, next_state, game_over))

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:  # if memory is too big, it will chose just a sample from the memory
            mini_sample = random.sample(self.memory, BATCH_SIZE)  # list of tuples
        else:
            mini_sample = self.memory
        states, actions, rewards, next_states, game_overs = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, game_overs)

    def train_short_memory(self, state, action, reward, next_state, game_over):
        self.trainer.train_step(state, action, reward, next_state, game_over)

    def get_action(self, state):
        action = [0, 0, 0]

        if self.is_random and random.uniform(0, 100) < self.epsilon:
            move = random.randint(0, 2)
            action[move] = 1
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()
            action[move] = 1
        return action

    def update_epsilon(self):
        self.epsilon -= self.decay_rate
        self.epsilon = max(self.epsilon, 5)


def plot_game_status(plot_games, plot_rewards, plot_scores, plot_mean_scores):
    plt.cla()
    plt.plot(plot_games, plot_rewards, label="rewards")
    plt.plot(plot_games, plot_scores, label="scores")
    plt.plot(plot_games, plot_mean_scores, label="average scores")
    plt.legend()
    plt.draw()
    plt.pause(0.001)


def train():
    plot_scores = []
    plot_mean_scores = []
    plot_games = []
    total_reward = 0
    plot_rewards = []
    total_score = 0
    record = 0
    if len(sys.argv) > 1:
        decay_rate = sys.argv[1]
    else:
        decay_rate = '80'
    if decay_rate.isnumeric():
        agent = Agent(int(decay_rate))
    else:
        agent = Agent()
    game = Game(Mode.TRAIN, AI_FPS)
    while game.is_running():

        state_old = agent.get_state(game)

        action = agent.get_action(state_old)
        reward, game_over, score = game.update(action, agent)
        total_reward += reward
        state_new = agent.get_state(game)
        agent.train_short_memory(state_old, action, reward, state_new, game_over)
        agent.remember(state_old, action, reward, state_new, game_over)
        if not game_over:
            game.draw()
        game.delay()
        if game_over:
            game.reset()
            agent.n_games += 1
            agent.update_epsilon()
            t0 = time.time()
            agent.train_long_memory()
            if record < score:
                record = score
                agent.model.save('record_model.pth')
            print("time passed:", time.time() - t0)
            print("epsilon: {:.2f}".format(agent.epsilon))
            print(f'Game: {agent.n_games}\nScore: {score}\n record: {record}')

            plot_games.append(agent.n_games)
            plot_scores.append(score)
            plot_rewards.append(total_reward / 1000)
            total_reward = 0
            total_score += score
            mean_score = total_score / agent.n_games
            plot_mean_scores.append(mean_score)
            plot_game_status(plot_games, plot_rewards, plot_scores, plot_mean_scores)
    agent.model.save('last_model.pth')


if __name__ == '__main__':
    train()


