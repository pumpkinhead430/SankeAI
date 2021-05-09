from Game import Game
from Mode import Mode
from CONSTANTS import HUMAN_FPS


def human():
    game = Game(Mode.HUMAN, HUMAN_FPS)
    while game.is_running():
        reward, game_over, score = game.update()
        if not game_over:
            game.draw()
        game.delay()
        if game_over:
            game.reset()


if __name__ == '__main__':
    human()
