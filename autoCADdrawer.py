from pyautocad import Autocad, APoint, ACAD
from Technomax.Routing_A_Star import Coordinate
import json
import array
import math
import numpy as np
import copy




class Shape:

    def __init__(self, path):
        self.points = dict()

def change_coord_system(func):
    def wrapped(*args, **kwargs):
        temp = func(*args, **kwargs)
        changed_elems = list()
        for elem in temp:  # if isinstance(cell_draw[0], list) else [cell_draw]:
            if elem[0] == "line":
                changed_elems.append(["line", elem[2], -elem[1], elem[4], -elem[3]])
            elif elem[0] == "arc":
                pR = list(elem[1])
                print(pR, elem[2])
                changed_elems.append(["arc", APoint(pR[1], -pR[0]), elem[2]])
        print(temp)
        print(changed_elems)
        return changed_elems
    return wrapped

class Cells:

    #scale- это уже окончательный масштаб с учетом масштаба чертежа
    #radius - тоже окончательный размер радиуса
    def __init__(self, scale, radius):
        self.scale = scale
        self.radius = radius
        self.cells = dict()
        self._prepareDict()

    @change_coord_system
    def getCell(self, code, glob_coord):
        print(code)

        return [elem for elem in map(self.cells[code], [glob_coord])][0]



    # генерация блоков-конструкторов для отрисовки конвейера

    def _prepareDict(self):
        self.cells.update({"0101": self._horiz})
        self.cells.update({"0-10-1": self._horiz})
        self.cells.update({"-10-10": self._vertic})
        self.cells.update({"1010": self._vertic})

        self.mode = "turn"  # режим отрисовки клеток с поворотом - поворот с радиусом
        if self.radius > self.scale / 2:
            self.mode = "line"  # режим отрисовки клеток с поворотом - линия
            # TODO сейчас я веду линию посередине клетки. при R > lambda/2 необходимо реализовать сдвиг
    # 1 квадрант
        self.cells.update({"-100-1": self._quadrant1})
        self.cells.update({"0110": self._quadrant1})
    # 2 квадрант
        self.cells.update({"0-110": self._quadrant2})
        self.cells.update({"-1001": self._quadrant2})
    # 3 квадрант
        self.cells.update({"1001": self._quadrant3})
        self.cells.update({"0-1-10": self._quadrant3})
    # 4 квадрант
        self.cells.update({"01-10": self._quadrant4})
        self.cells.update({"100-1": self._quadrant4})

    # гориз линия
    def _horiz(self, global_Cord):
        p1 = Coordinate(self.scale / 2, 0)
        p2 = Coordinate(self.scale / 2, self.scale)
        x = global_Cord.x * self.scale
        y = global_Cord.y * self.scale
        return [["line", p1.x + x, p1.y + y, p2.x + x, p2.y + y]]

    # вертик линия
    def _vertic(self, global_Cord):
        p1 = Coordinate(0, self.scale / 2)
        p2 = Coordinate(self.scale, self.scale / 2)
        x = global_Cord.x * self.scale
        y = global_Cord.y * self.scale
        return [["line", p1.x + x, p1.y + y, p2.x + x, p2.y + y]]

    # https://en.wikipedia.org/wiki/Quadrant_(plane_geometry)

    def _quadrant1(self, global_Cord):
        r = self.radius
        p1 = Coordinate(self.scale, self.scale / 2)  # TODO необязательно линия должна идти от середины
        p1_1 = Coordinate(p1.x / 2 + r, p1.y)
        p2 = Coordinate(self.scale / 2, 0)
        p2_2 = Coordinate(p2.x, self.scale / 2 - r)
        x = global_Cord.x * self.scale
        y = global_Cord.y * self.scale
        if self.mode == "line": return ["line", p1.x + x, p1.y + y, p2.x + x, p2.y + y]  # TODO фигово. Сделать нормально
        pR = Coordinate(p2_2.y, p1_1.x)
        return [["line", p1.x + x, p1.y + y, p1_1.x + x, p1_1.y + y], \
               ["line", p2.x + x, p2.y + y, p2_2.x + x, p2_2.y + y], \
               ["arc", APoint(pR.x + x, pR.y + y), r, 0, math.pi / 2]]
        # ----- 1                 полилиния--2 полилиния--данные для дуги--
        # построение дуги в автокад https://knowledge.autodesk.com/search-result/caas/CloudHelp/cloudhelp/2016/ENU/AutoCAD-ActiveX/files/GUID-864A7E1F-D221-4C83-A4DB-F60C8E56FED6-htm.html

    def _quadrant2(self, global_Cord):
        r = self.radius
        p1 = Coordinate(self.scale, self.scale / 2)
        p1_1 = Coordinate(self.scale / 2 + r, self.scale / 2)
        p2 = Coordinate(self.scale / 2, self.scale)
        p2_2 = Coordinate(self.scale / 2, self.scale / 2 + r)
        x = global_Cord.x * self.scale
        y = global_Cord.y * self.scale
        if self.mode == "line": return ["line", p1.x + x, p1.y + y, p2.x + x, p2.y + y]
        pR = Coordinate(p1_1.x, p2_2.y)
        return [["line", p1.x + x, p1.y + y, p1_1.x + x, p1_1.y + y], \
               ["line", p2.x + x, p2.y + y, p2_2.x + x, p2_2.y + y], \
               ["arc", APoint(pR.x + x, pR.y + y), r, 0, math.pi / 2]]
        # -----1 полилиния--2 полилиния--данные для дуги--
        # построение дуги в автокад https://knowledge.autodesk.com/search-result/caas/CloudHelp/cloudhelp/2016/ENU/AutoCAD-ActiveX/files/GUID-864A7E1F-D221-4C83-A4DB-F60C8E56FED6-htm.html

    def _quadrant3(self, global_Cord):
        r = self.radius
        p1 = Coordinate(0, self.scale / 2)
        p1_1 = Coordinate(self.scale / 2 - r, self.scale / 2)
        p2 = Coordinate(self.scale / 2, self.scale)
        p2_2 = Coordinate(self.scale / 2, self.scale / 2 + r)
        x = global_Cord.x * self.scale
        y = global_Cord.y * self.scale
        if self.mode == "line": return ["line", p1.x + x, p1.y + y, p2.x + x, p2.y + y]
        pR = Coordinate(p1_1.x, p2_2.y)
        return [["line", p1.x + x, p1.y + y, p1_1.x + x, p1_1.y + y], \
               ["line", p2.x + x, p2.y + y, p2_2.x + x, p2_2.y + y], \
               ["arc", APoint(pR.x + x, pR.y + y), r, 0, math.pi / 2]]
        # -----1 полилиния--2 полилиния--данные для дуги--
        # построение дуги в автокад https://knowledge.autodesk.com/search-result/caas/CloudHelp/cloudhelp/2016/ENU/AutoCAD-ActiveX/files/GUID-864A7E1F-D221-4C83-A4DB-F60C8E56FED6-htm.html

    def _quadrant4(self, global_Cord):
        r = self.radius
        p1 = Coordinate(0, self.scale / 2)
        p1_1 = Coordinate(self.scale / 2 - r, self.scale / 2)
        p2 = Coordinate(self.scale / 2, 0)
        p2_2 = Coordinate(self.scale / 2, self.scale / 2 - r)
        x = global_Cord.x * self.scale
        y = global_Cord.y * self.scale
        if self.mode == "line": return ["line", p1.x + x, p1.y + y, p2.x + x, p2.y + y]
        pR = Coordinate(p1_1.x, p2_2.y)
        return [["line", p1.x + x, p1.y + y, p1_1.x + x, p1_1.y + y], \
               ["line", p2.x + x, p2.y + y, p2_2.x + x, p2_2.y + y], \
               ["arc",APoint(pR.x + x, pR.y + y), r, 0, math.pi / 2]]
        # -----1 полилиния--2 полилиния--данные для дуги--
        # построение дуги в автокад https://knowledge.autodesk.com/search-result/caas/CloudHelp/cloudhelp/2016/ENU/AutoCAD-ActiveX/files/GUID-864A7E1F-D221-4C83-A4DB-F60C8E56FED6-htm.html



class drawDWG:
    

    def __init__(self):
        self.path2dwg = ""
        self.data = {}

    def execute(self, data):
        self.data = data
        self.scale = self._getScale()#scale содержит гостовский масштаб
        self.scaledCellSize = self.scale * self.data["CellSize"]

        self.cells = Cells(self.scaledCellSize, self.data["Radius"] * self.scale) # содержит блоки-конструктор для отрисовки конвейера

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
        self._conveyorsDraw()
        self._scaleFigures()
        self._figuresDraw()

        x = input()
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



    def _getFinConv(self, conveyor):
        if len(conveyor[0]) == 0: return []
        finConveyor = copy.deepcopy(conveyor[0])
        for i in [1,2]:
            for f in self.data["Figures"]:
                if conveyor[i] == f.name:
                    figure = f
                    point = conveyor[0][0 if i == 1 else -1]
                    break
            if i == 1:
                finConveyor.insert(0, self._getImaginaryCell(figure, point))
            else:
                finConveyor.append(self._getImaginaryCell(figure, point))
        return finConveyor

    def _getCode(self, coords):
        self.code = str()
        for i in [1, 2]:
            self.code += str(np.sign(coords[i - 1].x - coords[i].x))
            self.code += str(np.sign(coords[i - 1].y - coords[i].y))
        return self.code

    def _conveyorsDraw(self):
        self.coded_conveyors = list()

        # в этом цикле для каждой клетки конвейера получаем код
        for conv in self.data["Conveyors"]:
            #self.coded_conveyor = list()
            #self.coded_conveyor.clear()
            conveyor = self._getFinConv(conv)

            #разбиваем конвейер на клеточки
            for i in range(len(conveyor)):
                self.coded_conveyors.append([self._getCode([conveyor[i-2],conveyor[i-1],conveyor[i]]), conveyor[i-1]])
            #self.coded_conveyors.append(self.coded_conveyor)
            print("*")
        """
        for l in self.coded_conveyors:
            for c in l:
                if len(c) != 0:
                    print(c)
                    print("code", c[0], "x=",c[1].x, "y=", c[1].y)
                    
        """

        #TODO сделать в первую очередь преобразование локальных координат в глобальные
        for cell in self.coded_conveyors:

            try:
                cell_draw = self.cells.getCell(cell[0], cell[1]) #TODO передавать список

                for elem in cell_draw: #if isinstance(cell_draw[0], list) else [cell_draw]:
                    if elem[0] == "line":
                        self.acad.model.AddLightWeightPolyline(array.array("d", elem[1:]))

                    elif elem[0] == "arc":
                        self.acad.model.AddCircle(elem[1], elem[2])
            except KeyError:
                continue
            print("**")



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