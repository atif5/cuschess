
import numpy
import random

VALID = range(8)
numpFALSE = numpy.array((False, False))
movelist = [
    [[(0, 1), (1, 1), (-1, 1)], [(0, -1), (1, -1), (-1, -1)]],  # pawn
    [(1, 0), (-1, 0), (0, 1), (0, -1)],  # rook
    [(-1, -2), (1, -2), (2, -1), (2, 1), (1, 2),
     (-1, 2), (-2, 1), (-2, -1)],  # knight
    [(1, 1), (1, -1), (-1, 1), (-1, -1)],  # bishop
    [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1),
     (1, -1), (-1, 1), (-1, -1)],  # queen
    [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1),
     (1, -1), (-1, 1), (-1, -1)]  # king
]


class Piece:
    def __init__(self, board, pos, num, color):
        global movelist
        self.board = board
        self.pos = numpy.array(pos)
        self.num = num
        if not self.num:
            self.skipped = False
        self.color = color
        self.opp_color = (not self.color).real
        self.movelist = movelist[self.num]
        self.moved = False
        self.name = self.board.pieces[self.num]
        if self.color:
            self.name = self.name.capitalize()

    def __repr__(self):
        repr_ = f"{self.name} at pos: {self.pos}"
        return repr_

    def __str__(self):
        return self.__repr__()

    def en_passant(self):
        x, y = self.pos
        if x-1 in VALID:
            if rpiece := self.board.get_at(x-1, y):
                if not rpiece.num:
                    if rpiece.skipped:
                        return numpy.array((x-1, y+1-2*self.color))
        if x+1 in VALID:
            if rpiece := self.board.get_at(x+1, y):
                if not rpiece.num:
                    if rpiece.skipped:
                        return numpy.array((x+1, y+1-2*self.color))
        return numpFALSE

    def absolute_moves(self, king):
        return list(filter(lambda move: self.is_safe(move, king),
                           list(self.possible_moves())))

    def possible_moves(self, castling=True):
        if self.num in [1, 3, 4]:
            return list(self.possible_moves_rbq())
        elif self.num == 0:
            return list(self.possible_moves_pawn())
        elif self.num == 2:
            return list(self.possible_moves_knight())
        elif self.num == 5:
            return list(self.possible_moves_king(castling=castling))

    def possible_moves_rbq(self):
        for direction in self.movelist:
            possible_pos = self.pos.copy()
            possible_pos += direction
            x, y = possible_pos

            while (x in VALID) and (y in VALID):
                if bpiece := self.board.get_at(x, y):
                    if bpiece.color != self.color:
                        yield numpy.array(possible_pos)
                    break

                yield numpy.array(possible_pos)

                possible_pos += direction
                x, y = possible_pos

    def possible_moves_pawn(self):
        if self.num != 0:
            return
        specific_movelist = self.movelist[self.color]

        for i, move in enumerate(specific_movelist):
            possible_pos = self.pos.copy()
            possible_pos += move
            if not i:
                first_step = possible_pos
            x, y = possible_pos
            if not (x in VALID and y in VALID):
                continue
            rpiece = self.board.get_at(x, y)

            if bool(rpiece).real ^ bool(not i).real:
                if rpiece:
                    if rpiece.color != self.color:
                        yield numpy.array(possible_pos)
                    continue
                yield numpy.array(possible_pos)

        if (magicmove := self.en_passant()).any():
            yield magicmove

        if not self.moved:
            x, y = self.pos
            extra_step = (x, y+2-4*self.color)
            if not (self.board.get_at(*extra_step) or self.board.get_at(*first_step)):
                yield numpy.array(extra_step)

    def possible_moves_knight(self):
        if self.num != 2:
            return

        for hop in self.movelist:
            possible_pos = self.pos.copy()
            possible_pos += hop
            x, y = possible_pos

            if (x in VALID) and (y in VALID):
                if bpiece := self.board.get_at(x, y):
                    if bpiece.color != self.color:
                        yield numpy.array(possible_pos)
                    continue
                yield numpy.array(possible_pos)

    def possible_moves_king(self, castling):
        if self.num != 5:
            return
        for direction in self.movelist:
            possible_pos = self.pos.copy()
            possible_pos += direction
            x, y = possible_pos

            if (x in VALID) and (y in VALID):
                if bpiece := self.board.get_at(x, y):
                    if bpiece.color != self.color:
                        yield numpy.array(possible_pos)
                    continue

                yield numpy.array(possible_pos)

        x, y = self.pos
        if castling:
            if self.can_castle():
                yield numpy.array((x+2, y))
            if self.can_castle(right_side=False):
                yield numpy.array((x-2, y))

    def can_castle(self, right_side=True):
        if self.num != 5:
            return False

        if self.moved:
            return False

        x, y = self.pos
        castle_squares = [(x+i, y)
                          for i in range(-2+2*right_side.real, 1+2*right_side.real)]
        for square in castle_squares:
            if rpiece := not self.is_safe(square, self) or self.board.get_at(*square):
                if rpiece is self:
                    continue
                return False

        if not right_side and self.board.get_at(x-3, y):
            return False

        return True

    def is_incheck(self):
        if self.num != 5:
            return

        checkers = list()

        for line in self.board.internal:
            for piece in line:
                if not piece:
                    continue

                if piece.color == self.opp_color:
                    possible_moves = piece.possible_moves(castling=False)
                    for pos in possible_moves:
                        if (self.pos == pos).all():
                            if not checkers:
                                checkers.append(self)
                            checkers.append(piece)

        return checkers

    def is_safe(self, move, king):
        ipos = self.pos
        rpiece = self.board.get_at(*move)
        self.board.move(self.pos, move, test=True)
        det = king.is_incheck()
        self.board.undo(ipos, move, item=rpiece)
        return not det

    def notpos(self):
        return self.board.notpos(self.pos)


class Board:
    def __init__(self):
        self.pieces = ["p", "r", "n", "b", "q", "k"]
        order = [1, 2, 3, 4, 5, 3, 2, 1]

        first_line = [Piece(self, (i, 0), order[i], color=0) for i in range(8)]
        second_line = [Piece(self, (i, 1), 0, color=0) for i in range(8)]

        seventh_line = [Piece(self, (i, 6), 0, color=1) for i in range(8)]
        eight_line = [Piece(self, (i, 7), order[i], color=1) for i in range(8)]

        self.internal = [
            first_line,
            second_line,
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            seventh_line,
            eight_line]

        self.letters = "abcdefgh"

    def __str__(self):
        str_ = ""
        for line in self.internal:
            for piece in line:
                if piece:
                    str_ += str(piece.num+1)+' '
                else:
                    str_ += str(piece)+' '
            str_ += '\n'

        return str_

    def get_at(self, x, y):
        return self.internal[y][x]

    def notget_at(self, notation):
        pos = self.nottoreal(notation)
        return self.get_at(*pos)

    def empty_at(self, x, y):
        self.internal[y][x] = 0

    def change_at(self, x, y, item):
        self.internal[y][x] = item

    def move(self, spos, dpos, test=False):
        piece = self.get_at(*spos)
        self.empty_at(*piece.pos)
        piece.pos = numpy.array(dpos)
        x, y = piece.pos
        bpiece = self.get_at(x, y)
        self.change_at(x, y, piece)
        if not test:
            if not piece.moved:
                if not piece.num:
                    if abs(spos[1] - dpos[1]) == 2:
                        piece.skipped = True
                piece.moved = True
            if not piece.num:
                if not y or y == 7:
                    self.promote(piece)
            return bpiece

    def castle(self, king, right_side=True):
        ix, iy = king.pos
        self.move(king.pos, (ix-2+4*right_side.real, iy))
        x, y = king.pos
        rrook = self.get_at(ix-4+7*right_side.real, iy)
        self.move(rrook.pos, (x+1-2*right_side.real, iy))

    def en_passant(self, pawn, move):
        x, y = move
        self.move(pawn.pos, move)
        self.empty_at(x, y-1+2*pawn.color)

    def undo(self, spos, dpos, item=0):
        rpiece = self.get_at(*dpos)
        self.change_at(*dpos, item)
        rpiece.pos = numpy.array(spos)
        self.change_at(*spos, rpiece)

    def promote(self, pawn):
        promotion = Piece(
            self, pawn.pos, 4, pawn.color)
        self.change_at(*pawn.pos, promotion)

    def notpos(self, pos):
        x, y = pos
        return self.letters[x]+str(abs((y-7))+1)

    def nottoreal(self, notation):
        x, y = notation
        y = int(y)
        if y-1 not in VALID or x not in self.letters:
            return
        return (self.letters.index(x), abs(y-8))

    def FEN(self):
        fen = str()
        i = 0
        for line in self.internal:
            for piece in line:
                if piece:
                    if i:
                        fen += str(i)
                    fen += piece.name
                    i = 0
                else:
                    i += 1
            if i:
                fen += str(i)
                i = 0
            fen += '/'
        return fen[:-1]


class White:
    def __init__(self, board, name="white", real=1):
        self.board = board
        self.name = name
        self.real = real
        self.king = self.king_()

    def __str__(self):
        return self.name

    def pieces(self):
        for line in self.board.internal:
            for piece in line:
                if piece:
                    if piece.color == self.real:
                        yield piece

    def king_(self):
        for piece in self.pieces():
            if piece.num == 5:
                return piece

    def make_move(self, piece, move):
        if not piece.num:
            if not self.board.get_at(*move) and abs(piece.pos[0]-move[0]) == 1:
                self.board.en_passant(piece, move)
        if piece.num == 5:
            if move[0] == 2 and not piece.moved:
                self.board.castle(piece, right_side=False)
                return
            elif move[0] == 6 and not piece.moved:
                self.board.castle(piece)
                return

        return self.board.move(piece.pos, move)

    def has_no_moves(self):
        for piece in self.pieces():
            if piece.absolute_moves(self.king):
                return False

        return True


class Black(White):
    def __init__(self, board, name="black", real=0):
        super().__init__(board, name=name, real=0)
