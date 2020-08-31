import time
from typing import List
from _thread import start_new_thread

from chat import Chat


class Round(object):
    def __init__(self, word: str, player_drawing, players: list, game):
        self.word = word
        self.player_drawing = player_drawing
        self.players = players
        self.game = game
        self.player_guessed = []
        self.players_skipped = []
        self.skips = 0
        self.player_scores = {player: 0 for player in players}
        self.time = 75
        self.chat = Chat(self)
        start_new_thread(self.time_thread, ())

    def skip(self, player) -> bool:
        """returns true if round skipped threshold met"""
        if player not in self.players_skipped:
            self.players_skipped.append(player)
            self.skips += 1
            self.chat.update_chat(f"Player has voted to skip ({self.skips}/{len(self.players) - 2})")
            if self.skips >= len(self.players) - 2:
                return True

        return False

    def get_scores(self) -> list:
        """Returns all the player scores"""
        return self.player_scores

    def get_score(self, player) -> int:
        """gets a specific player score"""
        if player in self.player_scores:
            return self.player_scores[player]
        else:
            raise Exception("Player not in score list")
        
    def time_thread(self) -> None:
        """runs thread to keep track of time"""
        while self.time > 0:
            time.sleep(1)
            self.time -= 1
        self.end_round("Time's up")


    def guess(self, player, word: str) -> bool:
        """returns true if player guess correct answer"""
        if word == self.word:
            self.player_guessed.append(player)
            self.chat.update_chat(f"{player.get_name()} has guessed word")
            return True
            # TODO : implement scoring system here
        self.chat.update_chat(f"{player.get_name()} guessed {word}")
        return False

    def player_left(self, player) -> None:
        """remove player that left from scores and list"""
        if player in self.player_scores:
            del self.player_scores[player]

        if player in self.player_guessed:
            self.player_guessed.remove(player)

        if player == self.player_drawing:
            self.chat.update_chat("Round has been skipped because the drawer left")
            self.end_round("Drawing player left")

    def end_round(self, msg: str):
        for player in self.players:
            player.update_score(self.player_scores[player])
        self.game.round_ended()
