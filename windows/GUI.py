from tkinter import *


# класс - родитель для всех окон
class GUI():
    root = Tk()
    def __init__(self):
        #координаты расположения окна
        position_x = self.root.winfo_screenwidth() // 2 // 2  # ширина экрана
        position_y = self.root.winfo_screenheight() // 2 // 2  # высота экрана
        self.root.geometry('600x400+{}+{}'.format(position_x, position_y))

    #вызывается после создания всех объектов окон
    def startLoop(self):
        self.root.mainloop()


class MainWindow(GUI):
    def __init__(self):
        self.root.title('MainWindow')


#https://younglinux.info/tkinter/grid



