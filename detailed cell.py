import numpy as np

class DetailedCell:

    def __init__(self, three_cells, scale, radius):
        self.code = self._get_code(three_cells) # код, описывающий тип клетки
        self.type = self._get_type(self.code)


    def return_last_point(self, previous_cell):
        pass

    def _get_type(self):
        pass

    def _get_code(self, three_cells):
        self.code = str()
        for i in [1, 2]:
            self.code += str(np.sign(coords[i].x - coords[i-1].x))
            self.code += str(np.sign(coords[i].y - coords[i-1].y))
        return self.code