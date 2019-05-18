from pyautocad import Autocad, APoint, ACAD
from Technomax.Routing_A_Star import Coordinate
import json
import array
import math
class Shape:

    def __init__(self, path):
        self.points = dict()


class drawDWG:
    def __init__(self):
        self.path2dwg = ""
        self.data = {}

    def execute(self, data):
        self.data = data
        self.scale = self._getScale()#scale содержит гостовский масштаб
        self.scaledCellSize = self.scale * self.data["CellSize"]
        self._scaleFigures()
        self.acad = Autocad(create_if_not_exists=True)  # so far app is not open
        self.pathQmax = "D:\YandexDisk\#SKOLTECH\Early Research Tecnomax\pythonScript\Files\AutoCAD_cabines\Q-MAX.dwg"
        # TODO create windows attention about that in that time autocad will be opening
        #self.acad.Application.Documents.open(self.pathQmax)
        """l = []
        for obj in self.acad.iter_objects():
            try:
                if obj.layer == "Границы Цеха":
                    l.extend(list(obj.coordinates)) #use extend because will be 1 list

            except Exception:
                print(f"Exception: ошибка при итерации по файлу {self.path2dwg}")
                continue
        """

        #self.acad.Application.Documents.Add()
        self._figuresDraw()
        self._conveyorsDraw()

        return "next"


    # функция для оппределения scale фактора для чертежа. Задача: поместить полученную расстановку в заданый формат
    # пока формат только А1
    # TODO добавить поддержку остальных форматов
    def _getScale(self):
        index = self.data["occupiedFrame"].index(max(self.data["occupiedFrame"]))#если 0, то ширина расстановки самая большая сторона, иначе высота
        key = ["width", "height"]
        path = "Files/templates.json"  # путь до JSON файла

        with open(path, 'r', encoding="utf-8") as f:
            self.templates = json.loads(f.read())

        scale_raw = self.templates["A1"][key[index]] / self.data["occupiedFrame"][index] / self.data['CellSize']
        #перевод стандартных масштабов во float-список
        scales = [float(e.split(":")[0]) / float(e.split(":")[1]) for e in self.templates["GHOSTscales"]]

        #выбираю подходящий стандартный мастшаб из гостовских масштабов уменьшения
        for scale in scales:
            if scale > scale_raw:
                continue
            else:#возвращаю подходящий гостовский масштаб и строку
                return scale


    #масштабирование фигур с заданым масштабом
    def _scaleFigures(self):


        for i, f in enumerate(self.data["Figures"]):
            coord = f.start_point
            self.data["Figures"][i].start_point = Coordinate(coord.x * self.scaledCellSize, coord.y * self.scaledCellSize)

            coord = f.finish_point
            self.data["Figures"][i].finish_point = Coordinate(coord.x * self.scaledCellSize, coord.y * self.scaledCellSize)



        # отрисовка основной надписи. Размер листа пока А1
    def _templateDraw(self):
        # insPoint = self.acad.insertionPnt(0,0,0)
        self.acad.model.InsertBlock([0, 0, 0],
                                    "D:\YandexDisk\#SKOLTECH\Early Research Tecnomax\pythonScript\Files\AutoCAD_cabines\qmax.dwg",
                                    1, 1, 1, 0)

        pass

        # отрисовка фигур в натуральную величину

    def _figuresDraw(self):
        figures = self.data["Figures"]
        points = list()

        for f in figures:
            p = [f.start_point.y, -f.start_point.x,
                 (f.finish_point.y + self.scaledCellSize), -f.start_point.x,
                 (f.finish_point.y + self.scaledCellSize), -(f.finish_point.x + self.scaledCellSize),
                 f.start_point.y, -(f.finish_point.x + self.scaledCellSize),
                 f.start_point.y, -f.start_point.x]
            self.acad.model.AddLightWeightPolyline(array.array("d", p))
            insert_point = APoint(f.start_point.y + (f.finish_point.y - f.start_point.y + self.scaledCellSize)*0.5, - f.start_point.x -(f.finish_point.x - f.start_point.x + self.scaledCellSize)*0.5)
            text = self.acad.model.AddText(f.name, insert_point, 5)

            if (f.finish_point.y - f.start_point.y) < (f.finish_point.x - f.start_point.x):
                text.rotation = 1.5708
            text.Alignment = ACAD.acAlignmentCenter
            text.TextAlignmentPoint = insert_point




        # самое сложное - отрисовка конвейера
    def _conveyorsDraw(self):
        for conveyor in self.data["Conveyors"]:
            self.x_dirc = 0 # -1 stands for negative direction along X axis, 0 - const, +1 stands for positive direction along X axis
            self.y_dirc = -1 # the same for Y axis
            for i, coord in enumerate(conveyor):
                if i in [0, 1]: continue

                if conveyor[i-1].x - coord.x != 0:
                    #после этого условия проверям, мы шли до этого по прямой или нет?
                    if self.x_dirc:
                        p1 = APoint(conveyor[i-1].x, conveyor[i-1].y + self.scaledCellSize/2)
                        p2 = APoint(coord.x, coord.y + self.scaledCellSize/2)
                        self.acad.model.AddLine(p1,p2)
                #это условие необязательно, поскольку мы и так знаем, что если не по Х изменение, то значит по Y
                elif conveyor[i-1].y - coord.y != 0:
                    if self.straight:
                        p1 = APoint(conveyor[i - 1].x + self.scaledCellSize / 2, conveyor[i - 1].y)
                        p2 = APoint(coord.x + self.scaledCellSize / 2, coord.y)
                        self.acad.model.AddLine(p1, p2)


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




if "__main__" == __name__:
    data = 12
    drawer = drawDWG()
    drawer.execute(data)