#здесь будет логика работы всего приложения

from windows import *
from parsing import *
from autoCADparser import parseDWG
from autoCADdrawer import drawDWG
from Technomax.Sequence_Pair_Testing import Algorithm
import copy







class Constructor:
    def __init__(self):
        # Инициализация всех классов, которые требуется запустить с соотвествующей последовательностью, указанной в графе
        self.w = Windows()
        self.startWindow= StartWindow()
        self.loadProject = LoadProject()
        self.createProject1 = CreateProject1()
        self.parsedwg = parseDWG()
        self.parse = ParsingXslx()
        self.createProject2 = CreateProject2()
        self.generateSolution = GenerateSolution()
        self.algorithm = Algorithm()
        self.drawdwg = drawDWG()


        self.exeClass = self.startWindow  #текущее открытое окно приложения, второе поле списка содержит данные
        self.currentData = list()
        # карта(граф) приложения (логика переходов между окнами)
        # это словаь словарей. Первый ключ - объекты-дочки класса Windows
        # второй ключ - посланная команда из этого окна (нажатая кнопка)
        # второй ключ дает доступ к листу, 1 элемент это новый вызываемый объект, второй элемент - объект, у которого требуется получить данные методом get()
        self.appMap = {
            self.startWindow : {"Create Project" : [self.createProject1, self.startWindow], "Load Project" : [self.loadProject, self.startWindow]},
            self.loadProject : {"next": [0,[]], "back": [self.startWindow,[]]},
            self.createProject1 : {"next" : [self.parse, self.createProject1], "back" : [self.startWindow, []]},
            self.parse: {"next": [self.parsedwg, self.parse]},
            self.parsedwg : {"next" : [self.createProject2, self.parsedwg]}, # TODO надо, чтобы парсинг dwg добавил еще элемент в список с координатами препятствий, размерами площади
            self.createProject2 : {"next": [self.algorithm, self.createProject2], "back": [self.createProject1, self.createProject1]},
            self.algorithm : {"next" : [self.generateSolution, self.algorithm]},
            self.generateSolution : {"autocad": [self.drawdwg, self.generateSolution], "nx": [0,[]], "back" : [self.createProject2, self.createProject2], "update" : [self.algorithm, self.createProject2]},
            self.drawdwg : {"done" : [self.generateSolution, self.algorithm]}

        }


    def transferWindow(self, command):
        try:
            self.currentData = self.appMap[self.exeClass][command][1].get()
            self.exeClass = self.appMap[self.exeClass][command][0]
        except KeyError:
            return 0
        return 1

    def start(self):
        command = ""
        while command != "exit": #
            command = self.exeClass.execute(self.currentData) # получаем переданную команду после нажатия кнопки
            print(command)
            self.transferWindow(command) # определяем, какое окно открыть







