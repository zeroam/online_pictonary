from typing import List, Tuple


class Board(object):
    ROWS = COLS = 90

    def __init__(self):
        """init the board by creating emtpy board (all white pixels)"""
        self.data = self._create_empty_board()

    def update(self, row: int, col: int, color: int) -> None:
        """update singular pixel of the board"""
        self.data[row][col] = color

    def clear(self) -> None:
        """clears board to white"""
        self.data = self._create_empty_board()

    def _create_empty_board(self) -> List[List[tuple]]:
        """creates an empty board (all white)"""
        return [[0] * self.ROWS for _ in range(self.COLS)]

    def fill(self, x: int, y: int) -> None:
        """fills in a specific shape of area using recursion"""
        pass

    def get_board(self) -> List[List[Tuple[int, int, int]]]:
        """gets the data of the board"""
        return self.data
