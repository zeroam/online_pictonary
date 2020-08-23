import random
from typing import List, Tuple, Dict, Any

from board import Board
from round import Round


class Game(object):
    def __init__(self, id: int, players: list):
        """Init the game! once player threshold is met"""
        self.id = id
        self.players = players
        self.word_used = set()
        self.round = None
        self.board = Board()
        self.player_draw_ind = 0
        self.round_count = 1
        self.start_new_round()

    def start_new_round(self):
        """Starts a new round with a new word"""
        try:
            self.round = Round(self.get_word(), self.players[self.player_draw_ind], self.players, self)
            self.round_count += 1

            if self.player_draw_ind >= len(self.players):
                self.round_ended()
                self.end_game()

            self.player_draw_ind += 1
        except Exception:
            self.end_game()

    def player_guess(self, player, guess: str) -> bool:
        """Makes the players guess the word"""
        return self.round.guess(player, guess)

    def player_disconnected(self, player) -> None:
        """Call to clean up objects when player disconnects"""
        # TODO : check this
        if player in self.players:
            player_ind = self.players.index(player)
            if player_ind >= self.player_draw_ind:
                self.player_draw_ind -= 1
            self.players.remove(player)
            self.round.player_left(player)
            self.round.chat.update_chat(f"Player {player.get_name()} disconnected")
        else:
            raise Exception("Player not in game")

    def get_player_scores(self) -> Dict[Any, int]:
        """give a dict of player scores"""
        scores = {player: player.get_score() for player in self.players}
        return scores

    def skip(self) -> None:
        """Increments the round skips, if skips are greater than
        threshold, starts new round."""
        if self.round:
            new_round = self.round.skip()
            self.round.chat.update_chat(f"Player has voted to skip ({self.round.skips}/{len(self.players)})")
            if new_round:
                self.round.chat.update_chat(f"Round {self.round_count} has been skipped")
                self.round_ended()
                return True
            return False
        else:
            raise Exception("No round started yet!")

    def round_ended(self) -> None:
        """If the round ends call this"""
        self.round.chat.update_chat(f"Round {self.round_count} ended")
        self.start_new_round()
        self.board.clear()

    def update_board(self, x: int, y: int, color: int) -> None:
        """Calls update method on board."""
        if not self.board:
            raise Exception("No board created")
        self.board.update(x, y, color)

    def end_game(self) -> None:
        print(f"[GAME] game {self.id} ended")
        for player in self.players:
            player.game = None

    def get_word(self) -> str:
        """gives word that has not been used"""
        # TODO : get a list of words from somewhere
        with open("words.txt") as f:
            words = []
            for line in f:
                word = line.strip()
                if word not in self.word_used:
                    words.append(word)

        r = random.randint(0, len(words))
        return words[r].strip()
