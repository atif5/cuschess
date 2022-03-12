import sys
import os
import time
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
from .menu import ModeOption
import cuschess.cusonline.__main__ as online
import cuschess.computer.__main__ as comp
import cuschess.cuserver.server as serv
import cuschess.chess.__main__ as twoplayer
from cuschess.chess.graphical import LIGHTPINK


def main():
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((360, 360))
    options = [ModeOption((116, 80), "2 Player", 15, LIGHTPINK, twoplayer.main), 
               ModeOption((34, 120), "With the Computer", 15, LIGHTPINK, comp.main),
               ModeOption((129, 160), "Online", 15, LIGHTPINK, online.main),
               ModeOption((82, 200), "Run a server", 15, LIGHTPINK, serv.main)]
    while True:
        pygame.event.pump()
        for option in options:
            option.exist(screen)
        pygame.display.flip()
        clock.tick(60)


if __name__ == '__main__':
    main()
