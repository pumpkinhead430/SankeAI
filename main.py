# this branch is the Q learning  branch - changing states available

from Game import Game


def main():
    game = Game()
    while game.is_running():
        reward, game_over, score = game.update()
        game.draw()
        game.delay()
        if game_over:
            game.reset()


if __name__ == '__main__':
    main()
