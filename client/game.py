import pygame

from board import Board
from button import Button, TextButton
from chat import Chat
from leader_board import LeaderBoard
from player import Player
from top_bar import TopBar
from bottom_bar import BottomBar
from network import Network


class Game(object):
    BG = (255, 255, 255)
    COLORS = {
        (255,255,255): 0,
        (0,0,0): 1,
        (255,0,0): 2,
        (0,255,0): 3,
        (0,0,255): 4,
        (255,255,0): 5,
        (255,140,0): 6,
        (165,42,42): 7,
        (128,0,128): 8
    }


    def __init__(self, win, conn: Network=None):
        pygame.font.init()
        self.win = win
        self.conn = conn
        self.leader_board = LeaderBoard(50, 125)
        self.board = Board(310, 125)
        self.top_bar = TopBar(10, 10, 1280, 100)
        self.top_bar.change_round(1)
        self.players = []
        self.skip_button = TextButton(90, 800, 125, 50, (255, 255, 0), "Skip")
        self.bottom_bar = BottomBar(310, 880, self)
        self.chat = Chat(1050, 120)
        self.draw_color = (0, 0, 0)

    def add_player(self, player):
        self.players.append(player)
        self.leader_board.add_player(player)

    def draw(self):
        self.win.fill(self.BG)
        self.leader_board.draw(self.win)
        self.board.draw(self.win)
        self.top_bar.draw(self.win)
        self.bottom_bar.draw(self.win)
        self.skip_button.draw(self.win)
        self.chat.draw(self.win)
        pygame.display.update()

    def check_clicks(self):
        """handles clicks on buttons and screen"""
        mouse = pygame.mouse.get_pos()

        if self.skip_button.click(*mouse):
            print("Skip button clicked")
            skips = self.conn.send({1: []})
            print(skips)

        clicked_board = self.board.click(*mouse)
        if clicked_board:
            row, col = clicked_board
            self.conn.send({8: [row, col, self.COLORS[self.draw_color]]})
            self.board.update(row, col, self.draw_color)

        self.bottom_bar.button_events(*mouse)

    def run(self):
        run = True
        clock = pygame.time.Clock()
        while run:
            clock.tick(60)
            self.draw()

            try:
                # get board
                response = self.conn.send({3: []})
                if response:
                    self.board.compressed_board = response
                    self.board.translate_board()

                # get time
                response = self.conn.send({9: []})
                self.top_bar.time = response

                # get chat
                response = self.conn.send({2: []})
                self.chat.update_chat(response)

                # get round info
                self.top_bar.word = self.conn.send({6: []})
                self.top_bar.round = self.conn.send({5: []})
                self.drawing = self.conn.send({11: []})
                self.top_bar.drawing = self.drawing
                self.top_bar.max_round = len(self.players)

                # get player updates
                """response = self.conn.send({0: []})
                self.players = []
                for player in response:
                    p = Player(player)
                    self.add_player(p)"""

            except Exception:
                run = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    break
                    
                if pygame.mouse.get_pressed()[0]:
                    self.check_clicks()

                if event.type == pygame.KEYDOWN:
                    if not self.drawing:
                        if event.key == pygame.K_RETURN:
                            self.conn.send({0: [self.chat.typing]})
                            self.chat.typing = ""
                        else:
                        key_name = pygame.key.name(event.key)

                        key_name = key_name.lower()
                        self.chat.type(key_name)

    pygame.quit()


if __name__ == "__main__":
    g = Game()
    g.run()
