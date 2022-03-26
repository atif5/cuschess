
from cuschess import LIGHTPINK, PINK, BLACK
import cuschess.chess.__main__ as twoplayer
import cuschess.cuserver.server as serv
import cuschess.computer.__main__ as comp
import cuschess.cusonline.__main__ as online
import pygame
import sys
import time
from .menu import *


screen = pygame.display.set_mode((360, 360))


def main():
    global screen
    widgets = [
        InformingText((0, 20), "CusChess", 40, PINK,
                      midst=True, leng=360),
        Option((116, 80), "2 Player", 30, LIGHTPINK,
               {twoplayer.main: [screen]}, midst=True, leng=360),
        Option((34, 120), "With the Computer", 30,
               LIGHTPINK, {comp.main: [screen]}, midst=True, leng=360),
        Option((129, 160), "Online", 30, LIGHTPINK, {
               online.main: [screen], }, midst=True, leng=360),
        Option((82, 200), "Run a server", 30,
               LIGHTPINK, {serv.main: []}, midst=True, leng=360),
        Option((147, 240), "Quit", 30, LIGHTPINK, {exit: []}, midst=True, leng=360)]

    cuschessmenu = Menu(VIOLET, widgets)
    cuschessmenu.draw(screen)


if __name__ == '__main__':
    main()
