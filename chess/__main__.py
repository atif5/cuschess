
from .chess import *
import cuschess


def wait():
    time.sleep(0.000000000001)


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
        InformingText((0, 40), maint, 20, LIGHTPINK, midst=True, leng=360),
        InformingText((0, 120), "Play again?", 30,
                      LIGHTPINK, midst=True, leng=360),
        Option((86, 200), "Yes", 30, LIGHTPINK,
               {main: [screen]}),
        Option((222, 200), "No", 30, LIGHTPINK,
               {wait: []}),

    ]
    try_again = Menu(VIOLET, widgets)
    try_again.init_enders(["No", "Yes"])
    try_again.draw(screen)


if __name__ == '__main__':
    main()
