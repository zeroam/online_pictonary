import pygame

from game import Game
from player import Player
from network import Network


class MainMenu(object):
    BG = (255, 255, 255)

    def __init__(self):
        self.WIDTH = 1300
        self.HEIGHT= 1000
        self.win = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.name = ""
        self.waiting = False
        self.name_font = pygame.font.SysFont("comicsans", 80)
        self.title_font = pygame.font.SysFont("comicsans", 120)
        self.enter_font = pygame.font.SysFont("comicsans", 60)
        self.conn = None

    def draw(self):
        self.win.fill(self.BG)

        title = self.title_font.render("Pictonary!", 1, (0, 0, 0))
        self.win.blit(title, (self.WIDTH // 2 - title.get_width() // 2, 50))

        name = self.name_font.render(f"Type a name: {self.name}", 1, (0, 0, 0))
        self.win.blit(name, (100, 400))

        if self.waiting:
            enter_word = "In Queue..."
        else:
            enter_word = "Press enter to join a game"
        enter = self.enter_font.render(enter_word, 1, (0, 0, 0))
        self.win.blit(enter, (self.WIDTH // 2 - enter.get_width() // 2, 800))

        pygame.display.update()

    def run(self):
        run = True
        clock = pygame.time.Clock()

        while run:
            clock.tick(30)
            self.draw()

            if self.waiting:
                response = self.conn.send({-1: []})
                if response:
                    run = False
                    g = Game(self.win, self.conn)

                    for player in response:
                        p = Player(player)
                        g.add_player(p)
                    g.run()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()
                    quit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if len(self.name) > 1:
                            self.waiting = True
                            self.conn = Network(self.name)
                    else:
                        # gets the key name
                        key_name = pygame.key.name(event.key)

                        key_name = key_name.lower()
                        self.type(key_name)
    
    def type(self, char: str) -> None:
        if char == "backspace":
            if len(self.name) > 0:
                self.name = self.name[:-1]
        elif char == "space":
            self.name += " "
        elif len(char) == 1:
            self.name += char

        if len(self.name) >= 20:
            self.name = self.name[:20]


if __name__ == "__main__":
    pygame.font.init()
    main = MainMenu()
    main.run()
