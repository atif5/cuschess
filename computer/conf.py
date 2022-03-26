
from .chess import *
from stockfish import Stockfish
from platform import system

platform_ = system()

if platform_ == "Linux":
    ENGINE_PATH = "cuschess/computer/stockfish/stockfish_14.1_linux_x64"
elif platform_ == "Windows":
    ENGINE_PATH = "cuschess/computer/stockfish/stockfish_14.1_win_x64.exe"

ENGINE = Stockfish(path=ENGINE_PATH)
PLAYER_COLOR = None


def set_diff(level): ENGINE.set_skill_level(level)


def set_color(color):
    global PLAYER_COLOR
    PLAYER_COLOR = color


widgets1 = [
    InformingText((0, 30), "Choose your difficulty", 30, PINK,
                  midst=True, leng=360),
    Option((0, 80), "Easy", 30, LIGHTPINK,
           {set_diff: [1]}, midst=True, leng=360),
    Option((0, 120), "Medium", 30, LIGHTPINK,
           {set_diff: [6]}, midst=True, leng=360),
    Option((0, 160), "Hard", 30, LIGHTPINK,
           {set_diff: [15]}, midst=True, leng=360),
    Option((0, 200), "Cuss", 30, LIGHTPINK,
           {set_diff: [20]}, midst=True, leng=360)]

widgets2 = [
    InformingText((0, 30), "Choose your color", 30, PINK,
                  midst=True, leng=360),
    Option((20, 80), "White", 30, WHITE,
           {set_color: [1]}, midst=True, leng=360),
    Option((40, 120), "Black", 30, BLACK,
           {set_color: [0]}, midst=True, leng=360, high_color=BLACK)]


def configure(screen):
    color = Menu(VIOLET, widgets2)
    color.init_enders(["White", "Black"])
    diff = Menu(VIOLET, widgets1)
    diff.init_enders(["Easy", "Medium", "Hard", "Cuss"])
    color.draw(screen)
    diff.draw(screen)
    game = ComputerChessGame(screen, ENGINE, PLAYER_COLOR)

    return game
