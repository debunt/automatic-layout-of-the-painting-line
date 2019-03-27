#здесб подключаются все файлы, которые описывают интерфейс каждого окна
from tkinter import *
from constructor import *
from tkinter import filedialog
from tkinter import messagebox as mb
import os
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
        #self.frame = Frame(self.root)
        self.command = ""
        self.root.title('CreateProject1')

    def show(self, dataFromXslx):
        super().clearFrame()
        print(dataFromXslx)
        #зная путь до таблицы, генерируем таюлицу на форме
        keys = list(dataFromXslx.keys())
        for i, key in enumerate(keys):  # Rows
            # TODO убрать отсюда Obstacles сделать разворачивающийся список с координатами препятствий, их ширинами и высотами
            if key in ["Obstacles", "Строительная подоснова", "Чертеж кабины"]:
                continue
            if i in [0, 5, 9]:
                nameLabel = Label(self.root, text=key, font='Helvetica 9 bold')
                nameLabel.grid(row=i, column=0)
            else:
                nameLabel = Label(self.root, text=key)
                nameLabel.grid(row=i, column=0)
            for j, content in enumerate(dataFromXslx[key]):  # Columns
                if i in [0,5,9] or j == 1:
                    b = Label(self.root, text=str(content))
                    b.grid(row=i, column=j+1)
                else:
                    if j == 2 and str(content) == "":
                        continue
                    b = Entry(self.root, text="")
                    b.grid(row=i, column=j + 1)
                    b.insert(0, str(content))
        super().defaultButtons(row=18)
        return self.startloop()


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

        Label(self.root, text="GenerateSolution",
              font="Arial 12", bd=20).place(anchor=W, relx=0.05, rely=0.05)

        b5 = Button(self.root, text="Новый проект3", command=super().nextButton,
               width=15, height=3, font="Arial 12", bg='#D0F0C0').place(anchor=CENTER, relx=0.3, rely=0.3)

        b6 = Button(self.root, text="Загрузить проект3", command=super().backButton,
               width=15, height=3, font="Arial 12", bg='#FFD1DC').place(anchor=CENTER, relx=0.7, rely=0.3)
        return self.startloop()