# from Vladislav

class Coordinate:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __str__(self):
        return "(x:{}, y:{})".format(self.x, self.y)

    def get_length(self, other):  # Манхетоновское расстояние
        return abs(self.x - other.x) + abs(self.y - other.y)


class Routing:
    class Node:
        def __init__(self, parent, coordinate):  # У узла 2 параметра: имя родителя и координата родителя
            self.parent = parent
            self.coordinate = coordinate
            self.f = 0.0  # Оценочная функция
            self.g = 0.0  # Текущая оценка
            self.h = 0.0  # Эвристическая оценка

        def __eq__(self, other_node):   # Переопределяем встроенный метод "равенство"
            return self.coordinate == other_node.coordinate  # У coordinate уже два поля???

        def generate_children(self, area):  # Открываем потомков
            children = []

            # TODO Рскрытие потомков влияет на работу поиска на графе
            coordinates = [
                Coordinate(self.coordinate.x, self.coordinate.y + 1),
                Coordinate(self.coordinate.x + 1, self.coordinate.y),
                Coordinate(self.coordinate.x - 1, self.coordinate.y),
                Coordinate(self.coordinate.x, self.coordinate.y - 1),
            ]
            for coordinate in coordinates:
                child = self.generate_child(coordinate, area)
                if child:
                    children.append(child)  # Если потомок сущ., добавляем его в список children
            return children

        # Сначала обрабатываются исключения, потом создается объект - потомок
        def generate_child(self, coordinate, area):
            #TODO Исключения не работают, а циклят
            if coordinate.x < 0 or area.height <= coordinate.x:  # Неправильно введена координата
                return None
            if coordinate.y < 0 or area.width <= coordinate.y:
                return None
            if area.get_passability(coordinate) == -1:  # Если координата -- стена
                return None
            if area.get_passability(coordinate) == -2:  # or -2:  # Если координата -- другой конвейер
                return None

            return Routing.Node(self, coordinate)  # Тут важный момент: потомок - это родитель и ????

    @staticmethod
    def get_path(area, coordinate_from, coordinate_to):     # Метод в routing

        if area.get_passability(coordinate_to) == -1:  # or -2:  # Если координата -- другой конвейер
            return []
        if area.get_passability(coordinate_to) == -2:  # or -2:  # Если координата -- другой конвейер
            return []
        if area.get_passability(coordinate_from) == -1:  # or -2:  # Если координата -- другой конвейер
            return []
        if area.get_passability(coordinate_from) == -2:  # or -2:  # Если координата -- другой конвейер
            return []


        root = Routing.Node(None, coordinate_from)          # Первый узел (корень)
        root.g = 0.0
        root.h = root.coordinate.get_length(coordinate_to)  # Эвристика -- манхет. расстояние от нуля до термин. ноды
        #print('root.h =', root.h)
        # TODO root.h = 0 - поиск в ширину
        root.f = root.g + root.h                            # Оценочная функция для корня
        # root.f = root.g
        open_set = list()                                   # OPEN список откуда берутся вершины для раскрытия
        open_set.append(root)
        # print('open_set[0] =', open_set[0].parent)
        closed_set = list()                                 # CLOSED - после того как верш. раскрыли она идет сюда

        while open_set:
            open_set.sort(key=lambda node: node.f)         # Сортируем от мен. к бол. по полю "оцен. ф-ия"
            best_node = open_set[0]                        # Первый(самый дешевый) и будет лучшим
            #print('open_set[0].g =', open_set[0].g)

            if best_node.coordinate == coordinate_to:      # Если лучшая оказалась терминальной, то возвр. путь
                # print('stroka 67')
                path = []
                node = best_node
                # print('node.coordinate =', node.coordinate)
                while node:
                    path.insert(0, node.coordinate)        # Восстанавливаем путь из лучшей ноды
                    node = node.parent
                    # print('while node')
                return path
            open_set.remove(best_node)
            # print('len of openset =',len(open_set))
            closed_set.append(best_node)                   # Отправляем его в список закрытых

            children = best_node.generate_children(area)   # Если best оказался не термин., то открываем потомков дальше
            #print('len of children:', len(children))
            for child in children:
                if child in closed_set:                    # !!! Проверка не было ли такого состояния раньше !!!
                    continue
            # Для потомка находим тек. оценку, эврист. оценку и оценочную функцию

                child.g = best_node.g + area.get_passability(child.coordinate)
                # print(best_node.g, area.get_passability(child.coordinate))
                child.h = child.coordinate.get_length(coordinate_to)
                #print((child.g, child.h))
                child.f = child.g + child.h

                child_from_open_set = None                 # Инициализируем переменную
                for node_from_open_set in open_set:
                    if node_from_open_set == child:
                        child_from_open_set = node_from_open_set
                        break
                if child_from_open_set:
                    if child_from_open_set.g < child.g:
                        continue
                    open_set.remove(child_from_open_set)

                open_set.append(child)
                # print(open_set)
        return []