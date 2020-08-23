import json
import socket
import threading
from typing import List

from player import Player
from game import Game


class Server(object):
    PLAYERS = 1

    def __init__(self):
        self.connection_queue: List[Player] = []
        self.game_id = 0

    def player_thread(self, conn: socket.socket, player: Player) -> None:
        """handles in game communiation between clients"""
        while True:
            try:
                # receive request
                try:
                    data = conn.recv(1024).decode()
                    data = json.loads(data)
                    print("[LOG] receive data:", data)
                except Exception as e:
                    break

                keys = [int(key) for key in data.keys()]
                send_msg = {key: [] for key in keys}

                for key in keys:
                    if not player.game:
                        break

                    if key == -1:  # get game, returns a list of players
                        send = {player.get_name(): player.get_score() for player in player.game.players}
                        send_msg[-1] = send
                    elif key == 0:  # guess
                        correct = player.guess(data['0'][0])
                        send_msg[0] = correct
                    elif key == 1:  # skip
                        skip = player.game.skip()
                        send_msg[1] = skip
                    elif key == 2:  # get chat
                        content = player.game.round.chat.get_chat()
                        send_msg[2] = content
                    elif key == 3:  # get board
                        board = player.game.board.get_board()
                        send_msg[3] = board
                    elif key == 4:  # get score
                        scores = player.game.get_player_scores()
                        send_msg[4] = scores
                    elif key == 5:  # get round
                        round = player.game.round_count
                        send_msg[5] = round
                    elif key == 6:  # get word
                        word = player.game.round.word
                        send_msg[6] = word
                    elif key == 7:  # get skips
                        skips = player.game.round.skips
                        send_msg[7] = skips
                    elif key == 8:  # update board
                        x, y, color = data[8][:3]
                        player.game.update_board(x, y, color)
                    elif key == 9:  # get round time
                        t = player.game.round.time
                        send_msg[9] = t
                    else:
                        raise Exception("Not a valid request")

                # player is not apart of game
                print(f"send {len(json.dumps(send_msg).encode())} bytes")
                conn.sendall(json.dumps(send_msg).encode() + b".")
            except Exception as e:
                print(f"[EXCEPTION] {player.get_name()} disconnected: {e}")
                break
                # TODO : call player game disconnect method
        print(f"[DISCONNECT] {player.name} disconnected")
        conn.close()

    def handle_queue(self, player: Player) -> None:
        """adds plyaer to queue and creates new game if enough players"""
        self.connection_queue.append(player)

        if len(self.connection_queue) >= self.PLAYERS:
            self.game_id += 1
            game = Game(self.game_id, self.connection_queue[:])

            for p in self.connection_queue:
                p.set_game(game)

            self.connection_queue = []

    def authentication(self, conn: socket.socket, addr: str) -> None:
        try:
            data = conn.recv(1024)
            name = data.decode()
            if not name:
                raise Exception("No name received")
                
            print(f"[AUTHENTICATE] name: '{name}'")
            conn.sendall("1".encode())

            player = Player(addr, name)
            self.handle_queue(player)
            threading.Thread(target=self.player_thread, args=(conn, player)).start()
        except Exception as e:
            print(f"[ERROR] {e}")
            conn.close()

    def connection_thread(self):
        server = ""
        port = 5555

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        try:
            s.bind((server, port))
        except socket.error as e:
            print(e)

        s.listen(1)
        print("Waiting for a connection, Server started")

        while True:
            try:
                conn, addr = s.accept()
                print(f"[CONNECT] New connection!, {addr}")

                self.authentication(conn, addr)
            except Exception as e:
                conn.close()
                break


if __name__ == "__main__":
    s = Server()
    threading.Thread(target=s.connection_thread).start()
