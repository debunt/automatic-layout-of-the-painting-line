class Coordinate:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __str__(self):
        return 'x: {}, y: {}'.format(self.x, self.y)

    def get_length(self, other):  # Манхетоновское расстояние
        return abs(self.x - other.x) + abs(self.y - other.y)