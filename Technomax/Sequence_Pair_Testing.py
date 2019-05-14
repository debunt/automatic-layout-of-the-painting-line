from Technomax.Placement_Routing import *
#from Technomax import Brandford_1
import random
import math
import copy


class Statistics:
    def __init__(self, m1_count=0, m2_count=0, m3_count=0, bad_variants=0, good_variants=0, AHPP_m3 = 0):
        self.m1_count = m1_count
        self.m2_count = m2_count
        self.m3_count = m3_count
        self.bad_variants = bad_variants
        self.good_variants = good_variants
        self.AHPP_m3 = AHPP_m3

    def get_statistics(self):
        print('m1: {}, m2: {}, m3: {}'.format(self.m1_count, self.m2_count, self.m3_count))
        print('Acception of good variants: ', self.good_variants)
        print('Acception of bad variants: ', self.bad_variants)


class SeqPair:

    def __init__(self, X, Y, wid_hei_dict, delta):
        self.X = X
        self.Y = Y
        self.wid_hei_dict = wid_hei_dict
        self.delta = delta

    def modify_wid_hei_dict(self):
        tmp_wid_hei_dict = dict()
        for key, value in self.wid_hei_dict.items():
            tmp_wid_hei_dict.update({key: [value[0] + self.delta, value[1] + self.delta, value[2]]})
        return tmp_wid_hei_dict

    def find_SP_coordinates(self):

        tmp_wid_hei_dict = self.modify_wid_hei_dict()

        """
                 LCS of              LCS of
        block | (X1; Y1) | x_coor | (XR2 ; Y1) | y_coor
        """
        '''Block position array P[b]; b = 1...n is used to record the x or
        y coordinate of block b depending on the weight w(b) equals
        to the width or height of block b respectively.'''
        P = [0 for _ in range(len(self.X))]

        '''
        To record the indices in both X and Y for each block b, the array match[b]; 
        b = 1...n is constructed to be:
            if b = X[i] = Y [j]: 
                match[b].x = i and match[b].y = j
        '''

        # Далее пусть будет статическим методом

        class ForMatching:
            def __init__(self, x, y):
                self.x = x
                self.y = y

        match = ForMatching({}, {})

        for i in range(len(self.X)):
            for j in range(len(self.X)):
                if self.X[i] == self.Y[j]:
                    # ключ - Название фигуры, значение - индекс в последовательности
                    # в match попадают когда сошлись фигуры в одном списке и другом
                    match.x.update({self.X[i]: i})
                    match.y.update({self.Y[j]: j})
        '''
        The length array L[1...n] is used to record the length of candidates of the 
        longest common subsequence.
        '''
        L = [0 for _ in range(len(self.X))]

        # ALGORITHM for x coordinate:
        for i in range(len(self.X)):
            b = self.X[i]
            p = match.y[b]
            P[b - 1] = L[p]
            tmp = P[b - 1] + tmp_wid_hei_dict[b][0]
            for j in range(p, len(self.X)):
                if tmp > L[j]:
                    L[j] = tmp
                else:
                    break
        x_SP_coordinates = P
        #print(x_SP_coordinates)
        # ALGORITHM for y coordinate:
        P = [0 for _ in range(len(self.X))]
        match = ForMatching({}, {})

        XR = self.X[:]
        XR.reverse()
        for i in range(len(self.X)):
            for j in range(len(self.X)):
                if XR[i] == self.Y[j]:
                    match.x.update({XR[i]: i})
                    match.y.update({self.Y[j]: j})
        L = [0 for _ in range(len(self.X))]
        for i in range(len(self.X)):
            b = XR[i]
            p = match.y[b]
            P[b - 1] = L[p]
            tmp = P[b - 1] + tmp_wid_hei_dict[b][1]
            for j in range(p, len(self.X)):
                if tmp > L[j]:
                    L[j] = tmp
                else:
                    break

        y_SP_coordinates = P
        #print(y_SP_coordinates)

        for i in range(len(x_SP_coordinates)):
            x_SP_coordinates[i] = x_SP_coordinates[i] + self.delta

        for i in range(len(y_SP_coordinates)):
            y_SP_coordinates[i] = y_SP_coordinates[i] + self.delta

        return [x_SP_coordinates, y_SP_coordinates]


class TransformSeqPair:
    def __init__(self):
        pass

    @staticmethod
    def to_passabilities(seq_pair, area):
        x_y_SP_coordinates = seq_pair.find_SP_coordinates()
        figures = []
        for i in range(len(seq_pair.X)):
            figure = Figure(
                Coordinate(
                    x_y_SP_coordinates[0][i],
                    x_y_SP_coordinates[1][i]
                ),
                Coordinate(
                    x_y_SP_coordinates[0][i] + seq_pair.wid_hei_dict[i + 1][0] - 1,
                    x_y_SP_coordinates[1][i] + seq_pair.wid_hei_dict[i + 1][1] - 1
                ),
                seq_pair.wid_hei_dict[i + 1][2],
                seq_pair.wid_hei_dict[i + 1][3],
                seq_pair.wid_hei_dict[i + 1][4],
                seq_pair.wid_hei_dict[i + 1][5],
            )
            figures.append(figure)
        # print('len of figures:', len(figures))
        a = [[]]
        area.clear_map()

        sum_length = 0
        num_of_conveyors_added = 0
        conveyors = []
        del conveyors[:]
        for i in range(len(figures)):
            a = area.figure_adding(figures[i])
        for figure in figures:
            tmp = figure.neighbor_name
            coordinate_to = None
            for now_figure in figures:
                #print(now_figure.name)
                #print(tmp)
                if now_figure.name == tmp:
                    coordinate_to = now_figure.out_point
            a, conveyor = area.conveyor_adding(figure.in_point, coordinate_to)
            conveyors.append(conveyor)
            buf = area.conveyor_adding(figure.in_point, coordinate_to, only_path_len=True)
            if buf != 0:
                sum_length += buf
                num_of_conveyors_added += 1

        return a, figures, num_of_conveyors_added, sum_length, conveyors


class SimAnnealing:

    def __init__(self, init_temperature, frozen_temperature):
        self.temperature = init_temperature
        self.frozen = frozen_temperature

    # TODO Оказалось это должны быть методы класса, т.к. экземпляр класса для их ф-ала создавать не обязательно
    # TODO Методы при каждом вызове меняют seq_pair глобально

    @classmethod
    def m1_perturb(cls, seq_pair):
        rand_ind1 = random.randrange(0, len(seq_pair.X))
        rand_ind2 = random.randrange(0, len(seq_pair.X))

        while rand_ind1 == rand_ind2:
            rand_ind2 = random.randrange(0, len(seq_pair.X))
        seq_pair.X[rand_ind1], seq_pair.X[rand_ind2] = seq_pair.X[rand_ind2], seq_pair.X[rand_ind1]

        return seq_pair

    @classmethod
    def m2_perturb(cls, seq_pair):
        rand_ind1 = random.randrange(0, len(seq_pair.X))
        # rand_ind1 = 1  # Соответсвует седьмой фигуре
        rand_ind2 = random.randrange(0, len(seq_pair.X))
        # rand_ind2 = 6
        while rand_ind1 == rand_ind2:
            rand_ind2 = random.randrange(0, len(seq_pair.X))
        seq_pair.X[rand_ind1], seq_pair.X[rand_ind2] = seq_pair.X[rand_ind2], seq_pair.X[rand_ind1]

        ind1 = seq_pair.Y.index(seq_pair.X[rand_ind2])
        ind2 = seq_pair.Y.index(seq_pair.X[rand_ind1])
        seq_pair.Y[ind1], seq_pair.Y[ind2] = seq_pair.Y[ind2], seq_pair.Y[ind1]

        return seq_pair

    @classmethod
    def m3_perturb(cls, seq_pair):
        rand_ind = random.randrange(1, len(seq_pair.X) + 1)
        seq_pair.wid_hei_dict[rand_ind][0], seq_pair.wid_hei_dict[rand_ind][1] = \
            seq_pair.wid_hei_dict[rand_ind][1], seq_pair.wid_hei_dict[rand_ind][0]
        '''
        seq_pair.wid_hei_dict[rand_ind][3].x, seq_pair.wid_hei_dict[rand_ind][3].y = \
            seq_pair.wid_hei_dict[rand_ind][3].y, seq_pair.wid_hei_dict[rand_ind][3].x
        '''
        '''
        seq_pair.wid_hei_dict[rand_ind][4].x, seq_pair.wid_hei_dict[rand_ind][4].y = \
            seq_pair.wid_hei_dict[rand_ind][4].y - 2, seq_pair.wid_hei_dict[rand_ind][4].x + 2
        '''
        '''
        seq_pair.wid_hei_dict[rand_ind][3].x, seq_pair.wid_hei_dict[rand_ind][4].y = \
            seq_pair.wid_hei_dict[rand_ind][4].x, seq_pair.wid_hei_dict[rand_ind][3].y
        '''
        '''
        seq_pair.wid_hei_dict[rand_ind][3], seq_pair.wid_hei_dict[rand_ind][4] = \
            seq_pair.wid_hei_dict[rand_ind][4], seq_pair.wid_hei_dict[rand_ind][3]
        '''
        return seq_pair

    # Манхетонское расстояние между центрами фигур
    @classmethod
    def get_cost(cls, seq_pair, area):

        tmp_points = seq_pair.find_SP_coordinates()
        start_points_x = tmp_points[0]
        start_points_y = tmp_points[1]
        #sum_length = TransformSeqPair.to_passabilities(seq_pair, area)[3]

        def get_total_area():
            max_x = 0
            for i in range(len(start_points_x)):
                if start_points_x[i] > max_x:
                    max_x = start_points_x[i] + seq_pair.wid_hei_dict[i + 1][0] - 1
            max_height = max_x
            max_y = 0
            for j in range(len(start_points_y)):
                if start_points_y[j] > max_y:
                    max_y = start_points_y[j] + seq_pair.wid_hei_dict[j + 1][1] - 1
            max_width = max_y
            #print(max_width * max_height)
            return max_width, max_height

        def get_total_manhattan_length():
            total_manhattan_length = 0

            def get_central_point(k):
                f_x = start_points_x[k] + seq_pair.wid_hei_dict[k + 1][0] - 1
                f_y = start_points_y[k] + seq_pair.wid_hei_dict[k + 1][1] - 1

                central_point_x = (f_x + start_points_x[k]) / 2
                central_point_y = (f_y + start_points_y[k]) / 2

                return Coordinate(central_point_x, central_point_y)

            for i in range(len(start_points_x)):
                j = i
                while j < len(start_points_x):
                    total_manhattan_length += abs(get_central_point(i).x - get_central_point(j).x) + \
                                         abs(get_central_point(i).y - get_central_point(j).y)
                    j += 1
            return total_manhattan_length

        #def get_total_conveyor_length():
            #return sum_length

        total_area = get_total_area()
        total_manhattan_length = get_total_manhattan_length()
        #total_conveyor_length = get_total_conveyor_length()

        return total_manhattan_length #[1]*total_area[0]# #+  +  total_area[0] * total_area[1] #+  # #+  # + total_conveyor_length

    def sim_annealing(self, seq_pair, area):
        statistics = Statistics(0, 0, 0, 0)

        while self.temperature > self.frozen:
            for _ in range(100):
                prev_seq_pair = copy.deepcopy(seq_pair)
                prev_cost = self.get_cost(prev_seq_pair, area)
                # TODO сделать Тимберфульфа: P(m1)=4/5, P(m2)=1/5. If m1 rejected => m3 with P(1/10)

                random_unif = random.random()
                if random_unif < 0.00001:
                    new_seq_pair = self.m3_perturb(seq_pair)
                    statistics.m3_count += 1
                elif random_unif < 0.4:
                    new_seq_pair = self.m2_perturb(seq_pair)
                    statistics.m2_count += 1

                    delta_cost = self.get_cost(new_seq_pair, area) - prev_cost
                    if delta_cost < 0:
                        seq_pair = new_seq_pair
                        # if seq_pair.wid_hei_dict[5][0] != 2:
                        # print('Загрузка/выгрузка perturbation')
                        statistics.good_variants += 1
                    elif random.uniform(0.01, 1.0) < (math.e ** (-1 / (self.temperature / 80))) and delta_cost > 0:
                        seq_pair = new_seq_pair
                        statistics.bad_variants += 1
                    else:
                        seq_pair = prev_seq_pair
                else:
                    new_seq_pair = self.m1_perturb(seq_pair)
                    statistics.m1_count += 1
                    delta_cost = self.get_cost(new_seq_pair, area) - prev_cost
                    if delta_cost < 0:
                        seq_pair = new_seq_pair
                        # if seq_pair.wid_hei_dict[5][0] != 2:
                        # print('Загрузка/выгрузка perturbation')
                        statistics.good_variants += 1
                    elif random.uniform(0.01, 1.0) < (math.e ** (-1 / (self.temperature / 40))) and delta_cost > 0:
                        seq_pair = new_seq_pair
                        statistics.bad_variants += 1
                    else:
                        if random.random() < 0.5:
                            new_seq_pair = self.m3_perturb(seq_pair)
                            statistics.m3_count += 1
                            seq_pair = new_seq_pair
                        else:
                            seq_pair = prev_seq_pair
            # SCHEDULE
            if self.temperature > 30:
                self.temperature = float('{:.{}f}'.format(self.temperature, 10)) * 0.8
            elif self.temperature > 15:
                self.temperature = float('{:.{}f}'.format(self.temperature, 10)) * 0.95
            else:
                self.temperature = float('{:.{}f}'.format(self.temperature, 10)) * 0.8
        print('Cost after annealing:', self.get_cost(seq_pair, area))
        statistics.get_statistics()
        return seq_pair

    '''
    def sim_annealing_M3(self, seq_pair, area):
        #passabilities = TransformSeqPair.to_passabilities(self.sim_annealing(seq_pair, area), area)
        passabilities = TransformSeqPair.to_passabilities(seq_pair, area)
        # M3
        while self.temperature > self.frozen:
            for _ in range(10):
                prev_seq_pair = copy.deepcopy(seq_pair)
                prev_cost = self.get_cost(prev_seq_pair, area)
                new_seq_pair = seq_pair
                prev_passabilities = TransformSeqPair.to_passabilities(seq_pair, area)
                new_passabilities = prev_passabilities
    
                if random.random() < 0.5:
                    new_seq_pair = self.m3_perturb(seq_pair)
                    new_passabilities = TransformSeqPair.to_passabilities(seq_pair, area)
                delta_cost = self.get_cost(new_seq_pair, area) - prev_cost
                # print(delta_cost)
                # TODO глобально меняет seq_pair, поэтому все PERTURB аксептятся
                if delta_cost > 0:
                    seq_pair = prev_seq_pair
                    passabilities = prev_passabilities
                elif random.uniform(0, 1) > math.e ** ((delta_cost / self.temperature) * 100):
                    seq_pair = prev_seq_pair
                    passabilities = prev_passabilities                    
                else:
                    seq_pair = new_seq_pair
                    passabilities = new_passabilities
    
            self.temperature = float('{:.{}f}'.format(self.temperature, 100000)) * 0.2
    
        print('Cost after M3:', self.get_cost(seq_pair, area))
        return passabilities
    '''
"""
### Rules ###
(<...xi..xj... > , < ...xi..xj...>)) x[i] is left to x[j]
(<...xj..xi... > , < ...xi..xj...>)) x[i] is below x[j]
1) if bi is after bj in X and before bj in Y , then bi is before
bj in XR and before bj in Y , and
2) if bi is before bj in XR and before bj in Y , then bi is
after bj in X and before bj in Y
"""

# seq_pair = [[1, 7, 4, 5, 2, 6, 3, 8], [8, 4, 7, 2, 5, 3, 6, 1]]

# TODO Сделать нормальные ключи для словарей
'''
wid_hei_dict = {
    1: [2, 4, '1_АХПП'],
    2: [1, 3, '2_Печь'],
    3: [3, 3, '3_Печь_2'],
    4: [3, 5, '4_Кабина'],
    5: [3, 2, '5_Зона Загрузки'],
    6: [5, 3, '6_Зона Выгрузки'],
    7: [1, 2, '7_Курилка'],
    8: [2, 4, '8_Паркет'],
}

'''







from calcEquipment import Equipment

class Algorithm():
    #data - данные с предыдущего этапа
    def __init__(self):
        pass

    def execute(self, data):
        self.data = data
        eq = Equipment(data)
        ar = eq.get_area()
        area = Area(ar[0], ar[1])
        area.draw_map()

        wid_hei_dict = eq.packages[12]
        print(wid_hei_dict)

        X, Y = eq.get_sequences()

        init_seq_pair = SeqPair(X, Y, wid_hei_dict, delta=2)
        print('Initial cost:', SimAnnealing.get_cost(init_seq_pair, area))

        annealed_seq_pair = SimAnnealing(40, 0.1)
        res_of_simulation = annealed_seq_pair.sim_annealing(init_seq_pair, area)
        final_SP = res_of_simulation

        print('Simulation succeed!')
        '''
        a = res_of_simulation[0]
        figures = res_of_simulation[1]
        '''

        work_shop = TransformSeqPair.to_passabilities(final_SP, area)
        a = work_shop[0] #матрица после работы алгоритма routing
        figures = work_shop[1] #выбранный словарь для отрисовки

        conveyors = work_shop[4]

        self.data.update({"Routing" : a})
        self.data.update({"Figures": figures})
        self.data.update({"Conveyors" : conveyors})

        return "next"

    def get(self):
        return self.data
