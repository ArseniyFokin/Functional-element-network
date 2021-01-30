"""Модуль, содержащий в себе классы функциональных элементов"""
# from abc import abstractmethod

from win_global import *
from geometry import calculate_cursor_points, shift_point

"""
class allFE:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    @abstractmethod
    def draw(self):
        pass

    @abstractmethod
    def delete(self):
        pass
"""


class func_vertex_3:
    """Класс для функциональных элементов AND и OR"""

    def __init__(self, view: str, x: int, y: int):
        """
        :param view: Вид элемнета (AND или OR)
        :param x: Координата x центра элемента
        :param y: Координата y центра элемента
        """
        # super().__init__(x, y)
        self.x = x  # Координаты центра элемента
        self.y = y
        self.in1_x = x - 15  # Координаты левого входа
        self.in1_y = y - 15
        self.in2_x = x + 15  # Координаты правого входа
        self.in2_y = y - 15
        self.out_x = x  # Координаты выхода
        self.out_y = y + 15
        self.view = view  # Вид элемнета (AND или OR)
        self.fill = "green" if view == "AND" else "red"  # Цвет границы
        self.check_in1 = False  # Проверка левого входа
        self.check_in2 = False  # Провекра правого входа
        self.line = None  # Ломанная линия, граница
        self.oval0 = None  # Левый вход
        self.oval1 = None  # Правый вход
        self.oval2 = None  # Выход
        self.text = None  # Текст

    def draw(self):
        """Рисует ФЭ"""
        self.line = canvas.create_line(self.in1_x, self.in1_y, self.in2_x, self.in2_y, self.out_x, self.out_y,
                                       self.in1_x, self.in1_y, fill=self.fill)
        self.oval0 = canvas.create_oval(self.in1_x - 4, self.in1_y - 4, self.in1_x + 4, self.in1_y + 4, fill="black",
                                        outline="black")
        self.oval1 = canvas.create_oval(self.in2_x - 4, self.in2_y - 4, self.in2_x + 4, self.in2_y + 4, fill="black",
                                        outline="black")
        self.oval2 = canvas.create_oval(self.out_x - 4, self.out_y - 4, self.out_x + 4, self.out_y + 4, fill="black",
                                        outline="black")
        if self.view == "AND":
            self.text = canvas.create_text(self.x, self.y - 5, text="Λ")
        else:
            self.text = canvas.create_text(self.x, self.y - 5, text="v")

    def check_in(self, x, y):
        """
        Помечает вход, как занятый
        :param x: координата x
        :param y: координата y
        """
        if (x - self.in1_x) ** 2 + (y - self.in1_y) ** 2 <= 16:
            self.check_in1 = True
        elif (x - self.in2_x) ** 2 + (y - self.in2_y) ** 2 <= 16:
            self.check_in2 = True

    def select_in(self, x, y):
        """
        Возврашает координаты одно из двух входов, если (x,y) принадлежит овалу
        :param x: координата x
        :param y: координата y
        :return: координаты центра входа
        """
        if (x - self.in1_x) ** 2 + (y - self.in1_y) ** 2 <= 16:
            return self.in1_x, self.in1_y
        elif (x - self.in2_x) ** 2 + (y - self.in2_y) ** 2 <= 16:
            return self.in2_x, self.in2_y

    def in_False(self, x, y):
        """
        Помечает вход, как свободный
        :param x: координата x
        :param y: координата y
        """
        if (x - self.in1_x) ** 2 + (y - self.in1_y) ** 2 <= 16:
            self.check_in1 = False
        elif (x - self.in2_x) ** 2 + (y - self.in2_y) ** 2 <= 16:
            self.check_in2 = False

    def delete(self):
        """Удаляет ФЭ"""
        canvas.delete(self.line)
        canvas.delete(self.oval0)
        canvas.delete(self.oval1)
        canvas.delete(self.oval2)
        canvas.delete(self.text)


class func_edge:
    """Класс для рёбер СФЭ"""

    def __init__(self, in_x, in_y, out_x, out_y, class1, class2):
        """
        :param in_x: Координата x входа
        :param in_y: Координата y входа
        :param out_x: Координата x выхода
        :param out_y: Координата y выхода
        :param class1: ФЭ входа
        :param class2: ФЭ выхода
        """
        self.in_x = in_x
        self.in_y = in_y
        self.out_x = out_x
        self.out_y = out_y
        self.class1 = class1
        self.class2 = class2
        self.line = None  # Соединяющая линия
        self.line1 = None  # Стрелка
        self.line2 = None  # Стрелка

    def draw(self, x, y):
        """
        Рисует стрелку
        :param x: координата x
        :param y: координата y
        """
        x_new, y_new = shift_point(self.out_x, self.out_y, x, y)
        self.line = canvas.create_line(x_new, y_new, self.out_x, self.out_y)
        x1, y1, x2, y2 = calculate_cursor_points(self.out_x, self.out_y, x_new, y_new)
        self.line1 = canvas.create_line(x_new, y_new, x1, y1, width=2)
        self.line2 = canvas.create_line(x_new, y_new, x2, y2, width=2)

    def delete(self):
        """Удаляет стрелку"""
        canvas.delete(self.line)
        canvas.delete(self.line1)
        canvas.delete(self.line2)


class Start_vertex:
    """Класс для функциональных элементов START"""

    def __init__(self, x, y, value, text):
        """
        :param x: Координата x центра элемента
        :param y: Координата y центра элемента
        :param value: Значение вершины (1, 0, ?)
        :param text: Текст на вершине (1, 0, Si)
        i - номер в массиве стартовых вершин
        """
        self.x = x
        self.y = y
        self.out_x = x  # Координаты выхода
        self.out_y = y + 15
        self.value = value
        self.oval = None  # Граница ФЭ, тело
        self.oval1 = None  # Выход
        self.text = text

    def paint(self):
        """Рисует ФЭ"""
        self.oval = canvas.create_oval(self.x - 15, self.y - 15, self.x + 15, self.y + 15)
        self.oval1 = canvas.create_oval(self.x - 4, self.y + 15 - 4, self.x + 4, self.y + 15 + 4, fill="black",
                                        outline="black")
        if self.value == "Start":
            self.text = canvas.create_text(self.x, self.y, text="S" + self.text)
        else:
            self.text = canvas.create_text(self.x, self.y, text=self.value)

    def delete(self):
        """Удаляет ФЭ"""
        canvas.delete(self.oval)
        canvas.delete(self.oval1)
        canvas.delete(self.text)

    def rename(self, ind):
        """Переименовывает ФЭ"""
        if self.value != "0" and self.value != "1":
            canvas.delete(self.text)
            self.text = canvas.create_text(self.x, self.y, text="S" + str(ind))


class Finish_vertex:
    """Класс для функциональных элементов FINISH"""

    def __init__(self, x, y, text):
        """
        :param x: Координата x центра элемента
        :param y: Координата y центра элемента
        :param text: Текст (Fi)
        i - номер в массиве финальных вершин
        """
        self.x = x
        self.y = y
        self.in_x = x  # Коордирнаты входа
        self.in_y = y - 15
        self.check = False  # Проверка входа
        self.oval = None  # Граница ФЭ
        self.oval1 = None  # Вход
        self.text = text

    def paint(self):
        """Рисует ФЭ"""
        self.oval = canvas.create_oval(self.x - 15, self.y - 15, self.x + 15, self.y + 15)
        self.oval1 = canvas.create_oval(self.x - 4, self.y - 15 - 4, self.x + 4, self.y - 15 + 4, fill="black",
                                        outline="black")
        self.text = canvas.create_text(self.x, self.y, text="F" + self.text)

    def delete(self):
        """Удаляет ФЭ"""
        canvas.delete(self.oval)
        canvas.delete(self.oval1)
        canvas.delete(self.text)

    def rename(self, ind):
        """Переименовывает ФЭ"""
        canvas.delete(self.text)
        self.text = canvas.create_text(self.x, self.y, text="F" + str(ind))


class NO_vertex:
    """Класс для функциональных элементов NO"""

    def __init__(self, x, y):
        """
        :param x: Координата x центра элемента
        :param y: Координата y центра элемента
        """
        self.x = x
        self.y = y
        self.in_x = x  # Координаты входа
        self.in_y = y - 15
        self.out_x = x  # Координаты выхода
        self.out_y = y + 15
        self.check = False  # Проверка входа
        self.line = None  # Ломнаая линия, граница
        self.oval = None  # Вход
        self.oval1 = None  # Выход
        self.text = None

    def paint(self):
        """Рисует ФЭ"""
        self.line = canvas.create_line(self.x - 15, self.y - 15, self.x + 15, self.y - 15, self.x, self.y + 15,
                                       self.x - 15,
                                       self.y - 15)
        self.oval = canvas.create_oval(self.x - 4, self.y - 15 - 4, self.x + 4, self.y - 15 + 4, fill="black",
                                       outline="black")
        self.oval1 = canvas.create_oval(self.x - 4, self.y + 15 - 4, self.x + 4, self.y + 15 + 4, fill="black",
                                        outline="black")
        self.text = canvas.create_text(self.x, self.y - 10, text="__")

    def delete(self):
        """Удаляет ФЭ"""
        canvas.delete(self.line)
        canvas.delete(self.oval)
        canvas.delete(self.oval1)
        canvas.delete(self.text)
