
from .chess import *

def main(screen):
    game = ChessGame(screen)
    winner = game.main()
    game.graphicalboard.draw_all(game.checkers)
    pygame.display.flip()
    time.sleep(2)
    if type(winner) is not str:
        print("CusSsss. Checkmate,", winner, "won.")
    else:
        print("CusSsss.", winner)
    
    screen.fill(WHITE)
    screen.fill(BLACK)

if __name__ == '__main__':
    main()
