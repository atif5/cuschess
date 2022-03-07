
import time
from cuschess.logic import *
import pygame

LIGHTPINK = "#FFC0CB"
PINK = "#FF69B4"
RED = "#FF0000"
WHITE = "#FFFFFF"
BLACK = "#000000"


class BoardGraphical:
    sprites = {
        10: pygame.image.load("cuschess/sprites/wpawn.png"),
        11: pygame.image.load("cuschess/sprites/wrook.png"),
        12: pygame.image.load("cuschess/sprites/wknight.png"),
        13: pygame.image.load("cuschess/sprites/wbishop.png"),
        14: pygame.image.load("cuschess/sprites/wqueen.png"),
        15: pygame.image.load("cuschess/sprites/wking.png"),
        0: pygame.image.load("cuschess/sprites/bpawn.png"),
        1: pygame.image.load("cuschess/sprites/brook.png"),
        2: pygame.image.load("cuschess/sprites/bknight.png"),
        3: pygame.image.load("cuschess/sprites/bbishop.png"),
        4: pygame.image.load("cuschess/sprites/bqueen.png"),
        5: pygame.image.load("cuschess/sprites/bking.png")
    }
    lightpink = pygame.Surface((45, 45))
    pink = pygame.Surface((45, 45))
    white = pygame.Surface((45, 45))
    frame = pygame.image.load("cuschess/sprites/frame.jpg")
    framey = pygame.image.load("cuschess/sprites/framey.jpg")
    lightpink.fill(LIGHTPINK)
    pink.fill(PINK)
    white.fill(WHITE)

    def __init__(self, board, players, selected=None):
        self.board = board
        self.players = players
        self.size = (360, 360)
        self.square_size = (45, 45)
        self.screen = pygame.display.set_mode(self.size)
        self.squares = [1, 0, 1, 0, 1, 0, 1, 0,
                        0, 1, 0, 1, 0, 1, 0, 1,
                        1, 0, 1, 0, 1, 0, 1, 0,
                        0, 1, 0, 1, 0, 1, 0, 1,
                        1, 0, 1, 0, 1, 0, 1, 0,
                        0, 1, 0, 1, 0, 1, 0, 1,
                        1, 0, 1, 0, 1, 0, 1, 0,
                        0, 1, 0, 1, 0, 1, 0, 1]

        self.indicative = []
        self.selected = None

    def highlight_posssible_move(self, x, y, pos):
        if self.board.get_at(x, y):
            self.screen.blit(self.frame, pos)
        else:
            pygame.draw.circle(self.screen, RED,
                               (pos[0]+22.5, pos[1]+22.5), 7)

    def draw_base(self, checkers, plain=False):
        w, h = self.square_size
        for i, square in enumerate(self.squares):
            x, y = i % 8, i//8
            boardpos = (x, y)
            realpos = (x*w, y*w)
            if self.selected and (self.selected.pos == boardpos).all() and not plain:
                self.screen.blit(self.lightpink, realpos)
            elif self.board.get_at(x, y) in checkers and not plain:
                self.screen.blit(self.framey, realpos)
            elif square:
                self.screen.blit(self.white, realpos)
            else:
                self.screen.blit(self.pink, realpos)
            if boardpos in self.indicative and not plain:
                self.highlight_posssible_move(x, y, realpos)

    def walk(self, piece, path):
        sprite = self.sprites[piece.color*10+piece.num]
        for step in path:
            time.sleep(0.006)
            self.screen.fill(BLACK)
            self.screen.fill(WHITE)
            self.draw_base([], plain=True)
            self.draw_pieces(skip_selected=True)
            self.screen.blit(sprite, step)
            pygame.display.flip()

    def animate_movement(self, piece, dpos):
        w, h = self.square_size
        dx, dy = piece.pos[0]-dpos[0], piece.pos[1]-dpos[1]
        if not piece.num == 2:
            if not dx:
                det = (0 < dy).real
                path = [(piece.pos[0]*w, y) for y in range(piece.pos[1]*w,
                                                           dpos[1]*w, 3-6*det)]
            elif piece.pos[1] == dpos[1]:
                det = (0 < dx).real
                path = [(x, piece.pos[1]*w) for x in range(piece.pos[0]*w,
                                                           dpos[0]*w, 3-6*det)]
            else:
                dety = (0 < dy).real
                detx = (0 < dx).real
                path = [(x, y) for x, y in zip(range(piece.pos[0]*w, dpos[0]
                                                     * w, 3-6*detx), range(piece.pos[1]*w, dpos[1]*w, 3-6*dety))]
        else:
            dety = (0 < dy).real
            detx = (0 < dx).real
            detmx = (abs(dy) == 2*abs(dx)).real
            detmy = (not detmx).real
            path = [(x, y) for x, y in zip(range(piece.pos[0]*w, dpos[0]
                                                 * w, (1-2*detx)*(2-1*detmx)), range(piece.pos[1]*w, dpos[1]*w, (1-2*dety)*(2-1*detmy)))]
        path.append((dpos[0]*w, dpos[1]*w))
        self.walk(piece, path)

    def draw_pieces(self, skip_selected=False):
        w, h = self.square_size
        for iy in range(8):
            for ix in range(8):
                rpiece = self.board.get_at(ix, iy)
                pos = (ix*w, iy*w)
                if rpiece:
                    if rpiece == self.selected and skip_selected:
                        continue
                    sprite = self.sprites[rpiece.color*10+rpiece.num]
                    self.screen.blit(sprite, pos)

    def draw_all(self, checkers):
        self.draw_base(checkers)
        self.draw_pieces()

    def select(self, piece, player):
        self.deselect()
        self.selected = piece
        if not piece:
            return
        moves = self.selected.absolute_moves(player.king)
        for i, move in enumerate(moves):
            moves[i] = tuple(move.tolist())

        self.indicative += moves

    def deselect(self):
        self.selected = None
        self.indicative.clear()

    def graphical_select(self, player):
        w, h = self.square_size
        mx, my = pygame.mouse.get_pos()
        boardpos = (int(mx//w), int(my//w))
        if rpiece := self.board.get_at(*boardpos):
            if rpiece.color == player.real:
                self.select(rpiece, player)
            else:
                return

    def graphical_move(self, player):
        w, h = self.square_size
        mx, my = pygame.mouse.get_pos()
        boardpos = (int(mx//w), int(my//w))
        if boardpos not in self.indicative:
            self.deselect()
            self.graphical_select(player)
            return
        self.animate_movement(self.selected, boardpos)
        player.make_move(self.selected, boardpos)
        self.deselect()
        return True
