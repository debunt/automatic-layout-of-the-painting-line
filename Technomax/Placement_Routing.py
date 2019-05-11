import pprint
import tempfile
import os
from Technomax.Routing_A_Star import Routing, Coordinate


class Figure:
    def __init__(self, start_point, finish_point, name, loc_coordinate_from, loc_coordinate_to, neighbor_name):
        self.start_point = start_point
        self.finish_point = finish_point
        self.name = name
        self.neighbor_name = neighbor_name
        self.figures_queue = []
        # Поля для связи конвейера с фигурами
        # TODO пока в ручном режиме задую I/O агрегатов, в placement pins заранее известны
        self.in_point = Coordinate(start_point.x + loc_coordinate_from.x, start_point.y + loc_coordinate_from.y - 1)
        self.out_point = Coordinate(start_point.x + loc_coordinate_to.x, start_point.y + loc_coordinate_to.y - 1)

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


class Area:
    def __init__(self, width, height):
        self.passabilities = [
            [1,  1,  1],
            [1,  1,  1],
            [1,  1,  1],
        ]
        self.width = width
        self.height = height

    def draw_map(self):
        self.passabilities = [[1 for j in range(self.width)] for i in range(self.height)]  # Заполнение нулями матрицы-карты
        return self.passabilities

    def clear_map(self):
        self.passabilities = [[1 for j in range(self.width)] for i in range(self.height)]  # Заполнение нулями матрицы-карты
        return self.passabilities

    def get_passability(self, coordinate):
        return self.passabilities[coordinate.x][coordinate.y]  # Возвращает координату (x,y) точки

    def figure_adding(self, new_figure):
        list_of_figs = new_figure.create_figure_queue()
        # print(list_of_walls)
        # Добавление происходит проходясь по списку тьюплов list_of_figs
        for _ in range(len(list_of_figs)):
            buf = list_of_figs.pop()
            self.passabilities[buf[0]][buf[1]] = -1
        # Добавляем вход/выход агрегатам
        # self.passabilities[new_figure.in_point.x][new_figure.in_point.y] = -3
        # self.passabilities[new_figure.out_point.x][new_figure.out_point.y] = -4

        return self.passabilities

    def conveyor_adding(self, coordinate_from, coordinate_to, only_path_len=None):
        path = Routing.get_path(self, coordinate_from, coordinate_to)
        if only_path_len:
            return len(path)
        #print("Length of path =", len(path))
        #print("Path coordinates:")
        #for i in range(len(path)):
            #print(path[i], end=' ')
        # Добавление происходит поэлементной проходкой по Area
        if path:
            for _ in range(len(path)):
                buf = path.pop()
                self.passabilities[buf.x][buf.y] = -2
        #else:
            #print('Path does not exist')

        # print(list_of_walls)
        return self.passabilities


def coordinates_checker(start_point, finish_point):
    if start_point.x <= finish_point.x and start_point.y <= finish_point.y:
        return True
    return False
