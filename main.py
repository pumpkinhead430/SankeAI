# this branch is the Q learning  branch - normal neural network

from Game import Game


def main():
    game = Game()
    while game.is_running():
        game.update()
        game.draw()
        game.delay()


if __name__ == '__main__':
    main()
