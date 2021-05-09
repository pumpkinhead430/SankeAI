import sys

import torch
from Game import Game
from Mode import Mode
from model import linearQnet
from Agent import Agent
from CONSTANTS import AI_FPS


def trained():
    path = sys.argv[1]
    model = linearQnet(11, 256, 3)
    try:
        model.load(path)
    except FileNotFoundError:
        print('could not find model, loading an uninitialized model instead')
    game = Game(Mode.MODEL, AI_FPS)
    while game.is_running():
        state = Agent.get_state(game)
        reward, game_over, score = game.update(action=get_prediction(state, model))
        if not game_over:
            game.draw()
        game.delay()
        if game_over:
            game.reset()


def get_prediction(state, model):
    action = [0, 0, 0]
    state0 = torch.tensor(state, dtype=torch.float)
    prediction = model(state0)
    move = torch.argmax(prediction).item()
    action[move] = 1
    return action


if __name__ == '__main__':
    trained()
