from tkinter import *
#pip install Pillow


class Draw():

    @staticmethod
    def window(ar, figures, area):
        colors = ['#4aa755', "#c3cd4e", "#f5cb22", "#f2672c", "#e22f74", "#90509b", "#0846e4", "#00968d",
                  "#ededed"]

        root = Tk()
        #width_canvas = max([f.finish_point.y for f in figures]) + 1
        #height_canvas = max([f.finish_point.x for f in figures]) + 1
        width_canvas = ar[0]
        height_canvas = ar[1]

        koef = 25 # был 25
        c = Canvas(root, width=width_canvas*koef, height=height_canvas*koef, bg='white')
        c.pack()

        #рисую сетку
        for x in range(width_canvas + 1):
            c.create_line(x*koef, 0, x*koef, height_canvas*koef)
            c.create_text((x + 0.5) *koef, 0.5*koef, text=x, font="Verdana 10")

        for y in range(height_canvas + 1):
            c.create_line(0, y*koef, width_canvas*koef, y*koef)
            c.create_text(0.5 * koef, (y + 0.5) * koef, text=y, font="Verdana 10")



        #рисуем фигуры
        for i, f in enumerate(figures):
            c.create_rectangle(f.start_point.y*koef,f.start_point.x*koef,
                               (f.finish_point.y + 1) * koef, (f.finish_point.x + 1)*koef,  fill=colors[i], width=3)
            c.create_oval(f.start_point.y*koef - 5, f.start_point.x*koef - 5,
                          f.start_point.y * koef + 5, f.start_point.x * koef + 5, fill=colors[i])
            c.create_text((f.start_point.y + (f.finish_point.y - f.start_point.y + 1)/2)*koef,
                          (f.start_point.x + (f.finish_point.x - f.start_point.x + 1) / 2)*koef,
                          text=f.name, font="Verdana 10")
        indicies = []
        for line in area:
            indicies.append([ind for ind, n in enumerate(line) if n == -2])

        # закрашиваем путь
        for row, ind in enumerate(indicies):
            for i in ind:
                c.create_rectangle(i * koef, row * koef,(i + 1) * koef, (row + 1) * koef, fill="#463E3F", width=3)
        c.pack()
        root.mainloop()

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
