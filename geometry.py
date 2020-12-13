from math import *


def calculate_cursor_points(x_start, y_start, x_finish, y_finish, arrowhead_len=8, angle=40):
    x = x_finish - x_start
    y = -y_finish - (-y_start)
    norm_vec = sqrt(x * x + y * y)
    x_found = x_finish
    y_found = -y_finish

    x_new_point_first = -(x / norm_vec) * arrowhead_len
    y_new_point_first = -(y / norm_vec) * arrowhead_len
    x_new_point_second = -(x / norm_vec) * arrowhead_len
    y_new_point_second = -(y / norm_vec) * arrowhead_len

    rad_angle = angle * pi / 180

    x1_new_point_first = x_new_point_first * cos(rad_angle) - y_new_point_first * sin(rad_angle)
    y1_new_point_first = x_new_point_first * sin(rad_angle) + y_new_point_first * cos(rad_angle)

    x1_new_point_second = x_new_point_second * cos(-rad_angle) - y_new_point_second * sin(-rad_angle)
    y1_new_point_second = x_new_point_second * sin(-rad_angle) + y_new_point_second * cos(-rad_angle)

    x1_new_point_first = x1_new_point_first + x_found
    y1_new_point_first = y1_new_point_first + y_found

    x1_new_point_second = x1_new_point_second + x_found
    y1_new_point_second = y1_new_point_second + y_found

    a = list()
    a.append(x1_new_point_first)
    a.append(-y1_new_point_first)
    a.append(x1_new_point_second)
    a.append(-y1_new_point_second)

    return a


def shift_point(x_start, y_start, x_finish, y_finish, shift_len=4):
    x = x_finish - x_start
    y = -y_finish - (-y_start)
    norm_vec = sqrt(x * x + y * y)

    x_found = x_finish
    y_found = -y_finish

    x_new_point = -(x / norm_vec) * shift_len + x_found
    y_new_point = -(y / norm_vec) * shift_len + y_found

    return [x_new_point, -y_new_point]
