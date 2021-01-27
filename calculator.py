"""Модуль с функциями для проверки СФЭ на корректность и вычислений значений ее выходов"""

MAX_depth = 10000
cur_depth = 0


def calculate_finish_sign(start, finish, vertex, edges):
    """Ищет значения финальных состояний СФЭ

    :param start: список значений на входе в СФЭ
    :param finish: список финальных состояний(их номера в vertex), которые надо посчитать
    :param vertex: список вершин, для каждой вершины хранится ее тип:
        (0, 0): константный вход со значением 0
        (1, 1): константный вход со значением 1
        (2, 2): зарезервировано под функциональные блоки
        (3, n): стартовая вершина, где n - это номер этой стартовой вершины в start
        (4, 4): транзистор NOT
        (5, 5): транзистор OR
        (6, 6): транзистор AND
        (7, 7): финальное состояние(выход) СФЭ
    :param edges: список всех обратных ребер графа СФЭ, в ячейке с номером <номер вершины в списке vertex> лежат номера(из vertex) в которые из нее можно попасть по обратному ребру
    :return: список значений выходов СФЭ
    """
    global cur_depth
    ans = []
    vertex_sign = [-1]*len(vertex)
    f = None
    for i in finish:
        cur_depth = 0
        try:
            f = calculate_finish_point(i, start, vertex, edges, vertex_sign)
        except:
            f = None
        ans.append(f)
    return ans


def calculate_finish_point(s, start, vertex, edges, vertex_sign):
    """ищет значение переданного выхода СФЭ

    :param s: выход СФЭ, значение которого надо посчитать
    :param start: список значений на входе в СФЭ
    :param vertex: список вершин, для каждой вершины хранится ее тип:
        (0, 0): константный вход со значением 0
        (1, 1): константный вход со значением 1
        (2, 2): зарезервировано под функциональные блоки
        (3, n): стартовая вершина, где n - это номер этой стартовой вершины в start
        (4, 4): транзистор NOT
        (5, 5): транзистор OR
        (6, 6): транзистор AND
        (7, 7): финальное состояние(выход) СФЭ
    :param edges: список всех обратных ребер графа СФЭ, в ячейке с номером <номер вершины в списке vertex> лежат номера(из vertex) в которые из нее можно попасть по обратному ребру
    :param vertex_sign: список значений вершин: если вершину еще не посчитали по ее номеру(нумерация совпадает с vertex) лежит -1, если посчитать было невозможно, то None, иначе значение, которое вернет этот элемент СФЭ
    :return: возвращает значение выхода СФЭ (s), если посчитать не удалось, то вернет None или ошибку
    """
    global cur_depth, MAX_depth
    if cur_depth >= MAX_depth:
        return None
    if vertex[s][0] == 0:
        cur_depth = cur_depth + 1
        return 0
    elif vertex[s][0] == 1:
        cur_depth = cur_depth + 1
        return 1
    elif vertex[s][0] == 3:
        cur_depth = cur_depth + 1
        return start[vertex[s][1]]
    elif vertex[s][0] == 4:
        cur_depth = cur_depth + 1
        if vertex_sign[s] == -1:
            vertex_sign[s] = int(not calculate_finish_point(edges[s][0], start, vertex, edges, vertex_sign))
        return vertex_sign[s]
    elif vertex[s][0] == 5:
        cur_depth = cur_depth + 1
        if vertex_sign[s] == -1:
            vertex_sign[s] = int(calculate_finish_point(edges[s][0], start, vertex, edges, vertex_sign) or
                                 calculate_finish_point(edges[s][1], start, vertex, edges, vertex_sign))
        # проверка необходима из-за ленивой семантики в python 3 (1 or None вернет 1)
        if calculate_finish_point(edges[s][1], start, vertex, edges, vertex_sign) is None:
            vertex_sign[s] = None
        return vertex_sign[s]
    elif vertex[s][0] == 6:
        cur_depth = cur_depth + 1
        if vertex_sign[s] == -1:
            vertex_sign[s] = int(calculate_finish_point(edges[s][0], start, vertex, edges, vertex_sign) and
                                 calculate_finish_point(edges[s][1], start, vertex, edges, vertex_sign))
        # проверка необходима из-за ленивой семантики в python 3 (0 and None вернет 0)
        if calculate_finish_point(edges[s][1], start, vertex, edges, vertex_sign) is None:
            vertex_sign[s] = None
        return vertex_sign[s]
    elif vertex[s][0] == 7:
        cur_depth = cur_depth + 1
        return calculate_finish_point(edges[s][0], start, vertex, edges, vertex_sign)
    else:
        return None


def generate_bit_set(mask):
    """генератор всех наборов битов в порядке возрастания по битовой маске

    :param mask: битовая маска, состоящая из 1, 0 и ?. ? означает, что в данном месте могут быть и 0 и 1
    """
    size_mask = 0
    for i in mask:
        if i == '?':
            size_mask = size_mask + 1

    for i in range(2**size_mask):
        ans = ''
        cur_bit_set = bin(i)[2:]
        cur_bit_set = '0' * (size_mask - len(cur_bit_set)) + cur_bit_set
        cur = 0
        for j in mask:
            if j == '?':
                ans = ans + cur_bit_set[cur]
                cur = cur + 1
            else:
                ans = ans + j
        yield ans
