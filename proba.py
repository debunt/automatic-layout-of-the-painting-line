"""

файл нужен для тестирования работы генератора фигур
"""


from calcEquipment import *
import numpy as np




data = {'Имя параметра': ['Значение', 'СИ', ''], 'Ширина Размещения': '55000.0', 'Высота Размещения': '15000.0', 'Скорость конвейера': '3.0', 'Шаг цепи': '200.0', 'Размеры детали': ['', '', ''], 'Длина': '3800.0', 'Ширина': '700.0', 'Высота': '1800.0', 'Рекомендации Химиков': ['', '', 'Название Операции'], 'Ванна №1': '150.0', 'Ванна №2': '60.0', 'Ванна №3': '60.0', 'Ванна №4': '', 'Ванна №5': '', 'Ванна №6': '', 'Сушка': '11.0', 'Полимеризация': '21.0', 'Строительная подоснова': '', 'Чертеж кабины': '', 'Obstacles': {}, 'CellSize': 1542.0, 'GridWidth': 35, 'GridHeight': 9, 'Ванна №1 name': 'Обезжиривание', 'Ванна №2 name': 'Промывка', 'Ванна №3 name': 'Промывка деми', 'Ванна №4 name': '', 'Ванна №5 name': '', 'Ванна №6 name': '', 'Сушка name': '', 'Полимеризация name': '', 'Futur': '200', 'Attach_width': '2800', 'numAir': '0', 'Электронагрев': False, 'Воздушная завеса': False, 'Кабина покраски': 'Q-MAX', 'Radius': 500}

eq = Equipment(data)

"""
for p in eq.packages_mm:
    print(p[1][2], p[1][0], p[1][1], p[1][3], p[1][4])
"""

for p, p_mm in zip(eq.packages, eq.packages_mm):
    print(p_mm[4][2], p_mm[4][0], p_mm[4][1], p_mm[4][3], p_mm[4][4])
    print(p[4][2], p[4][0], p[4][1], p[4][3], p[4][4])
    print(" ")

