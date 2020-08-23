class Player(object):
    def __init__(self, ip: str, name: str):
        self.game = None
        self.ip = ip
        self.name = name
        self.score = 0

    def set_game(self, game) -> None:
        """sets the player game association"""
        self.game = game

    def update_score(self, x: int) -> None:
        """updates a player score"""
        self.score += x

    def guess(self, word: str) -> bool:
        """makes a player guess"""
        return self.game.player_guess(self, word)

    def disconnect(self) -> None:
        """call to disconnect player"""
        self.game.player_disconnected(self)

    def get_ip(self) -> str:
        """gets player ip address"""
        return self.ip

    def get_name(self) -> str:
        """gets player name"""
        return self.name

    def get_score(self) -> int:
        """gets player score"""
        return self.score