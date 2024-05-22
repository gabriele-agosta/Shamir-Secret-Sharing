class Player:
    __slots__ = ['x', 'y']

    def __init__(self, x):
        self.x = x
        self.y = []

    def addShare(self, value):
        self.y.append(value)