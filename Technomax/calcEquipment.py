import numpy as np
import json
from Technomax.Routing_A_Star import Coordinate
import copy
import math


#Обсчет всех геометрических параметров АХПП определяется в этом классе
class AHPP:  # AХПП

    @classmethod
    def get(self, data):
        self.unit_whl = {"w" : float(data["Ширина"]),
                         "l" : float(data['Длина']),
                        "h" : float(data['Высота'])}
        self.speed = float(data['Скорость конвейера'])
        self.sizes = dict()
        self.numOfBath = 0

        # 2.1.1Входная зона
        self.sizes.update({"entranceArea": int(round(self.unit_whl["l"] * 1.2 * 2, -2) // 2)})  # кратно 50
        if self.sizes["entranceArea"] < 2000:  # Чтобы округлить до 50, можно умножить на 2 и округлить до 100:
            self.sizes["entranceArea"] = 2000

            # 2.1.2.Зона перехода
        # TODO добавить выбор зоны по 2 расчетам - либо по умножению, либо по времени 1 мин
        self.sizes.update({"transitionArea": int(round(self.unit_whl["l"] * 1.25 * 2, -2) // 2)})
        if self.sizes["transitionArea"] < 2000:
            self.sizes["transitionArea"] = 2000

        # 2.1.3.Выходная зона
        # TODO добавить выбор зоны по 2 расчетам - либо по умножению, либо по времени 1 мин
        self.sizes.update({"outputArea": int(round(self.unit_whl["l"] * 1.5 * 2, -1) // 2)})
        if self.sizes["outputArea"] < 2000:
            self.sizes["outputArea"] = 2000

        # 2.1.5.Ширина АХПП
        self.sizes.update({"width": self.unit_whl["w"] + 1000})
        if self.sizes["width"] < 1200:
            self.sizes["width"] = 1200

        # 2.1.6Высота АХПП
        self.sizes.update({"height": self.unit_whl["h"] + 900})

        # Длинны ван
        for i in range(6):  # в baths хранятся исходные данные о продолжительности ТО
            curBath = "Ванна №" + str(i+1) #текущй ключ к словарю данных data

            try:
                if data[curBath] == "" or float(data[curBath]) < 1:
                    continue
            except ValueError:
                    continue

            length = int(self.speed * (float(data[curBath]) / 60) * 1000)  # V_конв * t * 1000мм
            if length < 600:
                length = 600
            self.sizes.update({curBath: [float(data[curBath])]})
            self.sizes[curBath].append(length)
            self.sizes[curBath].append(self.sizes["width"] + 750)
            self.numOfBath += 1
            # self.sizes["1bath"] >>[150.0, 'сек', 'Обезжиривание', 7500, 2450.0]

        # 2.3.	Расстояние от АХПП до печи сушки –
        # не менее 600 мм при параллельном расположении,
        # не менее 1000 мм при последовательном
        self.restrictionParalel = 600
        self.restrictionSeqence = 1000

        # 2.1.4.Длинна АХПП кратна
        self.totalLenght = (self.sizes["entranceArea"] +
                      self.sizes["transitionArea"]*(self.numOfBath-1) + self.sizes["outputArea"])
        for i in range(self.numOfBath):
            curBath = "Ванна №" + str(i + 1)  # текущй ключ к словарю self.size
            self.totalLenght += self.sizes[curBath][1] #прибавляем длинну каждой ванны
        self.sizes.update({"totalLenght" : self.totalLenght})

        #Расчет координат входа/выхода относительно start_point

        '''
        s ----------------------------------- x ----- y 
        |                                     |
        IN                AHPP               OUT
        |                                     |
        x ----------------------------------- f
        |
        |
        x
        '''
        self.sizes.update({"In" : Coordinate(self.sizes["width"] / 2, 0)})# in_point
        self.sizes.update({"Out": Coordinate(self.sizes["width"] / 2, self.sizes["totalLenght"])})# out_point

        return self.sizes


#класс для сушки и печи полимеризации одновременно
class Oven():

    def __init__(self, data, type):# type= "Сушка"|"Полимеризация";
        self.type = type #тип печи - либо Oven, либо Dryer
        self.data = data
        self.unit_whl = {"w": float(data["Ширина"]),
                         "l": float(data['Длина']),
                         "h": float(data['Высота'])}
        self.speed = float(data['Скорость конвейера'])
        self.L_work = float(data[type]) * float(data['Скорость конвейера']) * 1000 # мин * м/мин * 1000 мм

        self.configurations = {"oneLoop": self.oneLoop,
                               "twoLoop": self.twoLoop,
                               "fourLoop": self.fourLoop,
                               "snake": self.snake}
        self.path = "../Files/standarts.json"  # путь до JSON файла
        with open(self.path, 'r', encoding="utf-8") as f:
            self.standarts = json.loads(f.read())
        self.EF = self.distSide(R=int(self.data['Radius']), BC=int(self.data['Attach_width']),
                           GL=self.unit_whl["w"], DG=self.unit_whl["w"],
                           ED=self.standarts["Oven"]["minWallTurn"][1])


    def get(self, config): # config - название конфигурации
        return self.configurations[config](self.standarts["Oven"])  # вызываем функцию по конфигурации

    # расчет расстояния до стенки печи. Геометрическое решение см. AutoCAD
    # BC расстояние между креплениями, R радиус поворота, GL ширина детали, DG длина детали, ED требуемый запас по расстоянию
    def distSide(self, R, BC, GL, DG, ED):
        alpha = BC / R * 180 / np.pi
        FBD = np.tan(GL / (DG - BC)) * 90 / np.pi
        ABC = (180 - alpha) / 2
        DBK = 90 - FBD
        DBA = 180 - ABC + FBD
        DB = np.sqrt((((DG - BC) / 2) ** 2 + (GL / 2) ** 2))
        AD = np.sqrt(DB ** 2 + R ** 2 - 2 * DB * R * np.cos(np.deg2rad(DBA)))
        return ED + AD - R  # возвращаю EF


    def oneLoop(self, stdrt):
        self.sizes = dict()
        l_straight = self.L_work
        if self.data['Воздушная завеса']:
            l_straight += (stdrt["minEntr"][1]*2 +
                           2*(int(self.data['numAir'])*stdrt["airСurtain"][1]))
        l_straight = round(l_straight * 2 + 499, -3) // 2 #кратно 500
        self.sizes.update({"totalLenght" : l_straight})

        width = (stdrt["minWallEntr"][1] + stdrt["thicknessSandwich"][1]) * 2 +\
                self.unit_whl["w"]
        width = round(width + 99, -2) #кратно 100
        minWidth = stdrt["minWidthElectro"][1] if self.data['Электронагрев'] else stdrt["minWidth"][1]
        width = minWidth if width < minWidth else width
        self.sizes.update({"width": width})
        #TODO здесь округляю с заданной кратностью. Сделать настройку кратности путем чтения ее из JSON файла
        # Расчет координат входа/выхода относительно start_point
        '''
        s ----------------------------------- L ----- Y
        |                                     |
        IN             Dryer/Oven            OUT
        |                                     |
        W ----------------------------------- f
        |
        |
        X
        '''
        self.sizes.update({"In": Coordinate(self.sizes["width"] / 2, 0)})  # in_point
        self.sizes.update({"Out": Coordinate(self.sizes["width"] / 2, self.sizes["totalLenght"])})  # out_point
        return self.sizes


    def twoLoop(self, stdrt):
        '''
                s -------------------- L ----- Y
                |                      |
                IN                     |
                |       Dryer/Oven     |
               OUT                     |
                |                      |
                W -------------------- f
                |
                |
                X
                '''
        self.sizes = dict()
        l_straight = (self.L_work - np.pi*float(self.data['Radius']))/2 + stdrt["minEntr"][1] +\
                           (int(self.data['numAir'])*stdrt["airСurtain"][1])
        totalLenght = l_straight + float(self.data['Radius']) + self.EF
        totalLenght = round(totalLenght * 2 + 499, -3) // 2  # кратно 500
        self.sizes.update({"totalLenght" : totalLenght})
        width = self.unit_whl["w"] + 2*(float(self.data['Radius'])+
                                        stdrt["minWallEntr"][1] + stdrt["thicknessSandwich"][1])

        width = round(width + 99, -2)  # кратно 100
        minWidth = stdrt["minWidthElectro"][1] if self.data['Электронагрев'] else stdrt["minWidth"][1] #проверка на миним ширину
        width = minWidth if width < minWidth else width
        self.sizes.update({"width": width})
        # TODO здесь округляю с заданной кратностью. Сделать настройку кратности путем чтения ее из JSON файла
        # Расчет координат входа/выхода относительно start_point
        inx = stdrt["minWallEntr"][1] + stdrt["thicknessSandwich"][1] + self.unit_whl["w"]/2
        outx = inx + 2*self.data['Radius']
        self.sizes.update({"In": Coordinate(inx, 0)})  # in_point
        self.sizes.update({"Out": Coordinate(outx, 0)})  # out_point
        return self.sizes

    # 4-ех петелечная. Вход и выход в разных местах
    def fourLoop(self, stdrt):
        '''
        s -------------------- L ----- Y
        |                      |
        IN                     |
        |       Dryer/Oven     |
       OUT                     |
        |                      |
        W -------------------- f
        |
        |
        X
        '''
        self.sizes = dict()

        l_straight = (self.L_work - 3*np.pi * float(self.data['Radius']) + \
                      2*(stdrt["minEntr"][1] + int(self.data['numAir']) * stdrt["airСurtain"][1]) + \
                      self.EF + float(self.data['Radius'])) / 4

        totalLenght = l_straight + float(self.data['Radius']) + self.EF
        totalLenght = round(totalLenght * 2 + 499, -3) // 2  # кратно 500
        self.sizes.update({"totalLenght": totalLenght})
        width = self.unit_whl["w"] * 2 + 2 * (stdrt["minWallEntr"][1] + stdrt["thicknessSandwich"][1]) + \
                    6 * float(self.data['Radius'])

        width = round(width + 99, -2)  # кратно 100
        minWidth = stdrt["minWidthElectro"][1] if self.data['Электронагрев'] else stdrt["minWidth"][1]
        width = minWidth if width < minWidth else width # проверка на миним ширину
        self.sizes.update({"width": width})

        inx = stdrt["minWallEntr"][1] + stdrt["thicknessSandwich"][1] + self.unit_whl["w"] / 2
        outx = inx + 6 * self.data['Radius']
        self.sizes.update({"In": Coordinate(inx, 0)})  # in_point
        self.sizes.update({"Out": Coordinate(outx, 0)})  # out_point
        return self.sizes

    #с 4 петельками, выход и вход расположены рядом
    def snake(self, stdrt):
        '''
        s -------------------- L ----- Y
       IN                      |
       OUT                     |
        |       Dryer/Oven     |
        |                      |
        W -------------------- f
        |
        |
        X
        '''
        self.sizes = dict()

        l_straight = (self.L_work + 2 * (stdrt["minEntr"][1] + int(self.data['numAir']) * stdrt["airСurtain"][1])+\
            5*self.EF - float(self.data['Radius']) - stdrt["minBtwProducts"][1] - \
                      3 * np.pi * float(self.data['Radius']))/4
        totalLenght = l_straight + float(self.data['Radius']) + self.EF
        totalLenght = round(totalLenght * 2 + 499, -3) // 2  # кратно 500
        self.sizes.update({"totalLenght": totalLenght})


        width = self.unit_whl["w"]*2 + 2 * (stdrt["minWallEntr"][1] + stdrt["thicknessSandwich"][1]) + \
                4 * float(self.data['Radius']) + stdrt["minBtwProducts"][1]

        width = round(width + 99, -2)  # кратно 100
        minWidth = stdrt["minWidthElectro"][1] if self.data['Электронагрев'] else stdrt["minWidth"][1]
        width = minWidth if width < minWidth else width  # проверка на миним ширину
        self.sizes.update({"width": width})

        inx = stdrt["minWallEntr"][1] + stdrt["thicknessSandwich"][1] + self.unit_whl["w"] / 2
        outx = inx + self.unit_whl["w"] + stdrt["minBtwProducts"][1]
        self.sizes.update({"In": Coordinate(inx, 0)})  # in_point
        self.sizes.update({"Out": Coordinate(outx, 0)})  # out_point
        return self.sizes


class Equipment():

    def __init__(self, data):
        self.data = data # данные с предыдущего шага
        self.configurations = ["oneLoop","twoLoop", "fourLoop","snake"]
        self.packages_mm = list()  # сюда буду пихать словари с конфигурациями.
        self.packages = list()  # сюда буду пихать словари с конфигурациями.
        self.packagesTransf = list() # конфигурации, переведенные в размеры клеток
        self.get_blocks()

    def ahppCalc(self):
        sizes = AHPP.get(self.data)
        name = "АХПП"
        return name, sizes


    #генерация 4 списков конфигураций
    def dryerCalc(self):
        setDryers = list()
        dryer = Oven(self.data, "Сушка")
        for config in self.configurations:
            setDryers.append(dryer.get(config))
        name = "Сушка"
        return name, setDryers

    def polymerizCalc(self):
        setOvens = list()
        oven = Oven(self.data, "Полимеризация")
        for config in self.configurations:
            setOvens.append(oven.get(config))
        name = "Полимеризация"
        return name, setOvens


    #функция, возвращающая пакеты с размерами фигур в мм
    def getBlocks_mm(self):

        nA, ahpp = self.ahppCalc()
        nD, dryers = self.dryerCalc()
        nO, ovens = self.polymerizCalc()
        for numD, dryer in enumerate(dryers):
            for numO, oven in enumerate(ovens):
                nameDryer = nD + str(numD)
                nameOven = nO + str(numO)
                '''package = {
                    1 : [ahpp['totalLenght'], ahpp['width'], nA, ahpp["In"], ahpp["Out"], nameDryer],
                    2 : [dryer['totalLenght'], dryer['width'], nameDryer, dryer["In"], dryer["Out"], "Кабина"],
                    3 : [11500, 6800, "Кабина", Coordinate(3400, 0), Coordinate(3400, 11500), nameOven],
                    4 : [oven['totalLenght'], oven['width'], nameOven, oven["In"], oven["Out"], "Зона Разгрузки"],
                    # TODO зона разгрузки и погрузки может быть объеденена (как в проекте Брендфорд). Спрашивать об этом можно на этапе задания параметров
                    5 : [5000, 1000, "Зона Разгрузки", Coordinate(500,0), Coordinate(500,5000), "Зона Загрузки"],
                    6 : [5000, 1000, "Зона Загрузки", Coordinate(500,0), Coordinate(500,5000), nA],
                }'''
                package = {
                    1 : [ahpp['totalLenght'], ahpp['width'], nA, Coordinate(0, 0), Coordinate(0, 0), nameDryer],
                    2 : [dryer['totalLenght'], dryer['width'], nameDryer, Coordinate(0, 0), Coordinate(0, 0), "Кабина"],
                    3 : [11500, 6800, "Кабина", Coordinate(0, 0), Coordinate(0, 0), nameOven],
                    4 : [oven['totalLenght'], oven['width'], nameOven, Coordinate(0, 0), Coordinate(0, 0), "Зона Разгрузки"],
                    # TODO зона разгрузки и погрузки может быть объеденена (как в проекте Брендфорд). Спрашивать об этом можно на этапе задания параметров
                    5 : [5000, 1000, "Зона Разгрузки", Coordinate(0, 0), Coordinate(0, 0), "Зона Загрузки"],
                    6 : [5000, 1000, "Зона Загрузки", Coordinate(0, 0), Coordinate(0, 0), nA],
                }
                self.packages_mm.append(package)

        # вывод на печать
        #for p in self.packages_mm:
         #    print(p)

    ##функция, возвращающая пакеты с размерами фигур в клетках
    def get_blocks(self):
        self.getBlocks_mm()
        self.packages = copy.deepcopy(self.packages_mm) #копирование всех конфигураций с объектами
        for i, package in enumerate(self.packages):
            for key in package.keys():
                for j, elem in enumerate(package[key]):
                    if not isinstance(elem, str) and not isinstance(elem, Coordinate):
                        self.packages[i][key][j] = int(round(elem / float(self.data['CellSize'])))
                    if isinstance(elem, Coordinate):
                        # здесь я округляю в меньшую сторону. Может случиться проблема при большом размере клетки. Тогда вход и выход будут одной клеткой.
                        # TODO в будущем подумать над тем, чтобы задать конвейер не одной клеткой, а несколькими клетками.
                        self.packages[i][key][j] = Coordinate(int(math.floor(elem.x / float(self.data['CellSize']))), int(math.floor(elem.y / float(self.data['CellSize']))))

        #вывод на печать
        #for p in self.packages:
        #    print(p)

    def get_area(self):
        return int(float(self.data['Ширина Размещения']) / float(self.data['CellSize'])), int(float(self.data['Высота Размещения']) / float(self.data['CellSize']))

    def get_sequences(self):
        X = [1, 6, 3, 4, 5, 2]
        Y = [3, 4, 1, 2, 5, 6]
        return X, Y
