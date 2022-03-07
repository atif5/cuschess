
from .graphical import *
import time
import socket
import select

SERVICE_ADDR = ("0.0.0.0", 8002)


class OnlineChessGame:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.board = Board()
        self.players = [Black(self.board), White(self.board)]
        self.graphicalboard = BoardGraphical(self.board, self.players)
        self.black, self.white = self.players
        self.turn = self.white
        self.checkers = list()
        local = self.connect()
        if local:
            self.local = self.white
            self.remote = self.black
            self.turn = self.local
        else:
            self.local = self.black
            self.remote = self.white
            self.turn = self.remote

    def connect(self):
        global SERVICE_ADDR
        print(f"Trying to connect to the server --> {SERVICE_ADDR}...")
        try:
            self.sock.connect(SERVICE_ADDR)
        except ConnectionRefusedError:
            print("Could not connect to the server, please try again.")
            exit()

        print("Connected to the server.")
        return int.from_bytes(self.sock.recv(1), "big")

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

    def manage_localturn(self):
        self.reset_skipped(self.local.real)
        if pygame.mouse.get_pressed()[0]:
            if self.graphicalboard.selected:
                start_pos = self.graphicalboard.selected.pos.tolist()
                if end_pos := self.graphicalboard.graphical_move(self.local):
                    self.checkers = self.remote.king.is_incheck()
                    self.sock.send(
                        (start_pos[0]*10+start_pos[1]).to_bytes(1, "big"))
                    self.sock.send(
                        (end_pos[0]*10+end_pos[1]).to_bytes(1, "big"))
                    if ending := self.handle_ending():
                        return ending
                    else:
                        return False
            else:
                self.graphicalboard.graphical_select(self.local)

            time.sleep(0.1)

    def manage_remoteturn(self):
        self.reset_skipped(self.remote.real)
        if not (ready := select.select([self.sock], [], [], 0.01)[0]):
            return
        else:
            data1 = ready[0].recv(1)
            data2 = ready[0].recv(1)
        data1 = int.from_bytes(data1, 'big')
        data2 = int.from_bytes(data2, 'big')
        start_pos = (data1//10, data1 % 10)
        end_pos = (data2//10, data2 % 10)
        rpiece = self.board.get_at(*start_pos)
        self.graphicalboard.selected = rpiece
        self.graphicalboard.animate_movement(rpiece, end_pos)
        self.remote.make_move(rpiece, end_pos)
        self.checkers = self.local.king.is_incheck()
        

        if ending := self.handle_ending():
            return ending
        else:
            return False

    def manage_turns(self):
        if self.turn is self.remote:
            if ending := self.manage_remoteturn():
                return ending
            elif ending is False:
                self.turn = self.local
        elif self.turn is self.local:
            if ending := self.manage_localturn():
                return ending
            elif ending is False:
                self.turn = self.remote

    def main(self):
        clock = pygame.time.Clock()
        print(self.sock.recv(3))
        self.graphicalboard.reverse = not self.local.real
        while True:
            pygame.event.pump()
            self.handle_graphics()
            if winner := self.manage_turns():
                return winner
            pygame.display.flip()
            clock.tick(60)
