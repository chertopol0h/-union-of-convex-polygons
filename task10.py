"""
Николаенко Михаил Владимирович 4.4

10. Объединение выпуклых полигонов

ПРИМЕЧАНИЕ:
Два полигона задаются по отдельности. По нажатию на левую кнопку мыши ставятся вершины полигона, текущая точка
соединяется линией с предыдущей автоматически, чтобы соединить первую точку с последней, нажмите на правую кнопку мыши.
Затем приступайте к заданию второго полигона.
ВЕРШИНЫ В ПОЛИГОНЕ ЗАДАВАТЬ ПО ЧАСОВОЙ СТРЕЛКЕ.
"""

from tkinter import *
from shapely.geometry import LineString
from math import *
import time


def rotate(line_from, line_to, point):
    """
    Функция определяет, с какой стороны от вектора находится точка

    :param line_from: Первая точка отрезка
    :param line_to: Вторая точка отрезка
    :param point: Координаты точки
    :return: положительное возвращаемое значение соответствует левой стороне, отрицательное — правой, 0 - принадлежит
    """
    return (line_to[0] - line_from[0]) * (point[1] - line_to[1]) - (line_to[1] - line_from[1]) * (point[0] - line_to[0])


def intersection(p1, p2, p3, p4):
    """
    Пересечение отрезков

    :param p1: Первая точка первого отрезка
    :param p2: Вторая точка первого отрезка
    :param p3: Первая точка второго отрезка
    :param p4: Вторая точка второго отрезка
    :return: точка пересечения
    """
    line1 = LineString([(p1[0], p1[1]), (p2[0], p2[1])])
    line2 = LineString([(p3[0], p3[1]), (p4[0], p4[1])])
    if line1.intersection(line2).is_empty:
        return []
    else:
        return [line1.intersection(line2).x, line1.intersection(line2).y]


def findside(p1, p2, x, y):
    """
    Определение положения точки относительно ребра

    :param p1: первая точка ребра
    :param p2: вторая точка ребра
    :param x: координата X
    :param y: координата X
    :return:    Если True, то точка СПРАВА от ребра.
                Если False, то точка СЛЕВА от ребра.
    """
    xa = p2[0] - p1[0]
    ya = p2[1] - p1[1]
    x -= p1[0]
    y -= p1[1]
    if y*xa - x*ya > 0:
        return True     # right
    else:
        return False    # left


def find_leftest_point(cur_polygon):
    """
    Поиск точки с самым маленьким X с самым большим Y. То есть находится самая левая и верхняя точка.

    :param cur_polygon: полигон, заданный списком Point'ов
    :return: самая левая верхняя точка
    """
    leftest_point = Point(x=1000000, y=-1000000, next=None, prev=None)
    for point in cur_polygon:
        if point.x < leftest_point.x:
            leftest_point = point
        elif point.x == leftest_point.x:
            if point.y > leftest_point.y:
                leftest_point = point
    return leftest_point


class Point:
    """
    Класс вершины полигона с ссылками на следующую и предыдущую вершины.
    """
    def __init__(self, x, y, next=None, prev=None):
        self.x = x
        self.y = y
        self.next = next
        self.prev = prev

    def print(self):
        print(self.x, self.y, self.next, self.prev)


class Window:
    def __init__(self, size=500, fill=False):
        # Размер окна
        self.size = size
        # Флаг заливки объединённых полигонов
        self.fill = fill
        self.window = Tk()
        self.full_figure = False
        self.full_figure2 = False
        self.point = False
        self.point2 = False
        self.point_x = 0
        self.point_y = 0
        # список Point'ов
        self.polygon1 = list()
        self.polygon2 = list()
        self.final_points = list()
        self.window.title("what?")
        self.window.resizable(False, False)
        # current figure
        self.points = list()
        # current figure 2
        self.points2 = list()
        # canvas
        self.canvas = Canvas(self.window, width=self.size, height=self.size, background='white')
        self.canvas.grid(row=0, column=0)
        # mouse clicks
        self.canvas.bind("<ButtonRelease-1>", self.left_button_release)
        self.canvas.bind("<ButtonRelease-2>", self.right_button_release)

        # clear button
        self.clear_button = Button(self.window, text='Clear', command=self.clear_window)
        self.clear_button.grid(row=2, column=3)

        # go button
        self.go_button = Button(self.window, text='Go', command=self.start_algorithm)
        self.go_button.grid(row=1, column=3)

        self.window.mainloop()

    def clear_window(self):
        """
        Отчистка окна.
        """
        self.canvas.delete("all")
        self.full_figure = False
        self.full_figure2 = False
        self.points = list()
        self.points2 = list()
        self.polygon1 = list()
        self.polygon2 = list()
        self.final_points = list()

    def fill_polygon(self):
        """
        Заливка объединённых полигонов.
        """
        self.canvas.create_polygon(self.final_points, fill="sky blue")

    def start_algorithm(self):
        self.union()
        if self.fill:
            self.fill_polygon()

    def left_button_release(self, event):
        x, y = event.x, event.y
        point = Point(x, y, None, None)
        if not self.full_figure:
            if self.points == [] and self.polygon1 == []:
                self.points.append([x, y])
                self.polygon1.append(point)
                self.canvas.create_oval(x, y, x - 1, y - 1)
            else:
                x0, y0 = self.points[-1]
                self.canvas.create_line(x0, y0, x, y, width=2)
                self.points.append([x, y])
                point = Point(x, y, None, self.polygon1[-1])
                self.polygon1[-1].next = point
                self.polygon1.append(point)

        elif not self.full_figure2:
            if self.points2 == [] and self.polygon2 == []:
                self.points2.append([x, y])
                self.polygon2.append(point)
                self.canvas.create_oval(x, y, x - 1, y - 1)
            else:
                x0, y0 = self.points2[-1]
                self.canvas.create_line(x0, y0, x, y, width=2)
                self.points2.append([x, y])
                point = Point(x, y, None, self.polygon2[-1])
                self.polygon2[-1].next = point
                self.polygon2.append(point)

    def right_button_release(self, event):
        if not self.full_figure:
            print(self.points)
            if len(self.points) > 2 and len(self.polygon1) > 2:
                x0, y0 = self.points[-1]
                x, y = self.points[0]
                self.polygon1[-1].next = self.polygon1[0]
                self.polygon1[0].prev = self.polygon1[-1]
                self.canvas.create_line(x0, y0, x, y, width=2)
                self.full_figure = True
                for point in self.polygon1:
                    point.print()
                print()

        elif not self.full_figure2:
            print(self.points2)
            if len(self.points2) > 2 and len(self.polygon2) > 2:
                x0, y0 = self.points2[-1]
                x, y = self.points2[0]
                self.polygon2[-1].next = self.polygon2[0]
                self.polygon2[0].prev = self.polygon2[-1]
                self.canvas.create_line(x0, y0, x, y, width=2)
                self.full_figure2 = True
                for point in self.polygon2:
                    point.print()
                print()

    def union(self):
        """
        Реализация алгоритма "объединение выпуклых полигонов".

        :return: в self.final_polygon записываются координаты всех точек объединённых полигонов
        """

        left1 = find_leftest_point(self.polygon1)
        left2 = find_leftest_point(self.polygon2)
        if left1.x < left2.x:
            # текущий полигон
            cur_polygon = self.polygon1
            # другой полигон
            other_polygon = self.polygon2
        else:
            # текущий полигон
            cur_polygon = self.polygon2
            # другой полигон
            other_polygon = self.polygon1

        # текущая точка
        cur_point = Point(x=0, y=0, next=None, prev=None)
        start_point = find_leftest_point(cur_polygon)

        # Список использованных точек
        used = list()
        # Чтобы пройти первую итерацию цикла. Ничего лучше не придумал :)
        start = False
        # Счётчик найденных точек для нового полигона
        i = 0
        # Количество итераций цикла. Необходимо для аварийного выхода в случае зацикливания
        steps = 0
        while start_point.x != cur_point.x:
            # Если зациклились, выходим
            if steps > len(self.polygon1) + len(self.polygon2) + 1:
                break
            steps += 1
            # обработка первой итерации цикла
            if not start:
                # текущая рабочая точка, самая левая и самая верхняя
                cur_point = find_leftest_point(cur_polygon)
                # следующая точка после текущей
                next_point = cur_point.next
                start = True
            # ребро от cur_point до next_point
            line = [[cur_point.x, cur_point.y], [next_point.x, next_point.y]]
            # добавляем первую точку ребра в финальный список
            if line[0] not in used:
                self.final_points.append(line[0])
                used.append(line[0])
                print(str(i), ' - точка: ', line[0])
                i += 1
                self.canvas.create_oval(line[0][0] + 1, line[0][1] + 1, line[0][0] - 1, line[0][1] - 1,
                                        outline="red", fill="red", width=3)
                if len(self.final_points) > 1:
                    self.canvas.create_line(self.final_points[-2][0], self.final_points[-2][1],
                                            self.final_points[-1][0], self.final_points[-1][1],
                                            fill="green", width=2)
                    time.sleep(1)
                self.canvas.update()

            # текущая точка в другом полигоне
            other_point = find_leftest_point(other_polygon)
            # следующая точка в другом полигоне
            other_next_point = other_point.next
            j = 0
            # хранит все пересечиения для данного ребра
            intersections = list()
            while j < len(other_polygon):
                # текущее ребро в другом полигоне
                other_line = [[other_point.x, other_point.y], [other_next_point.x, other_next_point.y]]
                # точка пересечения рёбер
                point_of_intersection = intersection(line[0], line[1], other_line[0], other_line[1])
                if point_of_intersection:
                    lst = [other_line, point_of_intersection]
                    # добавляем в список точек пересечения лист: [[ребро], точка пересечения]
                    intersections.append(lst)

                # переход к следующей точке
                other_point = other_next_point
                other_next_point = other_point.next
                j += 1
            # если нет пересечений, переход к следующему ребру в текущем полигоне
            if not intersections:
                cur_point = next_point
                next_point = cur_point.next
                continue

            # Находим из всех точек пересечения самую ближайшую к первой точке текущего ребра
            great_intersection = None
            min_x = 10000000
            for line_and_point in intersections:
                modul = abs(line[0][0] - line_and_point[1][0])
                if modul < min_x:
                    min_x = modul
                    great_intersection = line_and_point

            # ндобавляем найденную точку пересечения в финальный список
            if great_intersection[1] not in used:
                self.final_points.append(great_intersection[1])
                used.append(great_intersection[1])
                print(str(i), ' - точка: ', great_intersection[1])
                i += 1
                self.canvas.create_oval(great_intersection[1][0] + 1, great_intersection[1][1] + 1,
                                        great_intersection[1][0] - 1, great_intersection[1][1] - 1,
                                        outline="red", fill="red", width=3)
                self.canvas.create_line(self.final_points[-2][0], self.final_points[-2][1],
                                        self.final_points[-1][0], self.final_points[-1][1],
                                        fill="green", width=2)
                time.sleep(1)
                self.canvas.update()
            else:
                continue

            # находим точку из другого ребра слева от текущего ребра и добавляем эту точку в финальный список
            for point_in_line in great_intersection[0]:
                # если False, то точка слева от ребра
                if not findside(line[0], line[1], point_in_line[0], point_in_line[1]):
                    if point_in_line not in used:
                        self.final_points.append(point_in_line)
                        used.append(point_in_line)
                        print(str(i), ' - точка: ', point_in_line)
                        i += 1
                        self.canvas.create_oval(point_in_line[0] + 1, point_in_line[1] + 1,
                                                point_in_line[0] - 1, point_in_line[1] - 1,
                                                outline="red", fill="red", width=3)
                        self.canvas.create_line(self.final_points[-2][0], self.final_points[-2][1],
                                                self.final_points[-1][0], self.final_points[-1][1],
                                                fill="green", width=2)
                        time.sleep(1)
                        self.canvas.update()
                    else:
                        other_point = other_next_point
                        other_next_point = other_point.next
                        j += 1
                        continue
                    for point in other_polygon:
                        if point.x == point_in_line[0] and point.y == point_in_line[1]:
                            cur_point = point
                    next_point = cur_point.next
                    cur_polygon, other_polygon = other_polygon, cur_polygon

        self.canvas.create_line(self.final_points[-1][0], self.final_points[-1][1],
                                self.final_points[0][0], self.final_points[0][1],
                                fill="green", width=2)
        self.canvas.update()
        print('=====================================================\n'
              'END\n'
              '=====================================================\n')


if __name__ == '__main__':
    Window(size=700, fill=False)
