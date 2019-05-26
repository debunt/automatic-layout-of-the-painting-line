import copy
from Technomax.Routing_A_Star import Coordinate
class Conveyor:

    def __init__(self, conveyor, offset):
        self.coordinate_from = conveyor[1].in_point
        self.coordinate_to = conveyor[2].out_point
        self.conveyor = self._get_pre_conv(conveyor[0], conveyor[1], conveyor[2], offset)


        self.final_conveyor = list()

    def _get_pre_conv(self, conveyor, figure_from, figure_to, offset):
        if len(conveyor[0]) == 0: return []
        preliminary_conv = copy.deepcopy(conveyor[0])
        for i in [1,2]:
            point = conveyor[0][0 if i == 1 else -1]
            point += offset
            if i == 1:
                preliminary_conv.insert(0, self._getImaginaryCell(figure_from, point))
            else:
                preliminary_conv.append(self._getImaginaryCell(figure_to, point))
        return preliminary_conv

    # возвращает координаты мнимой клетки
    def _getImaginaryCell(self, figure, point):
        if point.y < figure.start_point.y:
            return Coordinate(point.x, figure.start_point.y)#слева
        elif point.y >= figure.finish_point.y:
            return Coordinate(point.x, figure.finish_point.y)#справа
        elif point.x >= figure.finish_point.x:
            return Coordinate(figure.finish_point.x - 1, point.y)#снизу
        elif point.x < figure.start_point.x:
            return Coordinate(figure.start_point.x, point.y)#сверху

    def _build_conveyor(self):