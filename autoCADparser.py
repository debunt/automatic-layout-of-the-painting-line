from pyautocad import Autocad, APoint
from commomClasses import *
import math


class Shape:

    def __init__(self, path):
        self.points = dict()


class parseDWG:
    def __init__(self):
        self.path2dwg = ""
        self.data = {}
    def execute(self, data):
        self.data = data
        self.acad = Autocad(create_if_not_exists=True)  # so far app is not open
        self.path2dwg = self.data["Строительная подоснова"]# refer to the key to the field where the link to this file
        if self.path2dwg == "":
            return "next" #если не указан путь до файла, то перейти к следующему объекту
        # TODO create windows attention about that in that time autocad will be opened
        self.acad.Application.Documents.open(self.path2dwg)
        self._read()
        self.acad.Application.Documents.close() # close previous file in autocad


        return "next"

    #returns coordinate of base point, width and height of each figure on the list
    def _getBPoint_W_H(self, listCoordinates):
        maxindexes = [i * 2 + 1 for i, j in enumerate(listCoordinates[1::2]) if j == max(
            listCoordinates[1::2])]  # возвращает индексы максимальных элементов по Y координате ( поэтому я указал отсчет со 2 элемента)
        minindexes = [i * 2 for i, j in enumerate(listCoordinates[0::2]) if j == min(listCoordinates[0::2])]
        #теперь находим все минимальные
        indexbP = [i for i in maxindexes if (i - 1) in minindexes]  # find index of Y of base Point
        indexbP = [indexbP[0] - 1] + indexbP  # find index of X of base Point
        basePoint = Coordinate(listCoordinates[indexbP[0]], listCoordinates[indexbP[1]])  # object, consist of x and y
        width = max(listCoordinates[0::2]) - basePoint.x  # calculate width of layout
        height = basePoint.y - min(listCoordinates[1::2])  # calculate height of layout

        return [basePoint, width, height]


    def _read(self):

        initialLayout = dict()
        tempBoundaries = list()
        tempObstacles = list()
        #iteration will consider only polyline type. Other objects will be ignored
        for obj in self.acad.iter_objects("Polyline"):
            try:
                if obj.layer == "Границы Цеха":
                    tempBoundaries.extend(list(obj.coordinates)) #use extend because will be 1 list
                elif obj.layer == "Препятствия":
                    tempObstacles.append(list(obj.coordinates)) #use append because can be several lists
            except Exception:
                print(f"Exception: ошибка при итерации по файлу {self.path2dwg}")
                continue

        # At first, we find base point, width and height of initial Layout
        boundary = self._getBPoint_W_H(tempBoundaries)
        self.data["Ширина Размещения"][0] = boundary[1] # обновляем значение ширины размещения после парсинга файла
        self.data["Высота Размещения"][0] = boundary[2] # обновляем значение высоты размещения после парсинга файла

        #at final, we find base point, width and height of all obstacles
        obstacles = list()
        for obstacle in tempObstacles:
            templist = self._getBPoint_W_H(obstacle)
            local_base_point = Coordinate(abs(boundary[0].x - templist[0].x), abs(boundary[0].y - templist[0].y))
            obstacles.append([local_base_point, templist[1], templist[2]])

        self.data.update({"Obstacles" : obstacles})

        """ Печать лок координат препятствий, их ширины и высоты
        for i, o in enumerate(obstacles):
            print(f"лок коорд {i} фигуры", o[0].x, o[0].y)
            print(f"Ширина {i} фигуры", o[1])
            print(f"Высота {i} фигуры", o[2])
        """

    def get(self):
        return self.data




"""
if "__main__" == __name__:

    #АХПП размеры
    bs_axpp = [0, 0]
    phi_axpp = 0
    sizesAHPP = {
        'length': 45000,
         "width" : 1700
    }

    #Размеры Сушки
    bs_dryer = [2000, 2000]
    phi_dryer = 0
    sizesDryer = {
        'length': 30000,
        "width": 3000
    }

    # Размеры Печи
    bs_oven = [2000, 5000]
    phi_oven = 0
    sizesOven = {
        'length': 25000,
        "width": 5000
    }

    # Размеры блока
    bs_1 = [-7000, 0]
    phi_1 = 90
    sizes1 = {
        'length': 20000,
        "width": 5000
    }

    # формирую лист блоков для дальнейшей передачи функции draw
    blocks = list()
    blocks.append(CadAhpp(bs_axpp, sizesAHPP, phi_axpp))
    blocks.append(CadDryer(bs_dryer, sizesDryer, phi_dryer))
    blocks.append(CadPolimer(bs_oven, sizesOven, phi_oven))
    blocks.append(CadPolimer(bs_1, sizes1, phi_1))


    draw = DrawCAD()

    for block in blocks:
        draw.draw(block)



"""

