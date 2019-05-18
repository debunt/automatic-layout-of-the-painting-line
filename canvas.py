from tkinter import *
#pip install Pillow


class Draw():

    @staticmethod
    def window(data, root, screen_width, screen_height):
        colors = ['#4aa755', "#c3cd4e", "#f5cb22", "#f2672c", "#e22f74", "#90509b", "#0846e4", "#00968d",
                  "#ededed"]

        figures = data["Figures"]
        height_canvas = screen_height - 150

        #запись в один лист координаты конвейеров. Далее планируется выделение максимально удаленной точки по Х и по Y осям
        allCoordinates = list()
        for conveyor in data["Conveyors"]:
            allCoordinates.extend(conveyor[0])

        #поиск максимально удаленной точки среди конвейеров и среди фигур
        occupied_width_canvas = max(max(map(lambda coord: coord.y, allCoordinates)), max([f.finish_point.y for f in figures])) + 2
        occupied_height_canvas = max(max(map(lambda coord: coord.x, allCoordinates)), max([f.finish_point.x for f in figures])) + 2

        max_width_grid = data["GridWidth"]
        max_height_grid = data["GridHeight"]

        area_efficiency = occupied_width_canvas * occupied_height_canvas / (max_width_grid * max_height_grid)

        koef_x = int(screen_width / occupied_width_canvas)
        koef_y = int(height_canvas / occupied_height_canvas)
        koef = min (koef_x, koef_y)
        width_canvas = occupied_width_canvas*koef
        height_canvas = occupied_height_canvas*koef
        c = Canvas(root, width=width_canvas, height=height_canvas, bg='white')
        c.pack()

        #рисую сетку
        for x in range(width_canvas + 1):
            c.create_line(x*koef, 0, x*koef, height_canvas*koef)
            c.create_text((x + 0.5) *koef, 0.5*koef, text=x, font="Verdana 10")

        for y in range(height_canvas + 1):
            c.create_line(0, y*koef, width_canvas*koef, y*koef)
            c.create_text(0.5 * koef, (y + 0.5) * koef, text=y, font="Verdana 10")

        for i, conveyor in enumerate(data["Conveyors"]):
            for coord in conveyor[0]:
                c.create_rectangle(coord.y*koef, coord.x*koef, (coord.y+1)*koef, (coord.x+1)*koef, fill="#463E3F", width=3)
                c.create_text((coord.y + 0.5)*koef, (coord.x + 0.5)*koef, text=str(i), font="Verdana 10", fill="white")
            print(i, conveyor[1], conveyor[2])
        #рисуем фигуры
        for i, f in enumerate(figures):
            c.create_rectangle(f.start_point.y*koef,f.start_point.x*koef,
                               (f.finish_point.y + 1) * koef, (f.finish_point.x + 1)*koef,  fill=colors[i], width=3)
            c.create_oval(f.start_point.y*koef - 5, f.start_point.x*koef - 5,
                          f.start_point.y * koef + 5, f.start_point.x * koef + 5, fill=colors[i])
            c.create_text((f.start_point.y + (f.finish_point.y - f.start_point.y + 1)/2)*koef,
                          (f.start_point.x + (f.finish_point.x - f.start_point.x + 1) / 2)*koef,
                          text=f.name, font="Verdana 10")
            c.create_oval(f.in_point.y * koef - 3, f.in_point.x * koef - 3,
                          f.in_point.y * koef + 3, f.in_point.x * koef + 3, fill="yellow")

            c.create_oval(f.out_point.y * koef - 3, f.out_point.x * koef - 3,
                          f.out_point.y * koef + 3, f.out_point.x * koef + 3, fill="blue")



        c.pack()

        #возвращаю размеры занятого пространства. Они пригодятся для отрисовки цеха на чертеже
        return occupied_width_canvas, occupied_height_canvas

    @staticmethod
    def window_2(ar, figures):
        colors = ['#4aa755', "#c3cd4e", "#f5cb22", "#f2672c", "#e22f74", "#90509b", "#0846e4", "#00968d",
                  "#ededed"]

        root = Tk()
        # width_canvas = max([f.finish_point.y for f in figures]) + 1
        # height_canvas = max([f.finish_point.x for f in figures]) + 1
        width_canvas = ar[0]
        height_canvas = ar[1]

        koef = 25  # был 25
        c = Canvas(root, width=width_canvas * koef, height=height_canvas * koef, bg='white')
        c.pack()

        # рисую сетку
        for x in range(width_canvas + 1):
            c.create_line(x * koef, 0, x * koef, height_canvas * koef)
            c.create_text((x + 0.5) * koef, 0.5 * koef, text=x, font="Verdana 10")

        for y in range(height_canvas + 1):
            c.create_line(0, y * koef, width_canvas * koef, y * koef)
            c.create_text(0.5 * koef, (y + 0.5) * koef, text=y, font="Verdana 10")

        # рисуем фигуры
        for i, f in enumerate(figures):
            c.create_rectangle(f.start_point.y * koef, f.start_point.x * koef,
                               (f.finish_point.y + 1) * koef, (f.finish_point.x + 1) * koef, fill=colors[i], width=3)
            c.create_oval(f.start_point.y * koef - 5, f.start_point.x * koef - 5,
                          f.start_point.y * koef + 5, f.start_point.x * koef + 5, fill=colors[i])
            c.create_text((f.start_point.y + (f.finish_point.y - f.start_point.y + 1) / 2) * koef,
                          (f.start_point.x + (f.finish_point.x - f.start_point.x + 1) / 2) * koef,
                          text=f.name, font="Verdana 10")
        c.pack()
        root.mainloop()
