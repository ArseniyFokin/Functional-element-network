"""Модуль с функциями для геометрических построений в координатах Tkinter"""
import math


def calculate_cursor_points(x_start, y_start, x_finish, y_finish, arrowhead_len=8, angle=40):
    """рассчитывает координаты крыльев курсора в координатах Tkinter

    :param x_start: x координта точки из которой начинается стрелка
    :param y_start: y координта точки из которой начинается стрелка
    :param x_finish: x координта точки в которой заканчивается стрелка
    :param y_finish: y координта точки в которой заканчивается стрелка
    :param arrowhead_len: длина крыла курсора
    :param angle: угол на который крыло курсора отстает от линии стрелки
    :return: координаты 2х точек, в которых заканчиваются крылья курсора(выходя из (x_finish, y_finish))
    """
    # получим вектор (x, y) направления из (x_start, y_start) в (x_finish, y_finish)
    # вместо координаты y используем -y, для перехода из координат Tkinter в Декартовы
    # т.е. работаем с зеркальным отражением точки относительно OX
    x = x_finish - x_start
    y = -y_finish - (-y_start)

    norm_vec = math.sqrt(x * x + y * y)

    x_found = x_finish
    y_found = -y_finish

    # получим вектор направления из (x_finish, y_finish) в (x_start, y_start) длины arrowhead_len
    x_main_vec = -(x / norm_vec) * arrowhead_len
    y_main_vec = -(y / norm_vec) * arrowhead_len

    rad_angle = angle * math.pi / 180

    # получим векторы крыльев курсора сдвигом вектора (x_main_vec, y_main_vec) на заданный угол в обоих направлениях
    x_vec_first = x_main_vec * math.cos(rad_angle) - y_main_vec * math.sin(rad_angle)
    y_vec_first = x_main_vec * math.sin(rad_angle) + y_main_vec * math.cos(rad_angle)
    x_vec_second = x_main_vec * math.cos(-rad_angle) - y_main_vec * math.sin(-rad_angle)
    y_vec_second = x_main_vec * math.sin(-rad_angle) + y_main_vec * math.cos(-rad_angle)

    # получим искомые точки в Декартовых координатах
    x_new_point_first = x_vec_first + x_found
    y_new_point_first = y_vec_first + y_found
    x_new_point_second = x_vec_second + x_found
    y_new_point_second = y_vec_second + y_found

    # вернемся к точкам в координатах Tkinter обратно отразив их относительно OX (y = -y)
    return [x_new_point_first, -y_new_point_first, x_new_point_second, -y_new_point_second]


def shift_point(x_start, y_start, x_finish, y_finish, shift_len=4):
    """возвращает координаты точки, полученной сдвигом точки (x_start, y_start) в направлении точки (x_finish, y_finish) на длину shift_len в координатах Tkinter"""
    # получим вектор (x, y) направления из (x_start, y_start) в (x_finish, y_finish)
    # вместо координаты y используем -y, для перехода из координат Tkinter в Декартовы
    # т.е. работаем с зеркальным отражением точки относительно OX
    x = x_finish - x_start
    y = -y_finish - (-y_start)

    norm_vec = math.sqrt(x * x + y * y)

    x_found = x_start
    y_found = -y_start

    x_new_point = (x / norm_vec) * shift_len + x_found
    y_new_point = (y / norm_vec) * shift_len + y_found

    # вернемся к точкам в координатах Tkinter обратно отразив их относительно OX (y = -y)
    return [x_new_point, -y_new_point]
