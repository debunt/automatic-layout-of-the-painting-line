from pyautocad import Autocad, APoint
from pyautocad import ACAD
import math
import time


class Shape:

    def __init__(self, base_point, sizes, phi):
        self.points = dict()
        self.points.update({"base_point" : APoint(base_point[0], base_point[1])})
        self.sizes = sizes
        self.phi = phi * math.pi / 180  #deg2rad
        self._prepPoints()


    # TODO: после поворота, возникают погрешности. Скорее всего sin(90), cos(0) не чистая "1"
    def _prepPoints(self):

        # check if we already did it
        if "overallDim" not in self.points.keys():
            self.points.update({"overallDim": []})  # overall dimensions
            width = self.sizes["width"]
            length = self.sizes["length"]
            bp = self.points["base_point"]
    #         p3___________p2
    #        |               |
    #        |               |
    #        |bp___________p1|

            self.points["overallDim"].append(bp)  # add bp in list

            # first point, p[0] -> x, p[1] -> y
            p = [int(bp.x + length * math.cos(self.phi)), int(bp.y + length * math.sin(self.phi))]
            self.points["overallDim"].append(APoint(p[0], p[1])) # point 1

            # second point, p[0] -> x, p[1] -> y
            p = [int(p[0] - width * math.sin(self.phi)), int(p[1] + width * math.cos(self.phi))]
            self.points["overallDim"].append(APoint(p[0], p[1])) # point 2

            # third point, p[0] -> x, p[1] -> y
            p = [int(p[0] - length * math.cos(self.phi)), int(p[1] - length * math.sin(self.phi))]
            self.points["overallDim"].append(APoint(p[0], p[1]))  # point 3





class CadAhpp(Shape):

    def __init__(self, base_point, sizes, phi):
        super().__init__(base_point, sizes, phi)  # initialization of parent class
        self.label = "Агрегат химической подготовки поверхности L={len}".format(
            len=sizes["length"])


class CadDryer(Shape):
    def __init__(self, base_point, sizes, phi):
        super().__init__(base_point, sizes, phi)  # initialization of parent class
        self.label = "Печь сушки L={len}".format(len=sizes["length"])


class CadPolimer(Shape):
    def __init__(self, base_point, sizes, phi):
        super().__init__(base_point, sizes, phi)  # initialization of parent class
        self.label = "Печь полимеризации L={len}".format(len=sizes["length"])

class CadQMax(Shape):
    def __init__(self, base_point, sizes, phi):
        super().__init__(base_point, sizes, phi)  # initialization of parent class
        self.label = "Кабина для нанесения порошковой окраски"


class DrawCAD:
    def __init__(self):
        self.acad = Autocad(create_if_not_exists=True)  # so far app is not open
        self.dimscale = 100 # annotative scale for sizes #TODO масштаб должен настраиваться автоматически
        print("AutoCad запущен. Создан документ", self.acad.doc.Name)
        self.acad.Application.Documents.open("d:\Picture_ENG.dwg") #TODO путь с пробелами вызывает трудности
        print(self.acad.doc.Name)
        self.acad.size_scale(self.dimscale) # setting annotative scale for sizes
        self._clear()#стирание из файла


    def _clear(self):
        #TODO убрать костыль так, чтобы удаление не вызывало исключений
        while True:
            try:
                for obj in self.acad.iter_objects():
                    obj.Delete()
                break
            except Exception:
                print("Exception: ошибка при удалении. Выход из исключения, продолжение работы")
                continue


    def _drawLabel(self, shape):
        #TODO в зависимости от ориентации блока, вывести текст в середине
        print(shape.label)

    #drawing shapes consisting of points
    def _drawOverallDim(self, shape):
        #connecting all points of overall dimensions
        num = len(shape.points["overallDim"])
        for i in range(num - 1):
            self.acad.model.AddLine(shape.points["overallDim"][i], shape.points["overallDim"][i + 1])

        # to close the shape
        self.acad.model.AddLine(shape.points["overallDim"][num - 1], shape.points["overallDim"][0])

        # draw overall sizes: horizontal and vertical #TODO проверить работу простановки размеров на повернутых объектах
        self._drawSize(shape.points["overallDim"][0], shape.points["overallDim"][1], 2000)
        self._drawSize(shape.points["overallDim"][0], shape.points["overallDim"][3], 1000)


    # drawing size btw 2 points and with defined indent
    def _drawSize(self, p1, p2, indent):
        self.acad.linear_size(p1.x, p1.y, p2.x, p2.y, indent)

    def draw(self, shape):
        self._drawOverallDim(shape)



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

