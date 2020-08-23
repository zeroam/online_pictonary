import time
import socket
import json


class Network:
    def __init__(self, name: str):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "localhost"
        self.port = 5555
        self.addr = (self.server, self.port)
        self.name = name
        self.connect()

    def connect(self) -> None:
        try:
            self.client.connect(self.addr)
            self.client.send(self.name.encode())
            return self.client.recv(1024).decode()
        except Exception as e:
            self.disconnect(e)

    def send(self, data: dict) -> None:
        try:
            self.client.send(json.dumps(data).encode())

            d = ""
            while True:
                last = self.client.recv(1024).decode()
                d += last

                if d.count(".") == 1:
                    break

            if d.endswith("."):
                d = d[:-1]

            keys = [key for key in data.keys()]
            return json.loads(d)[str(keys[0])]
        except socket.error as e:
            self.disconnect(e)

    def disconnect(self, msg: str) -> None:
        print(f"[EXCEPTION] Disconnected from server: {msg}")
        self.client.close()


if __name__ == "__main__":
    n = Network("jayone")
    print("players:", n.send({-1: []}))
    print("guess:", n.send({0: ["hello"]}))
    print(n.send({1: []}))  # skip
    print("chat:", n.send({2: []}))  # chat
    # print(n.send({3: []}))  # get board
    print("round:", n.send({5: []}))  # get round
    print("word:", n.send({6: []}))
    print("skips:", n.send({7: []}))
    print("round time:", n.send({9: []}))
    time.sleep(1)
    print("round time:", n.send({9: []}))
