#здесб подключаются все файлы, которые описывают интерфейс каждого окна

from tkinter import *
from constructor import *
from tkinter import filedialog
from tkinter import messagebox as mb
import os
from PIL import ImageTk, Image
from calcEquipment import *
import parsing



# класс - родитель для всех окон, содержит объекты для всех окон
class Windows():
    root = Tk()

    def __str__(self):  # метод __str__, позволяющий переопределить то, как будет печататься объект:
        return "Windows"

    def __init__(self):

        #координаты расположения окна
        position_x = self.root.winfo_screenwidth() // 2 // 2  # ширина экрана
        position_y = self.root.winfo_screenheight() // 2 // 2  # высота экрана
        self.w = 700
        self.h = 440
        self.root.geometry('{}x{}+{}+{}'.format(self.w, self.h, position_x, position_y))
        self.data = 0 #данные о каждом окне
        #print("заход")
        #self.root.configure(background='#C0C0C0')


    # чтобы не повторяться в потомках, заведем функции для кнопок здесь
    def nextButton(self):
        #print("1")
        self.command = "next"
        self.root.quit()

    def backButton(self):
        self.command = "back"
        self.root.quit()
    """
    def createFrame(self):
        self.root = Frame(height = self.h, width= self.w, bd = 5, bg = 'white', relief=SUNKEN)
        self.root.pack(side='top', fill='both')
    """

    def clearFrame(self):
        for child in self.root.winfo_children():
            child.destroy()

    def startloop(self):
        self.root.mainloop()#здесь начинает исполняться обработчик формы tkinter
        return self.command

    #объявление наиболее повторяющихся кнопок, вперед и назад
    def defaultButtons(self, row):
        nextButton = Button(self.root, text="Назад", command=self.backButton,
                    width=6, height=1, font="Arial 12", bg='#FFD1DC')
        nextButton.grid(row=row, column=0, padx=10, pady=6, sticky='w')

        backButton = Button(self.root, text="Далее", command=self.nextButton,
                    width=6, height=1, font="Arial 12", bg='#D0F0C0')
        backButton.grid(row=row, column=5, padx=10, pady=6, sticky='w')

    def get(self):
        return self.data


class StartWindow(Windows):
    def __str__(self):  # метод __str__, позволяющий переопределить то, как будет печататься объект:
        return "StartWindow"
    def __init__(self):
        super().__init__()
        self.command = ""

        self.root.title('startWindow')

    def create_Project(self):
        self.command = "Create Project"
        super().root.quit()

    def load_Project(self):
        self.command = "Load Project"
        super().root.quit()

    def show(self, data):
        super().clearFrame()
        self.root.geometry('{}x{}+{}+{}'.format(self.w, self.h, 0, 0))
        l = Label(self.root, text="Автоматизированное создание\n планировки",
              font="Arial 16", bd=20, bg = 'white').place(anchor=CENTER, relx=0.5, rely=0.1)

        b1 = Button(self.root, text="Новый проект", command=self.create_Project,
               width=15, height=3, font="Arial 12", bg='#D0F0C0').place(anchor=CENTER, relx=0.3, rely=0.3)
        self.root.bind('<Button-1>', b1)

        b2 = Button(self.root, text="Загрузить проект", command=self.load_Project,
               width=15, height=3, font="Arial 12", bg='#FFD1DC').place(anchor=CENTER, relx=0.7, rely=0.3)
        return self.startloop()






class LoadProject(Windows):
    def __str__(self):  # метод __str__, позволяющий переопределить то, как будет печататься объект:
        return "LoadProject"
    def __init__(self):
        super().__init__()
        self.frame = Frame(self.root)
        self.root.title('LoadProject')



    def show(self, data):
        super().clearFrame()
        self.root.geometry('{}x{}+{}+{}'.format(self.w, self.h, 0, 0))
        l2 = Label(self.root, text="Загрузка",
              font="Arial 12", bd=20).place(anchor=W, relx=0.05, rely=0.05)

        b3 = Button(self.root,text="Новый проект1", command=super().nextButton,
               width=15, height=3, font="Arial 12", bg='#D0F0C0').place(anchor=CENTER, relx=0.3, rely=0.3)

        b4 = Button(self.root, text="Загрузить проект1", command=super().backButton,
               width=15, height=3, font="Arial 12", bg='#FFD1DC').place(anchor=CENTER, relx=0.7, rely=0.3)
        return self.startloop()
# 1 ый шаг
class CreateProject1(Windows):

    def __str__(self):  # метод __str__, позволяющий переопределить то, как будет печататься объект:
        return "CreateProject1"
    def __init__(self):
        super().__init__()
        self.command = ""
        self.contentFields = ["", "", "", ""]
        self.root.title('CreateProject1')

         #0имя проекта
         #1путь до таблицы
         #2путь до строительной подосновы (опционально)
         #3путь до покрасочной кабины (опционально)

        super().clearFrame()


    ## одна функция-вектор для кнопки по открытию всех файлов
    def openFileButton(self, extension, entry):
        path = filedialog.askopenfilename()
        try:
            if path != entry.get() and path != "":
                if os.path.splitext(path)[1] == extension:
                    entry.delete(0, 'end')
                    entry.insert(0, path)
                else:
                    #print(os.path.splitext(path)[1])
                    mb.showerror("Ошибка", f"Файл должен иметь расширение {extension}")
        except Exception:
            mb.showerror("Ошибка", str(Exception))

    #переопределяем метод родительского класса. Здесь загружаем все данные из полей в список
    def nextButton(self):
        i = 0
        children_widgets = self.root.winfo_children()
        for child_widget in children_widgets:
            if child_widget.winfo_class() == 'Entry':
                #print(child_widget.get())
                self.contentFields[i] = child_widget.get()
                i+=1

        self.command = "next"
        self.data = self.contentFields.copy() #return data about fields
        self.root.quit()

    #загрузка текста в форму из списка по порядку
    #TODO замутить JSON
    def loadText2Entry(self):
        i = 0
        for child_widget in self.root.winfo_children():
            if child_widget.winfo_class() == 'Entry':
                child_widget.insert(0, str(self.contentFields[i]))
                i+=1

#TODO убрать поле
    def show(self, data):
        super().clearFrame()
        self.root.geometry('{}x{}+{}+{}'.format(self.w, self.h, 0, 0))
        ###########################
        Label(self.root, text="1 Шаг",font="Arial 12", bd=5).grid(row=0, column=0,sticky='w')
        Label(self.root, text="Имя проекта",font="Arial 12", bd=5).grid(row=1, column=0, padx=2, pady=2, sticky='w')
        self.entry_projectname = Entry(self.root, textvariable=self.contentFields[0], width=40)
        self.entry_projectname.grid(row=2, column=0, padx=10, pady=2, sticky='w', columnspan=2)
        ###########################

        ###########################
        Label(self.root, text="Форма с входными данными, [xlsx]",
                   font="Arial 12", bd=5).grid(row=3, column=0, padx=2, pady=2, sticky='w')

        self.entry_openxsls = Entry(self.root, textvariable=self.contentFields[1], width=80) #grid method of a widget always returns None.
        self.entry_openxsls.grid(row=4, column=0, padx=10, pady=2, sticky='w', columnspan=2)


        b1 = Button(self.root, text="Открыть",
                    command=lambda: self.openFileButton(".xlsx", self.entry_openxsls),
                    font="Arial 12", bg='#D0F0C0')
        b1.grid(row=4, column=2, padx=0, pady=2, sticky='w')

        ##########################

        ###########################
        Label(self.root, text="Строительная подоснова, [dwg]",
              font="Arial 12", bd=5).grid(row=5, column=0, padx=2, pady=2, sticky='w')

        self.entryBaseDwg = Entry(self.root, textvariable=self.contentFields[2], width=80)  # grid method of a widget always returns None.
        self.entryBaseDwg.grid(row=6, column=0, padx=10, pady=2, sticky='w', columnspan=2)

        b1 = Button(self.root, text="Открыть", command=lambda: self.openFileButton(".dwg", self.entryBaseDwg),
                    font="Arial 12", bg='#D0F0C0')
        b1.grid(row=6, column=2, padx=0, pady=2, sticky='w')

        ##########################

        ###########################
        Label(self.root, text="Чертеж покрасочной кабины, [dwg]",
              font="Arial 12", bd=5).grid(row=7, column=0, padx=2, pady=2, sticky='w')

        self.entryPaintDwg = Entry(self.root, textvariable=self.contentFields[3], width=80)  # grid method of a widget always returns None.
        self.entryPaintDwg.grid(row=8, column=0, padx=10, pady=2, sticky='w', columnspan=2)

        Button(self.root, text="Открыть", command=lambda: self.openFileButton(".dwg", self.entryPaintDwg),
                    font="Arial 12", bg='#D0F0C0').grid(row=8, column=2, padx=0, pady=2, sticky='w')
        ##########################

        super().defaultButtons(row=14)
        self.loadText2Entry()
        return self.startloop()


#2 Step, fill in the fields on the form according to the data presented in xslx file
class CreateProject2(Windows):

    def __str__(self):  # метод __str__, позволяющий переопределить то, как будет печататься объект:
        return "CreateProject2"
    def __init__(self):
        super().__init__()
        self.w = 700
        self.h = 900
        self.command = ""
        self.root.title('CreateProject1')
        #self.labelCellSize = "" # размер 1 квадратой клетки
        #self.labelWidthGrid = "" # ширина поля в клетках
        #self.labelHeightGrid = "" # высота поля в клетках
        self.entriesDict = dict() # словарь полей ввода
        self.labelsDict = dict() # словарь лейблов, которые я буду изменять
        self.checkButDict = dict()
        self.data2algoritm = dict() # данные для алгоритма, которые будут в виде:

    '''wid_hei_dict = {
        1: [2, 4, '1_АХПП'],
        2: [1, 3, '2_Печь'],
        3: [3, 3, '3_Печь_2'],
        4: [3, 5, '4_Кабина'],
        5: [3, 2, '5_Зона Загрузки'],
        6: [5, 3, '6_Зона Выгрузки'],
    }'''


    def update_data(self):
        print(self.data.keys())
        for key in self.entriesDict.keys():
            self.data[key] = self.entriesDict[key].get()
        for key in self.checkButDict.keys():
            self.data[key] = self.checkButDict[key].get()
        print(self.data)


    #отоброзить сетку с препятствиями, кол-вом самих клеточек, тд.
    def show_grid_canvas(self, row=20, column=0):
        widthC = self.w - 10 # ширина канваса
        heightC = 450 # высота канваса
        c = Canvas(self.root, width=widthC, height=heightC, bg='white')
        c.grid(row=row, column=column, rowspan=20, columnspan=6)

        koefX = heightC/self.data["GridHeight"]
        koefY = widthC/self.data["GridWidth"]
        # рисую сетку
        for x in range(self.data["GridWidth"] + 1):
            c.create_line(x * koefY, 0, x * koefY, heightC)

        for y in range(self.data["GridHeight"] + 1):
            c.create_line(0, y * koefX, widthC, y * koefX)

        #разкомментировать когда появятся препятствия
        """
        colors = ['#8EEBEC', "#4CC552", "#6CBB3C", "#FFE87C", "#FFCBA4", "#E9AB17", "#F75D59", "#9172EC",
                  "#E78A61"]
        #рисуем фигуры
        for i, f in enumerate(figures):
            c.create_rectangle(f.start_point.y*koef,f.start_point.x*koef,
                               (f.finish_point.y + 1) * koef, (f.finish_point.x + 1)*koef,  fill=colors[i], width=3)
            c.create_oval(f.start_point.y*koef - 5, f.start_point.x*koef - 5,
                          f.start_point.y * koef + 5, f.start_point.x * koef + 5,fill=colors[i])
            c.create_text((f.start_point.y + (f.finish_point.y - f.start_point.y + 1)/2)*koef,
                          (f.start_point.x + (f.finish_point.x - f.start_point.x + 1) / 2)*koef,
                          text=f.name, font="Verdana 10")
        c.pack()
        """


    # calculation of grid size
    def gridEvaluate(self, event):
        for keyE, keyL in zip(["Ширина","Ширина Размещения","Высота Размещения"],["CellSize", "GridWidth", "GridHeight"]):

            if keyL == "CellSize":
                #сравниваем вначале ширину футура и шиирну детали, выбираем наибольшую
                width_Part = float(self.entriesDict["Ширина"].get())
                width_Futur = float(self.entriesDict["Futur"].get())

                two_lambda = width_Part if width_Part >= width_Futur else width_Futur
                self.data[keyL] = int(two_lambda * 5 / 2)  # расчет размера клетки
            else:
                self.data[keyL] = int(float(self.entriesDict[keyE].get()) / self.data["CellSize"])  # расчет ширины и высоты поля в клетках

            self.labelsDict[keyL].configure(text=keyL + ": " + str(self.data[keyL]))

        self.update_data()
        #TODO впихнуть сюда генерацию эквипмента
        self.show_grid_canvas()



    def show(self, dataFromXslx):
        super().clearFrame()
        self.root.geometry('{}x{}+{}+{}'.format(self.w, self.h, 0, 0))
        # TODO сделать итоговый адекватный словарь для передачи его модулю Алгоритма
        self.data = dataFromXslx
        self.entriesDict.clear() #очищаем словарь полей ввода
        self.labelsDict.clear() #очищаем словарь лейблов

        #зная путь до таблицы, генерируем таюлицу на форме
        keys = list(self.data.keys())
        for i, key in enumerate(keys):  # Rows
            # TODO убрать отсюда Obstacles сделать разворачивающийся список с координатами препятствий, их ширинами и высотами
            if key in ["Obstacles", "Строительная подоснова",
                       "Чертеж кабины", "Grid"]:
                continue
            if i in [0, 5, 9]:
                nameLabel = Label(self.root, text=key, font='Helvetica 9 bold')
                nameLabel.grid(row=i, column=0)

            else:
                nameLabel = Label(self.root, text=key)
                nameLabel.grid(row=i, column=0)


            for j, content in enumerate(self.data[key]):  # Columns
                if i in [0,5,9] or j == 1:
                    b = Label(self.root, text=str(content))
                    b.grid(row=i, column=j+1)
                else:
                    if j == 2 and str(content) == "" and i <= 9: #условие i <=9 чтобы отрисовывать поля для названия операций
                        continue
                    b = Entry(self.root, text="")
                    b.bind("<FocusOut>", self.gridEvaluate)
                    b.grid(row=i, column=j + 1, sticky=N)
                    b.insert(0, str(content))
                    if key in self.entriesDict.keys():
                        self.entriesDict.update({str(key + " name") : b})  # создаем словарь полей ввода.
                    else:
                        self.entriesDict.update({key : b}) # создаем словарь полей ввода.

        # отрисовка результатов расчета Входных данных для алгоритма

        #Крупный лейбл Параметры сетки
        b = Label(self.root, text="Параметры сетки", font='Helvetica 9 bold')
        b.grid(row=0, column=4)
        b = Label(self.root, text="Ширина конвейера")
        b.grid(row=1, column=4)

        # создаем Поле для ввода ширины футура
        e = Entry(self.root, justify='center', width=7)
        self.entriesDict.update({"Futur" : e})
        e.grid(row=2, column=4)
        e.insert(0, str("200"))
        e.bind("<FocusOut>", self.gridEvaluate)

        #Вставляем фото сечения FUTUR
        img = ImageTk.PhotoImage(Image.open("Files\Section FUTUR 100.PNG"))
        foto_futur = Label(self.root, image=img)
        foto_futur.grid(row=3, column=4, rowspan=5, sticky=N)

        #TODO занести в словарь координаты препятствий (в клетках)
        self.data.update({"Obstacles": {}}) #добавить потом препятствия в порядковом возврастании
        #в конце заносим новые данные (размер клетки, ширина и высота поля в клетках) в общий словарь
        for i, newKey in enumerate(["CellSize", "GridWidth", "GridHeight"]):
            l = Label(self.root)
            l.grid(row=8+i, column=4, sticky=N)
            self.data.update({newKey: 0})
            self.labelsDict.update({newKey : l})
        keys = list(self.data.keys())
        print(keys)
        self.gridEvaluate(None) # выполнить первичный расчет

        # Крупный лейбл Расстояние креплений
        b = Label(self.root, text="Расстояние креплений", font='Helvetica 9 bold')
        b.grid(row=11, column=4)

        # создаем Поле для ввода расстояние крепления
        e = Entry(self.root, justify='center', width=7)
        self.entriesDict.update({"Attach_width": e})
        e.grid(row=12, column=4)
        e.insert(0, str("4000"))
        e.bind("<FocusOut>", self.gridEvaluate)

        # Вставляем фото чертежа крепления детали
        img2 = ImageTk.PhotoImage(Image.open("Files/attachment_100.png"))
        foto_attach = Label(self.root, image=img2)
        foto_attach.grid(row=13, column=4, rowspan=4, sticky=N)

        # Крупный лейбл Остальные параметры
        b = Label(self.root, text="Параметры печи", font='Helvetica 9 bold')
        b.grid(row=0, column=5)

        cvar1 = BooleanVar()
        cvar1.set(0)
        c1 = Checkbutton(text="Электронагрев", variable=cvar1, onvalue=1, offvalue=0)
        self.checkButDict.update({"Электронагрев" : cvar1})
        c1.grid(row=1, column=5, sticky=W)

        cvar2 = BooleanVar()
        cvar2.set(0)
        c1 = Checkbutton(text="Воздушная завеса", variable=cvar2, onvalue=1, offvalue=0)
        self.checkButDict.update({"Воздушная завеса": cvar2})
        c1.grid(row=2, column=5, sticky=W)

        b = Label(self.root, text="Кол-во завес")
        b.grid(row=3, column=5,sticky="W")

        # создаем Поле для ввода кол-ва воздушных завес
        e = Entry(self.root, justify='center', width=7)
        self.entriesDict.update({"numAir": e})
        e.grid(row=3, column=5, sticky="E")
        e.insert(0, str("0"))
        e.bind("<FocusOut>", self.gridEvaluate)

        b = Label(self.root, text="Кабина нанесения\nкраски", font='Helvetica 9 bold')
        b.grid(row=4, column=5, rowspan=2)

        r_var = StringVar()
        r_var.set("Q-MAX")
        r1 = Radiobutton(text='Серия ТМХ', variable=r_var, value="Серия ТМХ")
        r2 = Radiobutton(text='Q-MAX', variable=r_var, value="Q-MAX")
        r3 = Radiobutton(text='Wagner', variable=r_var, value="Wagner")
        r4 = Radiobutton(text='ColorMax', variable=r_var, value="ColorMax")
        r1.grid(row=6, column=5, sticky=W)
        r2.grid(row=7, column=5, sticky=W)
        r3.grid(row=8, column=5, sticky=W)
        r4.grid(row=9, column=5, sticky=W)
        self.checkButDict.update({"Кабина покраски": r_var})

        # Крупный лейбл Остальные параметры
        b = Label(self.root, text="Радиус поворотов", font='Helvetica 9 bold')
        b.grid(row=10, column=5)

        radius = IntVar()
        radius.set(500)
        r1 = Radiobutton(text='500 мм', variable=radius, value=500)
        r2 = Radiobutton(text='750 мм', variable=radius, value=750)
        r1.grid(row=11, column=5, sticky=W)
        r2.grid(row=12, column=5, sticky=W)
        self.checkButDict.update({"Radius": radius})


        super().defaultButtons(row=18)



        return self.startloop()


#это окно будет отрисовывать окно с полученнрй планировкой, а также будут кнопки для отрисовки данного алгоритма в
# AutoCAD, NX
class GenerateSolution(Windows):

    def __str__(self):  # метод __str__, позволяющий переопределить то, как будет печататься объект:
        return "GenerateSolution"
    def __init__(self):
        super().__init__()
        #self.frame = Frame(self.root)
        self.command = ""
        self.root.title('CreateProject1')

    def show(self, data):
        super().clearFrame()
        self.data = data #
        print("Last Window", self.data)
        #Equipment.getBlocks(data)
        eq = Equipment(data)

        Label(self.root, text="GenerateSolution",
              font="Arial 12", bd=20).place(anchor=W, relx=0.05, rely=0.05)

        b5 = Button(self.root, text="Новый проект3", command=super().nextButton,
               width=15, height=3, font="Arial 12", bg='#D0F0C0').place(anchor=CENTER, relx=0.3, rely=0.3)

        b6 = Button(self.root, text="Загрузить проект3", command=super().backButton,
               width=15, height=3, font="Arial 12", bg='#FFD1DC').place(anchor=CENTER, relx=0.7, rely=0.3)
        return self.startloop()