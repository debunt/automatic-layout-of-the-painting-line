import xlrd
import os

"""
This class parse xslx file and return data
if xslx file is not transfered to this class
this class open template xslx file, situated in root folder"""

class ParsingXslx:

    def __init__(self):
        self.parsingData = {}


    def execute(self, data):

        #if field in previous stage has path to file, lets use that else use template
        if data[1] != "":
            path2File = data[1]
        else:
            path2File = "Files/templateInputData.xlsx"

        reader = xlrd.open_workbook(path2File).sheet_by_name("Лист1")
        self.parsingData = {}
        for i in range(reader.nrows):
            if reader.cell_value(i, 0) != xlrd.empty_cell.value:
                val = reader.cell_value(i, 0)  # current value of general coloumn
                self.parsingData.update({val if type(val) == str else int(val):  # замена float на int
                                             [reader.cell_value(i, 1), reader.cell_value(i, 2),
                                              reader.cell_value(i, 3), ]})

        self.parsingData.update({"Строительная подоснова" : data[2]})
        self.parsingData.update({"Чертеж кабины": data[3]})
        return "next"

    def get(self):
        return self.parsingData