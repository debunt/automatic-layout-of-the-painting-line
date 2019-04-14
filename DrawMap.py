from commomClasses import *
from tkinter import *



class drawCanvas:
    @staticmethod
    def draw_map_canvas(sizeW, sizeH, figures): # ширина карты, высота карты, фигуры
        top = Tk()
        koeff = 100
        C = Canvas(top, bg="white", height=sizeH*koeff, width=sizeW*koeff)
            for figure in figures:
                C.create_polygon(figure.start_point.x, figure.start_point.y,
                                 figure.finish_point.x, figure.start_point.y,
                                 ...xn, yn, options)