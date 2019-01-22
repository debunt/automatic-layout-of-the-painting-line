from pyautocad import Autocad, APoint
import math


class Shape:

    def __init__(self, base_point, sizes, phi):
        self.points = dict()
        self.points.update({"base_point" : APoint(base_point[0], base_point[1])})
        self.sizes = sizes
        self.phi = phi * math.pi / 180  # deg2rad
        self._prep_points()


    # TODO: после поворота, возникают погрешности. Скорее всего sin(90), cos(0) не чистая "1"
    def _prep_points(self):

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
        print(self.acad.doc.Name)
        self.acad.size_scale(self.dimscale) # setting annotative scale for sizes
        print("kek")


    def _draw_label(self):
        #TODO в зависимости от ориентации блока, вывести текст в середине
        print(self.label)

    #drawing shapes consisting of points
    def _draw_overall_dim(self, shape):
        #TODO: цвет размеров должен быть другим. Создать слой размеров
        #TODO: https://knowledge.autodesk.com/support/autocad/learn-explore/caas/CloudHelp/cloudhelp/2018/ENU/AutoCAD-Core/files/GUID-9123091A-2DCB-4DE8-983C-F7CA38FA67BE-htm.html
        #TODO: возможно 2017 и ниже autocad не поддерживает команду LAYER
        #connecting all points of overall dimensions
        num = len(shape.points["overallDim"])
        for i in range(num - 1):
            self.acad.model.AddLine(shape.points["overallDim"][i], shape.points["overallDim"][i + 1])

        # to close the shape
        self.acad.model.AddLine(shape.points["overallDim"][num - 1], shape.points["overallDim"][0])

        # draw overall sizes: horizontal and vertical #TODO проверить работу простановки размеров на повернутых объектах
        self._draw_size(shape.points["overallDim"][0], shape.points["overallDim"][1], 2000)
        self._draw_size(shape.points["overallDim"][0], shape.points["overallDim"][3], -1000)


    # drawing size btw 2 points and with defined indent
    def _draw_size(self, p1, p2, indent):
        self.acad.linear_size(p1.x, p1.y, p2.x, p2.y, indent)

    def draw(self, shape):
        self._draw_overall_dim(shape)




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

    blocks = list()
    blocks.append(CadAhpp(bs_axpp, sizesAHPP, phi_axpp))
    blocks.append(CadDryer(bs_dryer, sizesDryer, phi_dryer))
    blocks.append(CadPolimer(bs_oven, sizesOven, phi_oven))
    blocks.append(CadPolimer(bs_1, sizes1, phi_1))


    draw = DrawCAD()
    for block in blocks:
        draw.draw(block)




