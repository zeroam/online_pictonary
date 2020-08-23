class Player(object):
    def __init__(self, name: str):
        self.name = name
        self.score = 0

    def update_score(self, score: int):
        self.score += score

    def get_name(self):
        return self.name

    def get_score(self):
        return self.score
