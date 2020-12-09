MAX_depth = 10000
cur_depth = 0


def calculate_finish_sign(start, finish, vertex, edges):
    global cur_depth
    ans = []
    vertex_sign = [-1]*len(vertex)
    f = None
    for i in finish:
        cur_depth = 0
        try:
            f = calculate_finish_point(i, start, vertex, edges, vertex_sign)
        except():
            f = None
        ans.append(f)
    return ans


def calculate_finish_point(s, start, vertex, edges, vertex_sign):
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
        return vertex_sign[s]
    elif vertex[s][0] == 6:
        cur_depth = cur_depth + 1
        if vertex_sign[s] == -1:
            vertex_sign[s] = int(calculate_finish_point(edges[s][0], start, vertex, edges, vertex_sign) and
                                 calculate_finish_point(edges[s][1], start, vertex, edges, vertex_sign))
        return vertex_sign[s]
    elif vertex[s][0] == 7:
        cur_depth = cur_depth + 1
        return calculate_finish_point(edges[s][0], start, vertex, edges, vertex_sign)
    else:
        return None


def generate_bit_set(mask):
    size_mask = 0
    for i in mask:
        if i == '?':
            size_mask = size_mask + 1

    for i in range(2**size_mask):
        ans = ''
        cur_bitset = bin(i)[2:]
        cur_bitset = '0' * (size_mask - len(cur_bitset)) + cur_bitset
        cur = 0
        for j in mask:
            if j == '?':
                ans = ans + cur_bitset[cur]
                cur = cur + 1
            else:
                ans = ans + j
        yield ans
