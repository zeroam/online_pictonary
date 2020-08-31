from typing import List


class Chat(object):
    def __init__(self, r):
        self.content = []
        self.round = r

    def update_chat(self, msg) -> None:
        self.content.append(msg)

    def get_chat(self):
        return self.content

    def __len__(self):
        return len(self.content)

    def __str__(self):
        return "".join(self.content)

    def __repr__(self):
        return str(self)
