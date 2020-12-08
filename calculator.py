MAX_depth = 1000000
cur_depth = 0


def calculate_finish_sign(start, finish, vertex, edges):
    global cur_depth
    ans = []
    f = None
    for i in finish:
        cur_depth = 0
        try:
            f = calculate_finish_point(i, start, vertex, edges)
        except:
            f = None
        ans.append(f)
    return ans


def calculate_finish_point(s, start, vertex, edges):
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
        return int(not calculate_finish_point(edges[s][0], start, vertex, edges))
    elif vertex[s][0] == 5:
        cur_depth = cur_depth + 1
        return int(calculate_finish_point(edges[s][0], start, vertex, edges)
                   or calculate_finish_point(edges[s][1], start, vertex, edges))
    elif vertex[s][0] == 6:
        cur_depth = cur_depth + 1
        return int(calculate_finish_point(edges[s][0], start, vertex, edges)
                   and calculate_finish_point(edges[s][1], start, vertex, edges))
    elif vertex[s][0] == 7:
        cur_depth = cur_depth + 1
        return calculate_finish_point(edges[s][0], start, vertex, edges)
    else:
        return None
