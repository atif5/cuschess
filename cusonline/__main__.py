
from .chess import *

def main():
    game = OnlineChessGame()
    winner = game.main()
    game.graphicalboard.draw_all()
    pygame.display.flip()
    time.sleep(2)
    if type(winner) is not str:
        print("CusSsss. Checkmate,", winner, "won.")
    else:
        print("CusSsss.", winner)

if __name__ == '__main__':
    main()
