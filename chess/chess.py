
from .graphical import *


class ChessGame:
    def __init__(self, screen):
        self.board = Board()
        self.players = [Black(self.board), White(self.board)]
        self.graphicalboard = BoardGraphical(self.board, self.players, screen)
        self.black, self.white = self.players
        self.turn = self.white
        self.checkers = list()

    def handle_graphics(self):
        self.graphicalboard.draw_all(self.checkers)

    def reset_skipped(self, color):
        for line in self.board.internal:
            for piece in line:
                if piece:
                    if not piece.num and piece.color == color:
                        if piece.skipped:
                            piece.skipped = False

    def handle_ending(self):
        b = self.black.has_no_moves()
        w = self.white.has_no_moves()
        if b and self.black.king.is_incheck():
            return self.white
        elif w and self.white.king.is_incheck():
            return self.black
        elif b or w:
            return "It's a Draw!"
        else:
            return

    def manage_turns(self):
        if pygame.mouse.get_pressed()[0]:
            if self.graphicalboard.selected:
                if self.graphicalboard.graphical_move(self.turn):
                    other = self.players[(not self.turn.real).real]
                    self.reset_skipped(other.real)
                    self.checkers = other.king.is_incheck()
                    if ending := self.handle_ending():
                        return ending
                    self.turn = other
            else:
                self.graphicalboard.graphical_select(self.turn)

            time.sleep(0.1)

    def FEN(self):
        base = self.board.FEN()
        base += f" {self.turn.name[0]}"

    def main(self):
        clock = pygame.time.Clock()
        while True:
            pygame.event.pump()
            self.handle_graphics()
            if winner := self.manage_turns():
                return winner
            pygame.display.flip()
            clock.tick(60)
