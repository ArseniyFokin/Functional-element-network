from calculator import calculate_finish_sign, generate_bit_set
from fe_classes import *
from win_global import *

FUNC_ELEMENT = None
BUFFER_X = None
BUFFER_Y = None
BUFFER_TIP = None
v = None

RED_DEL = list()
FUNCTIONAL_ELEMENT = list()
EDGE_ELEMENT = list()
START_LIST = list()
FINAL_LIST = list()
NO_ELEMENT = list()
ALL_TRANSISTOR = list()
TEMP_START = []
START = []  # Массив стартовых состояний
EDGE = []  # Массив всех рёбер
VERTEX = []  # Массив всех вершин
FINAL = []  # Массив финальных состояний

def check_vertex(x, y, flag):
    """
    Возвращает ФЭ, которой принадлежит точка (x, y)
    :param x: Координата x
    :param y: Координата y
    :param flag: Тип операции
    1 - Меняет BUFFER_TIP:
        1 - Вход AND, OR
        2 - Выход AND, OR
        3 - Выход START
        4 - Вход FINISH
        5 - Вход NO
        6 - Выход NO
    2 - Не меняет BUFFER_TIP
    :return: ФЭ
    """
    global BUFFER_TIP
    for FE in FUNCTIONAL_ELEMENT:
        if (x - FE.in1_x) ** 2 + (y - FE.in1_y) ** 2 <= 16:
            if not FE.check_in1:
                if flag == 1:
                    BUFFER_TIP = 1
                return FE
            if flag == 2:
                return FE
    for FE in FUNCTIONAL_ELEMENT:
        if (x - FE.in2_x) ** 2 + (y - FE.in2_y) ** 2 <= 16:
            if not FE.check_in2:
                if flag == 1:
                    BUFFER_TIP = 1
                return FE
            if flag == 2:
                return FE
    for FE in FUNCTIONAL_ELEMENT:
        if (x - FE.out_x) ** 2 + (y - FE.out_y) ** 2 <= 16:
            if flag == 1:
                BUFFER_TIP = 2
            return FE
    for SL in START_LIST:
        if (x - SL.out_x) ** 2 + (y - SL.out_y) ** 2 <= 16:
            if flag == 1:
                BUFFER_TIP = 3
            return SL
    for FL in FINAL_LIST:
        if (x - FL.in_x) ** 2 + (y - FL.in_y) ** 2 <= 16:
            if not FL.check:
                if flag == 1:
                    BUFFER_TIP = 4
                return FL
            if flag == 2:
                return FL
    for NOE in NO_ELEMENT:
        if (x - NOE.in_x) ** 2 + (y - NOE.in_y) ** 2 <= 16:
            if not NOE.check:
                if flag == 1:
                    BUFFER_TIP = 5
                return NOE
            if flag == 2:
                return NOE
    for NOE in NO_ELEMENT:
        if (x - NOE.out_x) ** 2 + (y - NOE.out_y) ** 2 <= 16:
            if flag == 1:
                BUFFER_TIP = 6
            return NOE
    return False


def check_edge():
    """
    Проверяет BUFFER_TIP на вход
    BUFFER_TIP == 1 - Вход AND, OR
    BUFFER_TIP == 4 - Вход FINAL
    BUFFER_TIP == 5 - Вход NO
    :return:
    True - Вход
    False - Выход
    """
    global BUFFER_TIP
    if BUFFER_TIP == 1 or BUFFER_TIP == 4 or BUFFER_TIP == 5:
        return True
    return False


def back_line():
    """Отменяет ребро"""
    global BUFFER_X, BUFFER_Y, BUFFER_TIP
    BUFFER_X = None
    BUFFER_Y = None
    BUFFER_TIP = None
    canvas.delete(v)


def paint(event):
    """Рисует ФЭ"""
    global BUFFER_X, BUFFER_Y, BUFFER_TIP, v
    bCREATE_START['state'] = DISABLED
    bCREATE.grid_remove()
    if not FUNC_ELEMENT:
        return

    # Первая точка ребра поставлена, но кнопка EDGE отжата
    elif FUNC_ELEMENT != "EDGE" and BUFFER_X is not None and BUFFER_Y is not None:
        BUFFER_X = None
        BUFFER_Y = None

    # Кнопка OR
    elif FUNC_ELEMENT == "OR":
        a = func_vertex_3("OR", event.x, event.y)
        EDGE.append([])
        ALL_TRANSISTOR.append([5, 5, a])
        FUNCTIONAL_ELEMENT.append(a)
        VERTEX.append([5, 5])
        a.draw()

    # Кнопка AND
    elif FUNC_ELEMENT == "AND":
        a = func_vertex_3("AND", event.x, event.y)
        EDGE.append([])
        ALL_TRANSISTOR.append([6, 6, a])
        FUNCTIONAL_ELEMENT.append(a)
        VERTEX.append([6, 6])
        a.draw()

    # Кнопка EDGE, первая точка
    elif FUNC_ELEMENT == "EDGE" and BUFFER_X is None and BUFFER_Y is None and BUFFER_TIP is None:
        FE = check_vertex(event.x, event.y, 1)
        if FE:
            BUFFER_X = event.x
            BUFFER_Y = event.y
            v = canvas.create_oval(50, 50, 75, 75, outline="#000000", fill="#00ff00")

    # Кнопка EDGE, вторая точка
    elif FUNC_ELEMENT == "EDGE" and BUFFER_X is not None and BUFFER_Y is not None and BUFFER_TIP is not None:
        tip = BUFFER_TIP
        class1 = check_vertex(BUFFER_X, BUFFER_Y, 1)
        if check_vertex(event.x, event.y, 0):
            class2 = check_vertex(event.x, event.y, 1)
            if BUFFER_TIP != tip and (class1.x != class2.x or class1.y != class2.y) and (
                    BUFFER_TIP != 3 or tip != 2) and (BUFFER_TIP != 2 or tip != 3) and (
                    BUFFER_TIP != 5 or tip != 1) and (BUFFER_TIP != 1 or tip != 5) and (
                    BUFFER_TIP != 1 or tip != 4) and (BUFFER_TIP != 4 or tip != 1) and (
                    BUFFER_TIP != 3 or tip != 6) and (BUFFER_TIP != 6 or tip != 3) and (
                    BUFFER_TIP != 2 or tip != 6) and (BUFFER_TIP != 6 or tip != 2) and (
                    BUFFER_TIP != 5 or tip != 4) and (BUFFER_TIP != 4 or tip != 5):
                if BUFFER_TIP == 1:
                    class2.check_in(event.x, event.y)
                elif tip == 1:
                    class1.check_in(BUFFER_X, BUFFER_Y)
                elif BUFFER_TIP == 4:
                    class2.check = True
                elif tip == 4:
                    class1.check = True
                elif BUFFER_TIP == 5:
                    class2.check = True
                elif tip == 5:
                    class1.check = True
                flag = check_edge()
                if flag:
                    a = func_edge(event.x, event.y, BUFFER_X, BUFFER_Y, class2, class1)
                else:
                    a = func_edge(BUFFER_X, BUFFER_Y, event.x, event.y, class1, class2)
                in1 = -1
                in2 = -1
                for i in range(len(ALL_TRANSISTOR)):
                    if ALL_TRANSISTOR[i][-1] == class1:
                        in1 = i
                for i in range(len(ALL_TRANSISTOR)):
                    if ALL_TRANSISTOR[i][-1] == class2:
                        in2 = i
                if flag:
                    EDGE[in2].append(in1)
                else:
                    EDGE[in1].append(in2)
                EDGE_ELEMENT.append(a)
                if flag:
                    if type(class2) == func_vertex_3:
                        a.draw(*class2.select_in(event.x, event.y))
                    else:
                        a.draw(class2.in_x, class2.in_y)
                else:
                    if type(class1) == func_vertex_3:
                        a.draw(*class1.select_in(BUFFER_X, BUFFER_Y))
                    else:
                        a.draw(class1.in_x, class1.in_y)
                try:
                    result = calculate_finish_sign([0] * len(START), FINAL, VERTEX, EDGE)
                    flag = 1
                    if result is not None:
                        for r in result:
                            if r is None:
                                flag = 0
                    if result is None or result == [] or not flag:
                        bCREATE_START['state'] = DISABLED
                    else:
                        bCREATE_START['state'] = NORMAL
                except:
                    bCREATE_START['state'] = DISABLED
        BUFFER_X = None
        BUFFER_Y = None
        BUFFER_TIP = None
        canvas.delete(v)

    # Кнопка START
    elif FUNC_ELEMENT == "Start" or FUNC_ELEMENT == "0" or FUNC_ELEMENT == "1":
        a = Start_vertex(event.x, event.y, FUNC_ELEMENT, str(START.count(-1) + 1))
        EDGE.append([])
        ALL_TRANSISTOR.append([3, len(START_LIST), a])
        VERTEX.append([3, len(START_LIST)])
        START_LIST.append(a)
        if FUNC_ELEMENT == "Start":
            START.append(-1)
        elif FUNC_ELEMENT == "1":
            START.append(1)
        elif FUNC_ELEMENT == "0":
            START.append(0)
        a.paint()

    # Кнопка FINISH
    elif FUNC_ELEMENT == "Finish":
        a = Finish_vertex(event.x, event.y, str(len(FINAL_LIST) + 1))
        FINAL.append(len(ALL_TRANSISTOR))
        VERTEX.append([7, 7])
        FINAL_LIST.append(a)
        EDGE.append([])
        ALL_TRANSISTOR.append([7, 7, a])
        a.paint()

    # Кнопка NO
    elif FUNC_ELEMENT == "NO":
        a = NO_vertex(event.x, event.y)
        EDGE.append([])
        VERTEX.append([4, 4])
        NO_ELEMENT.append(a)
        ALL_TRANSISTOR.append([4, 4, a])
        a.paint()

    # Кнопка DEL ("Удалить")
    elif FUNC_ELEMENT == "DEL":
        DEE = None
        for ee in EDGE_ELEMENT:
            sr_x = (ee.in_x + ee.out_x) // 2
            sr_y = (ee.in_y + ee.out_y) // 2
            if (event.x - sr_x) ** 2 + (event.y - sr_y) ** 2 <= 16:
                DEE = ee
                break
        ind = None
        for i in range(len(ALL_TRANSISTOR)):
            if (event.x - ALL_TRANSISTOR[i][-1].x) ** 2 + (event.y - ALL_TRANSISTOR[i][-1].y) ** 2 <= 16:
                DEE = ALL_TRANSISTOR[i][-1]
                ind = i
                break
        if DEE is None:
            return
        if type(DEE) == func_edge:
            delete_edge(DEE)
        else:
            delete_vertex(DEE, ind)
            DEE.delete()
        try:
            result = calculate_finish_sign([0] * len(START), FINAL, VERTEX, EDGE)
            flag = 1
            if result is not None:
                for r in result:
                    if r is None:
                        flag = 0
            if result is None or result == [] or not flag:
                bCREATE_START['state'] = DISABLED
            else:
                bCREATE_START['state'] = NORMAL
        except:
            bCREATE_START['state'] = DISABLED


def delete_out(ind, x, y):
    """
    Удаляет все рёбра, исходящие из ФЭ
    :param ind: Номер ребра
    :param x: Координа x центра выхода
    :param y: Координата y центра выхода
    """
    global EDGE_ELEMENT, EDGE
    while True:
        flag = 0
        for ee in EDGE_ELEMENT:
            if (ee.out_x - x) ** 2 + (ee.out_y - y) ** 2 <= 16:
                delete_edge(ee)
                flag = 1
        if flag == 0:
            break
    for e in EDGE:
        if ind in e:
            e.remove(ind)


def delete_in(ind, x, y):
    """
    Удаляет все рёбра, входящие в ФЭ
    :param ind: Номер ребра
    :param x: Координа x центра входа
    :param y: Координа y центра выхода
    """
    global EDGE, EDGE_ELEMENT
    for _ in EDGE[ind]:
        for ee in EDGE_ELEMENT:
            if (ee.in_x - x) ** 2 + (ee.in_y - y) ** 2 <= 16:
                delete_edge(ee)


def delete_vertex(DEE, ind):
    """
    Удаление ФЭ
    :param DEE: ФЭ
    :param ind: Индекс ФЭ
    """
    global EDGE_ELEMENT, ALL_TRANSISTOR, EDGE, VERTEX, RED_DEL, START, START_LIST
    canvas.delete(RED_DEL[len(EDGE_ELEMENT) + ind])
    del RED_DEL[len(EDGE_ELEMENT) + ind]

    # Удаление START ФЭ
    if type(DEE) == Start_vertex:
        delete_out(ind, DEE.out_x, DEE.out_y)
        del ALL_TRANSISTOR[ind]
        del VERTEX[ind]
        del EDGE[ind]
        del START[START_LIST.index(DEE)]
        START_LIST.remove(DEE)
        i = 0
        for sl in range(len(START_LIST)):
            START_LIST[sl].rename(i + 1)
            i += 1
        i = 0
        for ver in VERTEX:
            if ver[0] == 3:
                ver[1] = i
                i += 1

    # Удаление FINAL ФЭ
    if type(DEE) == Finish_vertex:
        delete_in(ind, DEE.in_x, DEE.in_y)
        del ALL_TRANSISTOR[ind]
        del VERTEX[ind]
        del EDGE[ind]
        del FINAL[FINAL_LIST.index(DEE)]
        FINAL_LIST.remove(DEE)
        for fl in range(len(FINAL_LIST)):
            FINAL_LIST[fl].rename(fl + 1)
        for fl in range(len(FINAL_LIST)):
            for i in range(len(ALL_TRANSISTOR)):
                if ALL_TRANSISTOR[i][-1] == FINAL_LIST[fl]:
                    FINAL[fl] = i

    # Удаление AND, OR ФЭ
    if type(DEE) == func_vertex_3:
        delete_out(ind, DEE.out_x, DEE.out_y)
        delete_in(ind, DEE.in1_x, DEE.in1_y)
        delete_in(ind, DEE.in2_x, DEE.in2_y)
        del ALL_TRANSISTOR[ind]
        del VERTEX[ind]
        del EDGE[ind]
        FUNCTIONAL_ELEMENT.remove(DEE)

    # Удаление NO ФЭ
    if type(DEE) == NO_vertex:
        delete_out(ind, DEE.out_x, DEE.out_y)
        delete_in(ind, DEE.in_x, DEE.in_y)
        del ALL_TRANSISTOR[ind]
        del VERTEX[ind]
        del EDGE[ind]
        NO_ELEMENT.remove(DEE)
    for ed in range(len(EDGE)):
        for i in range(len(EDGE[ed])):
            if EDGE[ed][i] > ind:
                EDGE[ed][i] -= 1
    for f in range(len(FINAL)):
        if FINAL[f] > ind:
            FINAL[f] -= 1


def delete_edge(DEE):
    """
    Удаление
    :param DEE: Ребро
    """
    global EDGE_ELEMENT, ALL_TRANSISTOR, EDGE, RED_DEL
    canvas.delete(RED_DEL[EDGE_ELEMENT.index(DEE)])
    FEO = check_vertex(DEE.out_x, DEE.out_y, 2)
    FEI = check_vertex(DEE.in_x, DEE.in_y, 2)
    if type(FEI) is func_vertex_3:
        FEI.in_False(DEE.in_x, DEE.in_y)
    else:
        FEI.check = False
    ind1 = None
    ind2 = None
    for i in range(len(ALL_TRANSISTOR)):
        if ALL_TRANSISTOR[i][-1] == FEO:
            ind1 = i
    for i in range(len(ALL_TRANSISTOR)):
        if ALL_TRANSISTOR[i][-1] == FEI:
            ind2 = i
    if ind1 is not None and ind2 is not None and ind1 in EDGE[ind2]:
        EDGE[ind2].remove(ind1)
    del RED_DEL[EDGE_ELEMENT.index(DEE)]
    EDGE_ELEMENT.remove(DEE)
    DEE.delete()


def TEST(_):
    """Функция для отладки"""
    print(VERTEX)  # Массив вершин
    print(EDGE)  # Массив рёбер
    print(START)  # Массив стартовых вершин
    print(FINAL)  # Массив финальных вершин


def INFO(_):
    """Создаёт окно с ознокомительной информацией"""
    Temp_windows = Toplevel(root)
    Temp_windows.resizable(False, False)
    Temp_windows.minsize(200, 200)
    Temp_windows.title('Info')
    Temp_finish_label = Label(Temp_windows, bg='#ffffff', bd=0)
    text = "AND:\n0 Λ 0 -> 0\n0 Λ 1 -> 0\n1 Λ 0 -> 0\n1 Λ 1 -> 1\n"
    text += "OR:\n0 V 0 -> 0\n0 V 1 -> 1\n1 V 0 -> 1\n1 V 1 -> 1\n"
    text += "NO:\n0 -> 1\n1 -> 0\n"
    Temp_finish_label.configure(text=text, anchor="center", font="Arial 14")
    Temp_finish_label.pack(expand=True, fill=BOTH)


def Color_Button():
    """Перекрашивает кнопки в стандартный цвет"""
    bAND['bg'] = 'SystemButtonFace'
    bOR['bg'] = 'SystemButtonFace'
    bNO['bg'] = 'SystemButtonFace'
    bEDGE['bg'] = 'SystemButtonFace'
    bSTART['bg'] = 'SystemButtonFace'
    bFINISH['bg'] = 'SystemButtonFace'
    bONE['bg'] = 'SystemButtonFace'
    bZERO['bg'] = 'SystemButtonFace'
    bDEL['bg'] = 'SystemButtonFace'


def Clear_RED_DEL():
    for rd in RED_DEL:
        canvas.delete(rd)


def DEL(event):
    """Вывод на экран маркеров удаления"""
    global FUNC_ELEMENT, RED_DEL
    if event.widget['bg'] == '#00ff00':
        event.widget['bg'] = 'SystemButtonFace'
        FUNC_ELEMENT = None
        Clear_RED_DEL()
        RED_DEL = list()
        return
    Color_Button()
    event.widget['bg'] = '#00ff00'
    for ee in EDGE_ELEMENT:
        sr_x = (ee.in_x + ee.out_x) // 2
        sr_y = (ee.in_y + ee.out_y) // 2
        RED_DEL.append(canvas.create_oval(sr_x - 4, sr_y - 4, sr_x + 4, sr_y + 4, fill='red'))
    for ee in ALL_TRANSISTOR:
        RED_DEL.append(canvas.create_oval(ee[-1].x - 4, ee[-1].y - 4, ee[-1].x + 4, ee[-1].y + 4, fill='red'))
    FUNC_ELEMENT = "DEL"


def BUTTON(event):
    """Изменяет FUNC_ELEMENT на текст с нажатой кнопки"""
    global FUNC_ELEMENT, BUFFER_X, BUFFER_Y, BUFFER_TIP, RED_DEL
    Clear_RED_DEL()
    RED_DEL = list()
    FUNC_ELEMENT = event.widget.cget('text')
    Color_Button()
    event.widget['bg'] = '#00ff00'
    if v is not None:
        canvas.delete(v)
    BUFFER_X = None
    BUFFER_Y = None
    BUFFER_TIP = None


def CREATE(_):
    """Вывод результатов СФЭ"""
    result = []
    try:
        for TS in generate_bit_set(TEMP_START):
            TS = list(map(int, TS))
            result.append([[TS[i] for i in range(len(START)) if START[i] == -1], calculate_finish_sign(TS, FINAL, VERTEX, EDGE)])
    except:
        result = None
    flag = 1
    if result is not None:
        for r in result:
            if not r[1]:
                flag = 0
            for j in r[1]:
                if j is None:
                    flag = 0
    if result is not None and flag:
        if len(result) == 1:
            lFINISH.config(text=result[0][1])
        else:
            lFINISH.config(text="Success")
            Temp_windows = Toplevel(root)
            Temp_windows.resizable(False, False)
            Temp_windows.minsize(200, 200)
            Temp_windows.title('Finish')
            Temp_finish_label = Label(Temp_windows, bg='#ffffff', bd=0)
            text = "mask: " + "".join([TEMP_START[i] for i in range(len(START)) if START[i] == -1]) + "\n"
            for i in result:
                text += ("".join(map(str, i[0])) + " -> " + "".join(map(str, i[1])) + "\n")
            Temp_finish_label.configure(text=text, anchor="center", font="Arial 14")
            Temp_finish_label.pack(expand=True, fill=BOTH)
    else:
        lFINISH.config(text="Error")
    bCREATE.grid_remove()


def fSTART(_):
    """Задаёт значения стартовых ФЭ"""
    if bCREATE_START['state'] == DISABLED:
        return
    global TEMP_START
    Temp_text = "".join(i for i in lSTART.get() if i == '1' or i == '0' or i == '?')
    TEMP_START = [str(START[i]) for i in range(len(START))]
    if len(Temp_text) == START.count(-1):
        text = list(Temp_text)
        i = 0
        for j in range(len(START)):
            if START[j] == -1:
                TEMP_START[j] = text[i]
                i += 1
        bCREATE.grid()
    else:
        bCREATE.grid_remove()


def CLEAR(_):
    """Очищает все переменные"""
    global FUNC_ELEMENT, BUFFER_X, BUFFER_Y, BUFFER_TIP, v
    global FUNCTIONAL_ELEMENT, EDGE_ELEMENT, FINAL, START_LIST, ALL_TRANSISTOR, \
        NO_ELEMENT, EDGE, START, VERTEX, FINAL_LIST, TEMP_START, RED_DEL
    FUNC_ELEMENT = None
    BUFFER_X = None
    BUFFER_Y = None
    BUFFER_TIP = None
    v = None
    Clear_RED_DEL()
    RED_DEL = list()
    FUNCTIONAL_ELEMENT = list()
    EDGE_ELEMENT = list()
    START_LIST = list()
    FINAL_LIST = list()
    NO_ELEMENT = list()
    ALL_TRANSISTOR = list()
    TEMP_START = []
    START = []
    VERTEX = []
    EDGE = []
    FINAL = []
    canvas.delete("all")
    bCREATE_START['state'] = DISABLED
    bCREATE.grid_remove()


bAND.bind("<Button-1>", BUTTON)
bOR.bind("<Button-1>", BUTTON)
bNO.bind("<Button-1>", BUTTON)
bEDGE.bind("<Button-1>", BUTTON)
bSTART.bind("<Button-1>", BUTTON)
bFINISH.bind("<Button-1>", BUTTON)
bONE.bind("<Button-1>", BUTTON)
bZERO.bind("<Button-1>", BUTTON)
bDEL.bind("<Button-1>", DEL)
bCREATE.bind("<Button-1>", CREATE)
# bCHECK.bind("<Button-1>", TEST)
bCHECK.bind("<Button-1>", INFO)
bCLEAR.bind("<Button-1>", CLEAR)
bCREATE_START.bind("<Button-1>", fSTART)
canvas.bind("<Button-1>", paint)
canvas.bind("<Button-3>", back_line)

root.mainloop()
