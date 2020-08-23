import pygame
import random


class Board(object):
    ROWS = COLS = 90
    COLORS = {
        0: (255, 255, 255),  # white
        1: (0, 0, 0),  # black
        2: (255, 0, 0),  # red
        3: (0, 255, 0),  # green
        4: (0, 0, 255),  # blue
        5: (255, 255, 0),  # yello
        6: (255, 140, 0),  # orange
        7: (165, 42, 42),  # brown
        8: (128, 0, 128),  # purple
    }

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.WIDTH = 720
        self.HEIGHT = 720
        self.compressed_board = []
        self.board = self.create_board()
        self.BORDER_THICKNESS = 5

    def create_board(self):
        return [[(255, 255, 255) for _ in range(self.COLS)] for _ in range(self.ROWS)]

    def translate_board(self):
        for y, row in enumerate(self.compressed_board):
            for x, col in enumerate(row):
                self.board[y][x] = self.COLORS[col]

    def draw(self, win) -> None:
        pygame.draw.rect(win, (0, 0, 0), (self.x - self.BORDER_THICKNESS / 2, self.y - self.BORDER_THICKNESS / 2, self.WIDTH + self.BORDER_THICKNESS, self.HEIGHT + self.BORDER_THICKNESS), self.BORDER_THICKNESS)
        for y, row in enumerate(self.board):
            for x, col in enumerate(row):
                pygame.draw.rect(win, col, (self.x + x * 8, self.y + y * 8, 8, 8), 0)

    def click(self, x: int, y: int) -> tuple:
        row = int((y - self.y) / 8)
        col = int((x - self.x) / 8)

        if 0 <= row <= self.ROWS and 0 <= col <= self.COLS:
            return row, col

        return None


    def update(self, row: int, col: int, color: int) -> None:
        self.board[row][col] = color

    def clear(self) -> None:
        self.board = self.create_board()
