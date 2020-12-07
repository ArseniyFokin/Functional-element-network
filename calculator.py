def calculate_finish_sign(start, finish, vertex, edges):
    ans = []
    for i in finish:
        ans.append(calculate_finish_point(i, start, vertex, edges))
    return ans


def calculate_finish_point(s, start, vertex, edges):
    if len(vertex[s]) == 0:
        return None
    if vertex[s][0] == 0:
        return 0
    elif vertex[s][0] == 1:
        return 1
    elif vertex[s][0] == 3:
        return start[vertex[s][1]]
    elif vertex[s][0] == 4:
        return int(not calculate_finish_point(edges[s][0], start, vertex, edges))
    elif vertex[s][0] == 5:
        return int(calculate_finish_point(edges[s][0], start, vertex, edges)
                   or calculate_finish_point(edges[s][1], start, vertex, edges))
    elif vertex[s][0] == 6:
        return int(calculate_finish_point(edges[s][0], start, vertex, edges)
                   and calculate_finish_point(edges[s][1], start, vertex, edges))
    elif vertex[s][0] == 7:
        return calculate_finish_point(edges[s][0], start, vertex, edges)
    else:
        return None
