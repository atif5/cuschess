
from cuschess import *


class ComputerChessGame:
    def __init__(self, screen, engine, playerc):
        self.engine = engine
        self.engine.set_fen_position(
            "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
        self.board = Board()
        self.players = [Black(self.board), White(self.board)]
        self.black, self.white = self.players
        self.player = self.players[playerc]
        self.computer = self.players[(not playerc)]
        self.turn = self.white
        self.graphicalboard = BoardGraphical(
            self.board, self.players, screen, reverse=(not self.player.real))
        self.checkers = list()

    def handle_graphics(self):
        self.graphicalboard.draw_all(self.checkers)

    def change_difficulty(self, level):
        self.engine.set_skill_level(level)

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

    def manage_player_turn(self):
        if pygame.mouse.get_pressed()[0]:
            if self.graphicalboard.selected:
                if move := self.graphicalboard.graphical_move(self.player):
                    if ending := self.handle_ending():
                        return ending
                    self.engine.make_moves_from_current_position([move])
                    self.checkers = self.computer.king.is_incheck()
                    self.reset_skipped(self.computer.real)
                    self.turn = self.computer
            else:
                self.graphicalboard.graphical_select(self.player)

            time.sleep(0.1)

    def manage_computer_turn(self):
        pygame.display.flip()
        self.reset_skipped(self.computer.real)
        move = self.engine.get_best_move()
        spos, dpos = move[0:2], move[2:4]
        rdpos = self.board.nottoreal(dpos)
        rpiece = self.board.notget_at(spos)
        self.graphicalboard.select(rpiece, self.computer)
        self.graphicalboard.animate_movement(rpiece, rdpos)
        self.graphicalboard.deselect()
        self.computer.make_move(rpiece, self.board.nottoreal(dpos))
        self.engine.make_moves_from_current_position([move])
        self.checkers = self.player.king.is_incheck()
        self.turn = self.player
        if ending := self.handle_ending():
            return ending

    def manage_turns(self):
        if self.turn is self.computer:
            if ending := self.manage_computer_turn():
                return ending
        elif self.turn is self.player:
            if ending := self.manage_player_turn():
                return ending

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
