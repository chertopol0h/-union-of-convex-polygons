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
from shapely.geometry import LineString, Point as ShapelyPoint, Polygon as ShapelyPolygon
from math import *
import time


def rotate(a, b, c):
    """
    Векторное произведение (AB x AC)
    >0 - слева, <0 - справа, =0 - на линии
    """
    return (b[0]-a[0])*(c[1]-b[1]) - (b[1]-a[1])*(c[0]-b[0])


def line_intersection(line1, line2):
    """Найти точку пересечения двух отрезков"""
    p1, p2 = line1
    p3, p4 = line2
    
    line1_shapely = LineString([p1, p2])
    line2_shapely = LineString([p3, p4])
    
    if not line1_shapely.intersects(line2_shapely):
        return None
        
    intersection = line1_shapely.intersection(line2_shapely)
    if intersection.geom_type == 'Point':
        return [intersection.x, intersection.y]
    return None


def graham_scan(points):
    """Алгоритм Грэхема для построения выпуклой оболочки"""
    if len(points) < 3:
        return points
    
    # Находим самую нижнюю левую точку
    start = min(points, key=lambda p: (p.y, p.x))
    
    # Сортируем точки по полярному углу
    def polar_angle(p):
        return atan2(p.y - start.y, p.x - start.x)
    
    sorted_points = sorted(points, key=polar_angle)
    
    # Строим выпуклую оболочку
    hull = [start, sorted_points[0]]
    
    for i in range(1, len(sorted_points)):
        while len(hull) > 1 and rotate(hull[-2], hull[-1], sorted_points[i]) <= 0:
            hull.pop()
        hull.append(sorted_points[i])
    
    return hull


class PolygonPoint:
    """Точка полигона с информацией о принадлежности"""
    def __init__(self, x, y, polygon_id, point_id=None):
        self.x = x
        self.y = y
        self.polygon_id = polygon_id  # 1 или 2
        self.point_id = point_id
        self.is_intersection = False
        
    def __eq__(self, other):
        if not isinstance(other, PolygonPoint):
            return False
        return (abs(self.x - other.x) < 1e-10 and 
                abs(self.y - other.y) < 1e-10)
                
    def __hash__(self):
        return hash((round(self.x, 6), round(self.y, 6)))
        
    def __repr__(self):
        poly_str = "intersection" if self.is_intersection else f"poly{self.polygon_id}"
        return f"Point({self.x}, {self.y}, {poly_str})"


class Window:
    def __init__(self, size=500, fill=False):
        self.size = size
        self.fill = fill
        self.window = Tk()
        self.full_figure = False
        self.full_figure2 = False
        
        self.polygon1 = []
        self.polygon2 = []
        self.final_points = []
        
        self.window.title("Объединение выпуклых полигонов")
        self.window.resizable(False, False)
        
        self.points = []
        self.points2 = []
        
        self.canvas = Canvas(self.window, width=self.size, height=self.size, background='white')
        self.canvas.grid(row=0, column=0)
        
        self.canvas.bind("<ButtonRelease-1>", self.left_button_release)
        self.canvas.bind("<ButtonRelease-2>", self.right_button_release)

        self.clear_button = Button(self.window, text='Clear', command=self.clear_window)
        self.clear_button.grid(row=2, column=3)

        self.go_button = Button(self.window, text='Go', command=self.start_algorithm)
        self.go_button.grid(row=1, column=3)

        self.window.mainloop()

    def clear_window(self):
        self.canvas.delete("all")
        self.full_figure = False
        self.full_figure2 = False
        self.points = []
        self.points2 = []
        self.polygon1 = []
        self.polygon2 = []
        self.final_points = []

    def fill_polygon(self):
        if self.final_points:
            points_flat = []
            for p in self.final_points:
                points_flat.extend([p.x, p.y])
            self.canvas.create_polygon(points_flat, fill="sky blue", outline="green", width=2)

    def start_algorithm(self):
        self.union()
        if self.fill:
            self.fill_polygon()

    def left_button_release(self, event):
        x, y = event.x, event.y
        if not self.full_figure:
            if not self.points:
                self.points.append([x, y])
                self.polygon1.append(PolygonPoint(x, y, 1, len(self.polygon1)))
                self.canvas.create_oval(x-2, y-2, x+2, y+2, fill='blue')
            else:
                x0, y0 = self.points[-1]
                self.canvas.create_line(x0, y0, x, y, width=2, fill='blue')
                self.points.append([x, y])
                self.polygon1.append(PolygonPoint(x, y, 1, len(self.polygon1)))

        elif not self.full_figure2:
            if not self.points2:
                self.points2.append([x, y])
                self.polygon2.append(PolygonPoint(x, y, 2, len(self.polygon2)))
                self.canvas.create_oval(x-2, y-2, x+2, y+2, fill='red')
            else:
                x0, y0 = self.points2[-1]
                self.canvas.create_line(x0, y0, x, y, width=2, fill='red')
                self.points2.append([x, y])
                self.polygon2.append(PolygonPoint(x, y, 2, len(self.polygon2)))

    def right_button_release(self, event):
        if not self.full_figure and len(self.points) > 2:
            x0, y0 = self.points[-1]
            x, y = self.points[0]
            self.canvas.create_line(x0, y0, x, y, width=2, fill='blue')
            self.full_figure = True
            print("Полигон 1 завершен")

        elif not self.full_figure2 and len(self.points2) > 2:
            x0, y0 = self.points2[-1]
            x, y = self.points2[0]
            self.canvas.create_line(x0, y0, x, y, width=2, fill='red')
            self.full_figure2 = True
            print("Полигон 2 завершен")

    def find_all_intersections(self):
        """Найти все точки пересечения между полигонами"""
        intersections = []
        
        for i in range(len(self.polygon1)):
            p1 = self.polygon1[i]
            p2 = self.polygon1[(i + 1) % len(self.polygon1)]
            
            for j in range(len(self.polygon2)):
                p3 = self.polygon2[j]
                p4 = self.polygon2[(j + 1) % len(self.polygon2)]
                
                line1 = ([p1.x, p1.y], [p2.x, p2.y])
                line2 = ([p3.x, p3.y], [p4.x, p4.y])
                
                intersect = line_intersection(line1, line2)
                if intersect:
                    intersection_point = PolygonPoint(intersect[0], intersect[1], 0)
                    intersection_point.is_intersection = True
                    intersection_point.edge1 = (p1, p2)
                    intersection_point.edge2 = (p3, p4)
                    intersections.append(intersection_point)
                    
        return intersections

    def point_in_polygon(self, point, polygon):
        """Проверить, находится ли точка внутри полигона"""
        x, y = point.x, point.y
        n = len(polygon)
        inside = False
        
        p1 = polygon[0]
        for i in range(1, n + 1):
            p2 = polygon[i % n]
            if y > min(p1.y, p2.y):
                if y <= max(p1.y, p2.y):
                    if x <= max(p1.x, p2.x):
                        if p1.y != p2.y:
                            xinters = (y - p1.y) * (p2.x - p1.x) / (p2.y - p1.y) + p1.x
                        if p1.x == p2.x or x <= xinters:
                            inside = not inside
            p1 = p2
            
        return inside

    def polygon_contains_polygon(self, poly1, poly2):
        """Проверить, содержит ли poly1 poly2"""
        # Если все точки poly2 внутри poly1, то poly1 содержит poly2
        for point in poly2:
            if not self.point_in_polygon(point, poly1):
                return False
        return True

    def merge_convex_hull(self, points1, points2):
        """Объединить две выпуклые оболочки"""
        # Простой подход: объединяем все точки и строим выпуклую оболочку
        all_points = points1 + points2
        
        # Убираем дубликаты
        unique_points = []
        seen = set()
        for p in all_points:
            key = (round(p.x, 2), round(p.y, 2))
            if key not in seen:
                seen.add(key)
                unique_points.append(p)
        
        # Строим выпуклую оболочку
        if len(unique_points) < 3:
            return unique_points
            
        return graham_scan(unique_points)

    def union(self):
        """Улучшенный алгоритм объединения выпуклых полигонов"""
        print("Начало алгоритма объединения")
        self.final_points = []
        
        if not self.polygon1 or not self.polygon2:
            return
            
        # Находим все пересечения
        intersections = self.find_all_intersections()
        print(f"Найдено пересечений: {len(intersections)}")
        
        # Проверяем особые случаи
        poly1_contains_poly2 = self.polygon_contains_polygon(self.polygon1, self.polygon2)
        poly2_contains_poly1 = self.polygon_contains_polygon(self.polygon2, self.polygon1)
        
        if poly1_contains_poly2:
            print("Полигон 1 содержит полигон 2")
            self.final_points = self.polygon1
        elif poly2_contains_poly1:
            print("Полигон 2 содержит полигон 1")
            self.final_points = self.polygon2
        elif not intersections:
            print("Полигоны не пересекаются - строим выпуклую оболочку")
            # Для непересекающихся строим выпуклую оболочку всех точек
            self.final_points = self.merge_convex_hull(self.polygon1, self.polygon2)
        else:
            print("Полигоны пересекаются - строим объединение")
            # Для пересекающихся используем предыдущий алгоритм
            all_points = []
            
            # Добавляем точки пересечения
            for inter in intersections:
                all_points.append(inter)
                
            # Добавляем вершины полигонов, которые находятся снаружи другого полигона
            for point in self.polygon1:
                if not self.point_in_polygon(point, self.polygon2):
                    all_points.append(point)
                    
            for point in self.polygon2:
                if not self.point_in_polygon(point, self.polygon1):
                    all_points.append(point)
            
            # Сортируем точки по углу относительно центра
            if all_points:
                center_x = sum(p.x for p in all_points) / len(all_points)
                center_y = sum(p.y for p in all_points) / len(all_points)
                
                def angle_from_center(point):
                    return atan2(point.y - center_y, point.x - center_x)
                    
                all_points.sort(key=angle_from_center)
                
                self.final_points = all_points
        
        self.visualize_result()

    def visualize_result(self):
        """Визуализировать результат"""
        print("Визуализация результата:")
        
        # Очищаем старую визуализацию
        self.canvas.delete("all")
        
        # Рисуем исходные полигоны полупрозрачными
        if self.polygon1:
            points1 = [[p.x, p.y] for p in self.polygon1]
            for i in range(len(points1)):
                p1 = points1[i]
                p2 = points1[(i + 1) % len(points1)]
                self.canvas.create_line(p1[0], p1[1], p2[0], p2[1], width=1, fill='lightblue', dash=(2, 2))
        
        if self.polygon2:
            points2 = [[p.x, p.y] for p in self.polygon2]
            for i in range(len(points2)):
                p1 = points2[i]
                p2 = points2[(i + 1) % len(points2)]
                self.canvas.create_line(p1[0], p1[1], p2[0], p2[1], width=1, fill='lightcoral', dash=(2, 2))
        
        # Рисуем объединенный полигон
        if len(self.final_points) > 1:
            # Сначала рисуем все точки
            for i, point in enumerate(self.final_points):
                color = 'orange' if point.is_intersection else 'green'
                self.canvas.create_oval(point.x-4, point.y-4, point.x+4, point.y+4, 
                                      fill=color, outline=color)
                self.canvas.create_text(point.x, point.y-10, text=str(i), fill='black')
            
            # Затем рисуем линии с анимацией
            for i in range(len(self.final_points)):
                p1 = self.final_points[i]
                p2 = self.final_points[(i + 1) % len(self.final_points)]
                
                # Рисуем линию
                self.canvas.create_line(p1.x, p1.y, p2.x, p2.y, width=3, fill='green')
                
                print(f"{i} - {p1}")
                self.canvas.update()
                time.sleep(0.3)
        
        print(f"Всего точек в объединении: {len(self.final_points)}")


if __name__ == '__main__':
    Window(size=700, fill=False)