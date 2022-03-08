
import socket


class ChessServer:
    def __init__(self, addr):
        self.addr = addr
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(self.addr)
        self.sock.listen(2)
        self.players = list()

    def __str__(self):
        return f"Chess server running at {self.addr}"

    def accept(self):
        player, addr = self.sock.accept()
        print(addr, "connected!")
        if not self.players:
            player.send((1).to_bytes(1, "big"))
        else:
            player.send((0).to_bytes(1, "big"))

        self.players.append(player)

    def accept_all(self):
        self.accept()
        self.accept()
        for player in self.players:
            player.send(b"ok!")

    def serve(self):
        player1, player2 = self.players
        data1 = player1.recv(1)
        data2 = player1.recv(1)
        enddata = int.from_bytes(player1.recv(1), "big")
        player2.send(data1)
        player2.send(data2)
        if enddata:
            return True
        data1 = player2.recv(1)
        data2 = player2.recv(1)
        enddata = int.from_bytes(player2.recv(1), "big")
        player1.send(data1)
        player1.send(data2)
        if enddata:
            return True

    def reset(self):
        self.players.clear()

    def main(self):
        print("[*]", self, "is now listening.")
        self.accept_all()
        while True:
            if self.serve():
                print("[*] Game ended.")
                self.reset()
                self.main()


def main():
    server = ChessServer(("0.0.0.0", 8002))
    server.main()
    print(server, "shutting down...")


if __name__ == '__main__':
    main()
