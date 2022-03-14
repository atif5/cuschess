from cuschess.chess.graphical import LIGHTPINK, PINK
import cuschess.chess.__main__ as twoplayer
import cuschess.cuserver.server as serv
import cuschess.computer.__main__ as comp
import cuschess.cusonline.__main__ as online
from .menu import *
import pygame
import sys
import time
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"


def main():
    screen = pygame.display.set_mode((360, 360))
    widgets = [
               InformingText((79, 20), "CusChess", 40, PINK),
               Option((116, 80), "2 Player", 30, LIGHTPINK, {twoplayer.main: [screen]}),
               Option((34, 120), "With the Computer", 30,
                          LIGHTPINK, {comp.main: [screen]}),
               Option((129, 160), "Online", 30,
                          LIGHTPINK, {online.main: [screen]}),
               Option((82, 200), "Run a server", 30,
                          LIGHTPINK, {serv.main: []}),
               Option((147, 240), "Quit", 30, LIGHTPINK, {exit: []})]

    cuschessmenu = Menu((0, 0, 0), widgets, screen)
    cuschessmenu.draw()


if __name__ == '__main__':
    main()
