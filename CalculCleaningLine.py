#Calculation general sizes of Cleaning Line (AХПП)
#before start, download pandas, xlrd in virtual environment

import xlrd
import pprint

##class EquipmentBase:
  #  def __init__(self, )

class Data:
    
    def __init__(self, xslxName):
        reader = xlrd.open_workbook(xslxName).sheet_by_name("Лист1")
        self.data = {}
        for i in range(reader.nrows):
            if reader.cell_value(i, 0) != xlrd.empty_cell.value:
                val = reader.cell_value(i, 0) #current value of general coloumn
                self.data.update({val if type(val) == str else int(val) : #замена float на int
                [reader.cell_value(i, 1), reader.cell_value(i, 2), reader.cell_value(i, 3),]})  
                
        self.baths = []#data about baths
        for i in range(1 , int(self.data["Количество ванн"][0] + 1)):
                self.baths.append(self.data[i]) #list in order of sequence
        self.speed = self.data["Скорость конвейера"][0]
        self.whl = {"w" : self.data["Ширина"][0], "h" : self.data["Высота"][0], "l": self.data["Длина"][0]}
    


class AHPP:#AХПП
    def __init__(self, unit_whl, speed, baths):
        self.unit_whl = unit_whl #0Width, 1height, 2length
        self.speed = speed 
        self.sizes = dict()

        #2.1.1Входная зона                     
        self.sizes.update({"entranceArea" : int(round(self.unit_whl["l"] * 1.2 * 2, -2) // 2)}) #кратно 50
        if self.sizes["entranceArea"] < 2000: #Чтобы округлить до 50, можно умножить на 2 и округлить до 100:
            self.sizes["entranceArea"] = 2000 

        
        #2.1.2.Зона перехода 
        #TODO добавить выбор зоны по 2 расчетам - либо по умножению, либо по времени 1 мин
        self.sizes.update({"transitionArea" : int(round(self.unit_whl["l"] * 1.25 * 2, -2) // 2)})
        if self.sizes["transitionArea"] < 2000: 
            self.sizes["transitionArea"] = 2000
        
        #2.1.3.Выходная зона 
        #TODO добавить выбор зоны по 2 расчетам - либо по умножению, либо по времени 1 мин
        self.sizes.update({"outputArea" : int(round(self.unit_whl["l"] * 1.5 * 2, -1) // 2)})
        if self.sizes["outputArea"] < 2000: 
            self.sizes["outputArea"] = 2000
        
        #2.1.5.Ширина АХПП
        self.sizes.update({"width" : self.unit_whl["w"] + 1000})
        if self.sizes["width"] < 1200:
            self.sizes["width"] = 1200
        
        #2.1.6Высота АХПП
        self.sizes.update({"height" : self.unit_whl["h"] + 900})

        #Длинны ван
        for i in range(len(baths)):#в baths хранятся исходные данные о продолжительности ТО
            length = int(self.speed * (baths[i][0] / 60) * 1000) # V_конв * t * 1000мм
            if length < 600:
                length = 600
            self.sizes.update({str(i + 1) + "bath" : baths[i]})
            self.sizes[str(i + 1) + "bath"].append(length)
            self.sizes[str(i + 1) + "bath"].append(self.sizes["width"] + 750)
            #self.sizes["1bath"] >>[150.0, 'сек', 'Обезжиривание', 7500, 2450.0]
        
        #2.3.	Расстояние от АХПП до печи сушки – 
        # не менее 600 мм при параллельном расположении, 
        # не менее 1000 мм при последовательном
        self.restrictionParalel = 600
        self.restrictionSeqence = 1000
        
           
        #2.1.4.Длинна АХПП кратна 
        #TODO варьировать величинами до округления полной длины



if __name__ == "__main__":
    # path = input("Введите путь до Excel файла")

    inputData = Data("Входные_Данные.xlsx") # dictionary in output
    #pprint.pprint(inputData.baths)
    ahpp = AHPP(inputData.whl, inputData.speed, inputData.baths)


    