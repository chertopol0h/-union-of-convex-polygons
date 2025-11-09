"""
Николаенко Михаил Владимирович 4.4

10. Объединение выпуклых полигонов
"""

from tkinter import *


# функция определяет, с какой стороны от вектора находится точка
# (положительное возвращаемое значение соответствует левой стороне, отрицательное — правой, 0 - принадлежит).
def rotate(line_from, line_to, point):
  return (line_to[0] - line_from[0]) * (point[1] - line_to[1]) - (line_to[1] - line_from[1]) * (point[0] - line_to[0])


# find rightest point in polygon
def right_point(points):
    rightest_point = [-1000000, 0]
    for point in points:
        if point[0] > rightest_point[0]:
            rightest_point = point
    return rightest_point


# find leftest point in polygon
def left_point(points):
    leftest_point = [1000000, 0]
    for point in points:
        if point[0] < leftest_point[0]:
            leftest_point = point
    return leftest_point


# сортирует points по уменьшению y
def bubble_biggest_y(true_points):
    points = true_points.copy()
    for i in range(len(points) - 1):
        for j in range(len(points) - i - 1):
            if points[j][1] < points[j+1][1]:
                buff = points[j]
                points[j] = points[j+1]
                points[j+1] = buff
    return points


def find_vr(pointsR, vl, type):
    pointsR_sorted = bubble_biggest_y(pointsR)
    vr = pointsR_sorted[0]
    for cur_point in pointsR_sorted:
        if type == 'upper':
            if rotate(vl, vr, cur_point) > 0:
                vr = cur_point
            for point in pointsR_sorted:
                if rotate(vl, vr, point) > 0:
                    vr = point
                    continue
        else:
            if rotate(vl, vr, cur_point) < 0:
                vr = cur_point
            for point in pointsR_sorted:
                if rotate(vl, vr, point) < 0:
                    vr = point
                    continue
    return vr


def find_vl(pointsL, vr, type):
    pointsL_sorted = bubble_biggest_y(pointsL)
    vl = pointsL_sorted[0]
    for cur_point in pointsL_sorted:
        if type == 'upper':
            if rotate(vr, vl, cur_point) < 0:
                vl = cur_point
            for point in pointsL_sorted:
                if rotate(vr, vl, point) < 0:
                    vl = point
                    continue
        else:
            if rotate(vr, vl, cur_point) > 0:
                vl = cur_point
            for point in pointsL_sorted:
                if rotate(vr, vl, point) > 0:
                    vl = point
                    continue
    return vl


def jarvismarch(A):
    n = len(A)
    P = list(range(n))
    # start point
    for i in range(1,n):
        if A[P[i]][0]<A[P[0]][0]:
            P[i], P[0] = P[0], P[i]
    H = [P[0]]
    del P[0]
    P.append(H[0])
    while True:
        right = 0
        for i in range(1,len(P)):
            if rotate(A[H[-1]],A[P[right]],A[P[i]])<0:
                right = i
        if P[right]==H[0]:
            break
        else:
            H.append(P[right])
            del P[right]
    return H


class Window:
    size = 500

    def __init__(self):
        self.window = Tk()
        self.full_figure = False
        self.full_figure2 = False
        # point
        self.point = False
        self.point2 = False
        self.point_x = 0
        self.point_y = 0
        self.window.title("MECHMAT SILA")
        self.window.resizable(False, False)
        # current figure
        self.points = []
        # current figure 2
        self.points2 = []
        # canvas
        self.canvas = Canvas(self.window, width=self.size, height=self.size, background='white')
        self.canvas.grid(row=0, column=0)
        # mouse clicks
        self.canvas.bind("<ButtonRelease-1>", self.left_button_release)
        self.canvas.bind("<ButtonRelease-2>", self.right_button_release)

        # clear button
        self.clear_button = Button(self.window, text='Clear', command=self.clear_window)
        self.clear_button.grid(row=2, column=3)
        # self.clear_button.pack()

        # go button
        self.go_button = Button(self.window, text='Go', command=self.start_algorithm)
        self.go_button.grid(row=1, column=3)

        self.window.mainloop()

    def clear_window(self):
        self.canvas.delete("all")
        self.full_figure = False
        self.full_figure2 = False
        self.points = []
        self.points2 = []
        # self.image = Image.new('RGB', (self.DEFAULT_WIDTH, self.DEFAULT_WIDTH), 'white')
        # self.draw = ImageDraw.Draw(self.image)

    def start_algorithm(self):
        lines = self.merge(pointsL=self.points, pointsR=self.points2)
        lower = lines[0]
        upper = lines[1]
        self.canvas.create_line(upper[0][0], upper[0][1], upper[1][0], upper[1][1], fill="red", width=2)
        self.canvas.create_line(lower[0][0], lower[0][1], lower[1][0], lower[1][1], fill="red", width=2)

    def left_button_release(self, event):
        x, y = event.x, event.y
        if not self.full_figure:
            if self.points == []:
                self.points.append([x, y])
                self.canvas.create_oval(x, y, x - 1, y - 1)
            else:
                x0, y0 = self.points[-1]
                self.canvas.create_line(x0, y0, x, y)
                self.points.append([x, y])
        elif not self.full_figure2:
            if self.points2 == []:
                self.points2.append([x, y])
                self.canvas.create_oval(x, y, x - 1, y - 1)
            else:
                x0, y0 = self.points2[-1]
                self.canvas.create_line(x0, y0, x, y)
                self.points2.append([x, y])

    def right_button_release(self, event):
        if not self.full_figure:
            print(self.points)
            if len(self.points) > 2:
                x0, y0 = self.points[-1]
                x, y = self.points[0]
                self.canvas.create_line(x0, y0, x, y)
                self.full_figure = True

        elif not self.full_figure2:
            print(self.points2)
            if len(self.points2) > 2:
                x0, y0 = self.points2[-1]
                x, y = self.points2[0]
                self.canvas.create_line(x0, y0, x, y)
                self.full_figure2 = True

    def polygon(self):
        if not self.full_figure:
            self.canvas.delete("all")
            if self.point:
                x, y = self.point_x, self.point_y
                self.canvas.create_oval(x + 1, y + 1, x - 1, y - 1, fill="green")
            if len(self.points) == 1:
                x, y = self.points[0]
                self.canvas.create_oval(x, y, x - 1, y - 1)
            else:
                l = len(self.points)
                for i in range(0, len(self.points)):
                    x, y = self.points[i]
                    x0, y0 = self.points[(i - 1) % l]
                    self.canvas.create_line(x0, y0, x, y)

        elif not self.full_figure2:
            self.canvas.delete("all")
            if self.point2:
                x, y = self.point_x, self.point_y
                self.canvas.create_oval(x + 1, y + 1, x - 1, y - 1, fill="green")
            if len(self.points2) == 1:
                x, y = self.points2[0]
                self.canvas.create_oval(x, y, x - 1, y - 1)
            else:
                l = len(self.points2)
                for i in range(0, len(self.points2)):
                    x, y = self.points2[i]
                    x0, y0 = self.points2[(i - 1) % l]
                    self.canvas.create_line(x0, y0, x, y)

    def bridge(self, pointsL, pointsR, type):
        vl = right_point(points=pointsL)
        self.canvas.create_oval(vl[0], vl[1], vl[0] - 1, vl[1] - 1, outline="red", fill="red", width=2)

        vr = left_point(points=pointsR)
        self.canvas.create_oval(vr[0], vr[1], vr[0] - 1, vr[1] - 1, outline="red", fill="red", width=2)
        while 2 * 2 == 4:
            vr_new = find_vr(pointsR, vl, type)
            vl_new = find_vl(pointsL, vr, type)
            # self.canvas.create_line(vl_new[0],vl_new[1] , vr_new[0], vr_new[1], fill="red", width=2)
            if vr == vr_new and vl == vl_new:
                break
            vr = vr_new
            vl = vl_new
        return [vl, vr]

    def merge(self, pointsL, pointsR):
        upper_line = self.bridge(pointsL=pointsL, pointsR=pointsR, type='upper')
        lower_line = self.bridge(pointsL=pointsL, pointsR=pointsR, type='lower')
        return [upper_line, lower_line]


if __name__ == '__main__':
    Window()
