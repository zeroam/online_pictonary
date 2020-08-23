import pygame

from board import Board
from button import Button, TextButton
from chat import Chat
from leader_board import LeaderBoard
from player import Player
from top_bar import TopBar
from bottom_bar import BottomBar
from chat import Chat


class Game(object):
    BG = (255, 255, 255)

    def __init__(self):
        pygame.font.init()

        self.WIDTH = 1300
        self.HEIGHT= 1000
        self.win = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.leader_board = LeaderBoard(50, 125)
        self.board = Board(310, 125)
        self.top_bar = TopBar(10, 10, 1280, 100)
        self.top_bar.change_round(1)
        self.skip_button = TextButton(90, 800, 125, 50, (255, 255, 0), "Skip")
        self.bottom_bar = BottomBar(310, 880, self)
        self.chat = Chat(1050, 120)
        self.draw_color = (0, 0, 0)

        # self.players = [Player("Tim"), Player("Bob"), Player("Joe"), Player("Mike"), Player("Sam")]
        # for player in self.players:
        #     self.leader_board.add_player(player)

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

        clicked_board = self.board.click(*mouse)
        if clicked_board:
            row, col = clicked_board
            self.board.update(row, col, self.draw_color)

        self.bottom_bar.button_events(*mouse)

    def run(self):
        run = True
        clock = pygame.time.Clock()
        while run:
            clock.tick(60)
            self.draw()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    break
                    
                if pygame.mouse.get_pressed()[0]:
                    self.check_clicks()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.chat.update_chat(self.chat.typing)
                        self.chat.typing = ""
                    else:
                        key_name = pygame.key.name(event.key)

                        key_name = key_name.lower()
                        self.chat.type(key_name)

        pygame.quit()


if __name__ == "__main__":
    g = Game()
    g.run()
