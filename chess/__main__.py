
from .chess import *
import cuschess

def wait():
    time.sleep(0.5)

def main(screen):
    game = ChessGame(screen)
    winner = game.main()
    game.graphicalboard.draw_all(game.checkers)
    pygame.display.flip()
    time.sleep(2)
    if type(winner) is not str:
        maint = f"CusSsss. Checkmate, {winner}, won."
    else:
        maint = f"CusSsss, {winner}"

    widgets = [
        InformingText((0, 40), maint, 20, LIGHTPINK, midst=True, screen=screen),
        InformingText((0, 120), "Play again?", 30, LIGHTPINK, midst=True, screen=screen),
        Option((86, 200), "Yes", 30, LIGHTPINK,
               {main: [screen]}),
        Option((222, 200), "No", 30, LIGHTPINK,
               {wait: []}),
        
        ]
    try_again = Menu(BLACK, widgets, screen)
    try_again.init_enders(["No", "Yes"])
    print(widgets[2].ssize)
    print(widgets[3].ssize)
    try_again.draw()


if __name__ == '__main__':
    main()
