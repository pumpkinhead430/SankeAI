from Game import Game
from Mode import Mode


def human():
    game = Game(Mode.HUMAN)
    while game.is_running():
        reward, game_over, score = game.update()
        game.draw()
        game.delay()
        if game_over:
            game.reset()


if __name__ == '__main__':
    human()
