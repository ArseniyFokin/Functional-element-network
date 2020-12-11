from tkinter import *

from calculator import calculate_finish_sign, generate_bit_set
from geometry import calculate_cursor_points

canvas_width = 700
canvas_height = 500
brush_size = 3
brush_color = "black"
FUNCELEMENT = None
BUFFER_X = None
BUFFER_Y = None
BUFFER_TIP = None
v = None

RED_DEL = list()
FUNCTIONAL_ELEMENT = list()
EDGE_ELEMENT = list()
START_LIST = list()
FINALL_LIST = list()
NO_ELEMENT = list()
ALL_TRANSISTIR = list()
TEMP_START = []
START = []  # Массив стартовых состояний
EDGE = []  # Массив всех рёбер
VERSH = []  # Массив всех вершин
FINALL = []  # Массив финальных состояний


class func_versh_3:
    def __init__(self, view, x, y):
        self.x = x
        self.y = y
        self.in1_x = x - 15
        self.in1_y = y - 15
        self.in2_x = x + 15
        self.in2_y = y - 15
        self.in3_x = x
        self.in3_y = y + 15
        self.view = view
        self.fill = "green" if view == "AND" else "red"
        self.check_in1 = False
        self.check_in2 = False
        self.line = None
        self.oval = None
        self.oval1 = None
        self.oval2 = None
        self.text = None

    def draw(self):
        self.line = canvas.create_line(self.in1_x, self.in1_y, self.in2_x, self.in2_y, self.in3_x, self.in3_y,
                                       self.in1_x, self.in1_y, fill=self.fill)
        self.oval = canvas.create_oval(self.in1_x - 4, self.in1_y - 4, self.in1_x + 4, self.in1_y + 4, fill="black",
                                       outline="black")
        self.oval1 = canvas.create_oval(self.in2_x - 4, self.in2_y - 4, self.in2_x + 4, self.in2_y + 4, fill="black",
                                        outline="black")
        self.oval2 = canvas.create_oval(self.in3_x - 4, self.in3_y - 4, self.in3_x + 4, self.in3_y + 4, fill="black",
                                        outline="black")
        if self.view == "AND":
            self.text = canvas.create_text(self.x, self.y - 5, text="Λ")
        else:
            self.text = canvas.create_text(self.x, self.y - 5, text="v")

    def check_in(self, x, y):
        if (x - self.in1_x) ** 2 + (y - self.in1_y) ** 2 <= 16:
            self.check_in1 = True
        elif (x - self.in2_x) ** 2 + (y - self.in2_y) ** 2 <= 16:
            self.check_in2 = True

    def in_False(self, x, y):
        if (x - self.in1_x) ** 2 + (y - self.in1_y) ** 2 <= 16:
            self.check_in1 = False
        elif (x - self.in2_x) ** 2 + (y - self.in2_y) ** 2 <= 16:
            self.check_in2 = False

    def delete(self):
        canvas.delete(self.line)
        canvas.delete(self.oval)
        canvas.delete(self.oval1)
        canvas.delete(self.oval2)
        canvas.delete(self.text)


class func_edge:
    def __init__(self, in_x, in_y, out_x, out_y, class1, class2):
        self.in_x = in_x
        self.in_y = in_y
        self.out_x = out_x
        self.out_y = out_y
        self.class1 = class1
        self.class2 = class2
        self.line = None
        self.line1 = None
        self.line2 = None

    def draw(self):
        self.line = canvas.create_line(self.in_x, self.in_y, self.out_x, self.out_y)
        x1, y1, x2, y2 = calculate_cursor_points(self.out_x, self.out_y, self.in_x, self.in_y)
        self.line1 = canvas.create_line(self.in_x, self.in_y, x1, y1, width=2)
        self.line2 = canvas.create_line(self.in_x, self.in_y, x2, y2, width=2)

    def delete(self):
        canvas.delete(self.line)
        canvas.delete(self.line1)
        canvas.delete(self.line2)


class Start_versh:
    def __init__(self, x, y, value):
        self.x = x
        self.y = y
        self.out_x = x
        self.out_y = y + 15
        self.value = value
        self.oval = None
        self.oval1 = None
        self.text = None

    def paint(self):
        self.oval = canvas.create_oval(self.x - 15, self.y - 15, self.x + 15, self.y + 15)
        self.oval1 = canvas.create_oval(self.x - 4, self.y + 15 - 4, self.x + 4, self.y + 15 + 4, fill="black", outline="black")
        if self.value == "Start":
            self.text = canvas.create_text(self.x, self.y, text="S" + str(START.count(-1)))
        else:
            self.text = canvas.create_text(self.x, self.y, text=self.value)

    def delete(self):
        canvas.delete(self.oval)
        canvas.delete(self.oval1)
        canvas.delete(self.text)

    def rename(self, ind):
        canvas.delete(self.text)
        self.text = canvas.create_text(self.x, self.y, text="S" + str(ind))


class Finish_versh:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.in_x = x
        self.in_y = y - 15
        self.check = False
        self.oval = None
        self.oval1 = None
        self.text = None

    def paint(self):
        self.oval = canvas.create_oval(self.x - 15, self.y - 15, self.x + 15, self.y + 15)
        self.oval1 = canvas.create_oval(self.x - 4, self.y - 15 - 4, self.x + 4, self.y - 15 + 4, fill="black", outline="black")
        self.text = canvas.create_text(self.x, self.y, text="F" + str(len(FINALL_LIST)))

    def delete(self):
        canvas.delete(self.oval)
        canvas.delete(self.oval1)
        canvas.delete(self.text)

    def rename(self, ind):
        canvas.delete(self.text)
        self.text = canvas.create_text(self.x, self.y, text="F" + str(ind))


class NO_versh:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.in_x = x
        self.in_y = y - 15
        self.out_x = x
        self.out_y = y + 15
        self.value = None
        self.check = False
        self.line = None
        self.oval = None
        self.oval1 = None
        self.text = None

    def paint(self):
        self.line = canvas.create_line(self.x - 15, self.y - 15, self.x + 15, self.y - 15, self.x, self.y + 15, self.x - 15,
                                       self.y - 15)
        # canvas.create_oval(self.x - 15, self.y - 15, self.x + 15, self.y + 15)
        self.oval = canvas.create_oval(self.x - 4, self.y - 15 - 4, self.x + 4, self.y - 15 + 4, fill="black", outline="black")
        self.oval1 = canvas.create_oval(self.x - 4, self.y + 15 - 4, self.x + 4, self.y + 15 + 4, fill="black", outline="black")
        self.text = canvas.create_text(self.x, self.y - 10, text="__")

    def delete(self):
        canvas.delete(self.line)
        canvas.delete(self.oval)
        canvas.delete(self.oval1)
        canvas.delete(self.text)


def check_versh(x, y, flag):
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
        if (x - FE.in3_x) ** 2 + (y - FE.in3_y) ** 2 <= 16:
            if flag == 1:
                BUFFER_TIP = 2
            return FE
    for SL in START_LIST:
        if (x - SL.out_x) ** 2 + (y - SL.out_y) ** 2 <= 16:
            if flag == 1:
                BUFFER_TIP = 3
            return SL
    for FL in FINALL_LIST:
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
    global BUFFER_TIP
    if BUFFER_TIP == 1 or BUFFER_TIP == 4 or BUFFER_TIP == 5:
        return True
    return False


def back_line():
    global BUFFER_X, BUFFER_Y, BUFFER_TIP
    BUFFER_X = None
    BUFFER_Y = None
    BUFFER_TIP = None
    canvas.delete(v)


def paint(event):
    global BUFFER_X, BUFFER_Y, BUFFER_TIP, v
    bCREATESTART['state'] = DISABLED
    bCREATE.grid_remove()
    if not FUNCELEMENT:
        return
    elif FUNCELEMENT != "EDGE" and BUFFER_X is not None and BUFFER_Y is not None:
        BUFFER_X = None
        BUFFER_Y = None
    elif FUNCELEMENT == "OR":
        a = func_versh_3("OR", event.x, event.y)
        EDGE.append([])
        ALL_TRANSISTIR.append([5, 5, a])
        FUNCTIONAL_ELEMENT.append(a)
        VERSH.append([5, 5])
        a.draw()
    elif FUNCELEMENT == "AND":
        a = func_versh_3("AND", event.x, event.y)
        EDGE.append([])
        ALL_TRANSISTIR.append([6, 6, a])
        FUNCTIONAL_ELEMENT.append(a)
        VERSH.append([6, 6])
        a.draw()
    elif FUNCELEMENT == "EDGE" and BUFFER_X is None and BUFFER_Y is None and BUFFER_TIP is None:
        FE = check_versh(event.x, event.y, 1)
        if FE:
            BUFFER_X = event.x
            BUFFER_Y = event.y
            v = canvas.create_oval(50, 50, 75, 75, outline="#000000", fill="#00ff00")
    elif FUNCELEMENT == "EDGE" and BUFFER_X is not None and BUFFER_Y is not None and BUFFER_TIP is not None:
        tip = BUFFER_TIP
        class1 = check_versh(BUFFER_X, BUFFER_Y, 1)
        if check_versh(event.x, event.y, 0):
            class2 = check_versh(event.x, event.y, 1)
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
                for i in range(len(ALL_TRANSISTIR)):
                    if ALL_TRANSISTIR[i][-1] == class1:
                        in1 = i
                for i in range(len(ALL_TRANSISTIR)):
                    if ALL_TRANSISTIR[i][-1] == class2:
                        in2 = i
                if flag:
                    EDGE[in2].append(in1)
                else:
                    EDGE[in1].append(in2)
                EDGE_ELEMENT.append(a)
                a.draw()
                try:
                    result = calculate_finish_sign([0] * len(START), FINALL, VERSH, EDGE)
                    if result is None or result == []:
                        bCREATESTART['state'] = DISABLED
                    else:
                        bCREATESTART['state'] = NORMAL
                except:
                    bCREATESTART['state'] = DISABLED
        BUFFER_X = None
        BUFFER_Y = None
        BUFFER_TIP = None
        canvas.delete(v)
    elif FUNCELEMENT == "Start" or FUNCELEMENT == "0" or FUNCELEMENT == "1":
        a = Start_versh(event.x, event.y, FUNCELEMENT)
        EDGE.append([])
        ALL_TRANSISTIR.append([3, len(START_LIST), a])
        VERSH.append([3, len(START_LIST)])
        START_LIST.append(a)
        if FUNCELEMENT == "Start":
            START.append(-1)
        elif FUNCELEMENT == "1":
            START.append(1)
        elif FUNCELEMENT == "0":
            START.append(0)
        a.paint()
    elif FUNCELEMENT == "Finish":
        a = Finish_versh(event.x, event.y)
        FINALL.append(len(ALL_TRANSISTIR))
        VERSH.append([7, 7])
        FINALL_LIST.append(a)
        EDGE.append([])
        ALL_TRANSISTIR.append([7, 7, a])
        a.paint()
    elif FUNCELEMENT == "NO":
        a = NO_versh(event.x, event.y)
        EDGE.append([])
        VERSH.append([4, 4])
        NO_ELEMENT.append(a)
        ALL_TRANSISTIR.append([4, 4, a])
        a.paint()
    elif FUNCELEMENT == "DEL":
        DEE = None
        for ee in EDGE_ELEMENT:
            sr_x = (ee.in_x + ee.out_x) // 2
            sr_y = (ee.in_y + ee.out_y) // 2
            if (event.x - sr_x) ** 2 + (event.y - sr_y) ** 2 <= 16:
                DEE = ee
                break
        ind = None
        for i in range(len(ALL_TRANSISTIR)):
            if (event.x - ALL_TRANSISTIR[i][-1].x) ** 2 + (event.y - ALL_TRANSISTIR[i][-1].y) ** 2 <= 16:
                DEE = ALL_TRANSISTIR[i][-1]
                ind = i
                break
        if DEE is None:
            return
        if type(DEE) == func_edge:
            delete_edge(DEE)
        else:
            delete_vertex(DEE, ind)
            DEE.delete()


def delete_out(DEE, ind, x, y):
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


def delete_in(DEE, ind, x, y):
    global EDGE, EDGE_ELEMENT
    for e in EDGE[ind]:
        for ee in EDGE_ELEMENT:
            if (ee.in_x - x) ** 2 + (ee.in_y - y) ** 2 <= 16:
                delete_edge(ee)


def delete_vertex(DEE, ind):
    global EDGE_ELEMENT, ALL_TRANSISTIR, EDGE, VERSH, RED_DEL, START, START_LIST
    canvas.delete(RED_DEL[len(EDGE_ELEMENT) + ind])
    del RED_DEL[len(EDGE_ELEMENT) + ind]
    # Удаление стартовых вершин
    if type(DEE) == Start_versh:
        delete_out(DEE, ind, DEE.out_x, DEE.out_y)
        del ALL_TRANSISTIR[ind]
        del VERSH[ind]
        del EDGE[ind]
        del START[START_LIST.index(DEE)]
        START_LIST.remove(DEE)
        for sl in range(len(START_LIST)):
            START_LIST[sl].rename(sl + 1)
        i = 0
        for ver in VERSH:
            if ver[0] == 3:
                ver[1] = i
                i += 1
    # Удаление финальных вершин
    if type(DEE) == Finish_versh:
        delete_in(DEE, ind, DEE.in_x, DEE.in_y)
        del ALL_TRANSISTIR[ind]
        del VERSH[ind]
        del EDGE[ind]
        del FINALL[FINALL_LIST.index(DEE)]
        FINALL_LIST.remove(DEE)
        for fl in range(len(FINALL_LIST)):
            FINALL_LIST[fl].rename(fl + 1)
        for fl in range(len(FINALL_LIST)):
            for i in range(len(ALL_TRANSISTIR)):
                if ALL_TRANSISTIR[i][-1] == FINALL_LIST[fl]:
                    FINALL[fl] = i
    if type(DEE) == func_versh_3:
        delete_out(DEE, ind, DEE.in3_x, DEE.in3_y)
        delete_in(DEE, ind, DEE.in1_x, DEE.in1_y)
        delete_in(DEE, ind, DEE.in2_x, DEE.in2_y)
        del ALL_TRANSISTIR[ind]
        del VERSH[ind]
        del EDGE[ind]
        FUNCTIONAL_ELEMENT.remove(DEE)
    if type(DEE) == NO_versh:
        delete_out(DEE, ind, DEE.out_x, DEE.out_y)
        delete_in(DEE, ind, DEE.in_x, DEE.in_y)
        del ALL_TRANSISTIR[ind]
        del VERSH[ind]
        del EDGE[ind]
        NO_ELEMENT.remove(DEE)
    for ed in range(len(EDGE)):
        for i in range(len(EDGE[ed])):
            if EDGE[ed][i] > ind:
                EDGE[ed][i] -= 1
    for f in range(len(FINALL)):
        if FINALL[f] > ind:
            FINALL[f] -= 1


def delete_edge(DEE):
    global EDGE_ELEMENT, ALL_TRANSISTIR, EDGE, RED_DEL
    canvas.delete(RED_DEL[EDGE_ELEMENT.index(DEE)])
    FEO = check_versh(DEE.out_x, DEE.out_y, 2)
    FEI = check_versh(DEE.in_x, DEE.in_y, 2)
    if type(FEI) is func_versh_3:
        FEI.in_False(DEE.in_x, DEE.in_y)
    else:
        FEI.check = False
    ind1 = None
    ind2 = None
    for i in range(len(ALL_TRANSISTIR)):
        if ALL_TRANSISTIR[i][-1] == FEO:
            ind1 = i
    for i in range(len(ALL_TRANSISTIR)):
        if ALL_TRANSISTIR[i][-1] == FEI:
            ind2 = i
    if ind1 is not None and ind2 is not None and ind1 in EDGE[ind2]:
        EDGE[ind2].remove(ind1)
    del RED_DEL[EDGE_ELEMENT.index(DEE)]
    EDGE_ELEMENT.remove(DEE)
    DEE.delete()


def TEST(event):
    print(VERSH)  # Массив вершин
    print(EDGE)  # Массив рёбер
    print(START)  # Массив стартовых вершин
    print(FINALL)  # Массив финальных вершин


def INFO(event):
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
    global FUNCELEMENT, RED_DEL
    if event.widget['bg'] == '#00ff00':
        event.widget['bg'] = 'SystemButtonFace'
        FUNCELEMENT = None
        Clear_RED_DEL()
        RED_DEL = list()
        return
    Color_Button()
    event.widget['bg'] = '#00ff00'
    for ee in EDGE_ELEMENT:
        sr_x = (ee.in_x + ee.out_x) // 2
        sr_y = (ee.in_y + ee.out_y) // 2
        RED_DEL.append(canvas.create_oval(sr_x - 4, sr_y - 4, sr_x + 4, sr_y + 4, fill='red'))
    for ee in ALL_TRANSISTIR:
        RED_DEL.append(canvas.create_oval(ee[-1].x - 4, ee[-1].y - 4, ee[-1].x + 4, ee[-1].y + 4, fill='red'))
    FUNCELEMENT = "DEL"


def BUTTON(event):
    global FUNCELEMENT, BUFFER_X, BUFFER_Y, BUFFER_TIP, RED_DEL
    Clear_RED_DEL()
    RED_DEL = list()
    FUNCELEMENT = event.widget.cget('text')
    Color_Button()
    event.widget['bg'] = '#00ff00'
    if v is not None:
        canvas.delete(v)
    BUFFER_X = None
    BUFFER_Y = None
    BUFFER_TIP = None


def CREATE(event):
    result = []
    try:
        for TS in generate_bit_set(TEMP_START):
            TS = list(map(int, TS))
            result.append([TS, calculate_finish_sign(TS, FINALL, VERSH, EDGE)])
    except:
        result = None
    flag = 1
    if result is not None:
        for r in result:
            if not r[1]:
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
            text = "mask: " + "".join(TEMP_START) + "\n"
            for i in result:
                text += ("".join(map(str, i[0])) + " -> " + "".join(map(str, i[1])) + "\n")
            Temp_finish_label.configure(text=text, anchor="center", font="Arial 14")
            Temp_finish_label.pack(expand=True, fill=BOTH)
    else:
        lFINISH.config(text="Error")
    bCREATE.grid_remove()


def fSTART(event):
    if bCREATESTART['state'] == DISABLED:
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


def CLEAR(event):
    global FUNCELEMENT, BUFFER_X, BUFFER_Y, BUFFER_TIP, v
    global FUNCTIONAL_ELEMENT, EDGE_ELEMENT, FINALL, START_LIST, ALL_TRANSISTIR, \
        NO_ELEMENT, EDGE, START, VERSH, FINALL_LIST, TEMP_START, RED_DEL
    FUNCELEMENT = None
    BUFFER_X = None
    BUFFER_Y = None
    BUFFER_TIP = None
    v = None
    Clear_RED_DEL()
    RED_DEL = list()
    FUNCTIONAL_ELEMENT = list()
    EDGE_ELEMENT = list()
    START_LIST = list()
    FINALL_LIST = list()
    NO_ELEMENT = list()
    ALL_TRANSISTIR = list()
    TEMP_START = []
    START = []
    VERSH = []
    EDGE = []
    FINALL = []
    canvas.delete("all")
    bCREATESTART['state'] = DISABLED
    bCREATE.grid_remove()


root = Tk()
root.title("Functional element network")
root.resizable(True, True)
root.grid_columnconfigure((0, 1, 2, 3), weight=1)
root.grid_rowconfigure(2, weight=1)

canvas = Canvas(root, width=canvas_width, height=canvas_height, bg="white")
bAND = Button(text="AND", command=None)
bOR = Button(text="OR", command=None)
bNO = Button(text="NO", command=None)
bEDGE = Button(text="EDGE", command=None)
bSTART = Button(text="Start", command=None)
bFINISH = Button(text="Finish", command=None)
bONE = Button(text="0", command=None)
bZERO = Button(text="1", command=None)
bDEL = Button(text="Удаление", command=None)
bCREATE = Button(text="Построить", command=None)
bCHECK = Button(text="Информация", command=None)
bCLEAR = Button(text="Очистить поле", command=None)
lSTART = Entry()
lFINISH = Label(bg='#ffffff')
LabelFinish = Label(text="          Finish:          ", anchor="center")
bCREATESTART = Button(root, text="Задать Start", command=None, state=DISABLED)

bAND.grid(row=0, column=0, sticky=N + S + W + E)
bOR.grid(row=0, column=1, sticky=N + S + W + E)
bNO.grid(row=0, column=2, sticky=N + S + W + E)
bEDGE.grid(row=0, column=3, sticky=N + S + W + E)
bSTART.grid(row=1, column=0, sticky=N + S + W + E)
bFINISH.grid(row=1, column=1, sticky=N + S + W + E)
bONE.grid(row=1, column=2, sticky=N + S + W + E)
bZERO.grid(row=1, column=3, sticky=N + S + W + E)
canvas.grid(row=2, column=0, columnspan=4, sticky=N + S + W + E)
bCHECK.grid(row=3, column=0, sticky=N + S + W + E)
bDEL.grid(row=3, column=1, sticky=N + S + W + E)
bCREATE.grid(row=3, column=2, columnspan=1, sticky=N + S + W + E)
bCREATE.grid_remove()
bCLEAR.grid(row=3, column=3, sticky=N + S + W + E)
bCREATESTART.grid(row=4, column=0, sticky=N + S + W + E)
lSTART.grid(row=4, column=1, sticky=N + S + W + E)
LabelFinish.grid(row=4, column=2, sticky=N + S + W + E)
lFINISH.grid(row=4, column=3, sticky=N + S + W + E)

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
bCREATESTART.bind("<Button-1>", fSTART)
canvas.bind("<Button-1>", paint)
canvas.bind("<Button-3>", back_line)

root.mainloop()
