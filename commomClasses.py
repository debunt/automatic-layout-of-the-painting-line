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


class Figure:
    def __init__(self, start_point, finish_point):
        self.start_point = start_point
        self.finish_point = finish_point
        # self.fig_name = fig_name -- для создания именнованных фигур
        self.figures_queue = []
        # Поля для связи конвейера с фигурами
        # TODO пока в ручном режиме задую I/O агрегатов, в placement pins заранее известны
        self.in_point = Coordinate(start_point.x + 0, start_point.y - 1)
        self.out_point = Coordinate(start_point.x + 0, start_point.y - 1)

    def create_figure_queue(self):
        delta_x = self.finish_point.x - self.start_point.x
        delta_y = self.finish_point.y - self.start_point.y
        '''
        u ----------- f ----- y 
        |             |
        |             |
        s ----------- b
        |
        |
        x
        '''
        s = self.start_point
        f = self.finish_point

        # TODO Далее начинаю создавать тьюплы. Зачем, если есть класс Coordinate? - чтобы сортировать

        iter_x = s.x
        for _ in range(delta_x):
            self.figures_queue.append((iter_x, s.y))
            self.figures_queue.append((iter_x, f.y))
            iter_x += 1

        iter_y = s.y
        for _ in range(delta_y + 1):
            self.figures_queue.append((s.x, iter_y))
            self.figures_queue.append((f.x, iter_y))
            iter_y += 1

        return sorted(self.figures_queue, reverse=True)

    def get_coordinates(self):
        print(self.start_point)
