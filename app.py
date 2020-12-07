from tkinter import *
from calculator import calculate_finish_sign

canvas_width = 700
canvas_height = 500
brush_size = 3
brush_color = "black"
FUNCELEMENT = None
BUFFER_X = None
BUFFER_Y = None
BUFFER_TIP = None
v = None

FUNCTIONAL_ELEMENT = list()
EDGE_ELEMENT = list()
START_LIST = list()
FINALL_LIST = list()
NO_ELEMENT = list()
ALL_TRANSISTIR = list()
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

    def draw(self):
        canvas.create_line(self.in1_x, self.in1_y, self.in2_x, self.in2_y, self.in3_x, self.in3_y, self.in1_x,
                           self.in1_y, fill=self.fill)
        canvas.create_oval(self.in1_x - 4, self.in1_y - 4, self.in1_x + 4, self.in1_y + 4, fill="black",
                           outline="black")
        canvas.create_oval(self.in2_x - 4, self.in2_y - 4, self.in2_x + 4, self.in2_y + 4, fill="black",
                           outline="black")
        canvas.create_oval(self.in3_x - 4, self.in3_y - 4, self.in3_x + 4, self.in3_y + 4, fill="black",
                           outline="black")
        if self.view == "AND":
            canvas.create_text(self.x, self.y - 5, text="Λ")
        else:
            canvas.create_text(self.x, self.y - 5, text="v")

    def check_in(self, x, y):
        if (x - self.in1_x) ** 2 + (y - self.in1_y) ** 2 <= 16:
            self.check_in1 = True
        if (x - self.in2_x) ** 2 + (y - self.in2_y) ** 2 <= 16:
            self.check_in2 = True


class func_edge:
    def __init__(self, in_x, in_y, out_x, out_y, class1, class2):
        self.in_x = in_x
        self.in_y = in_y
        self.out_x = out_x
        self.out_y = out_y
        self.class1 = class1
        self.class2 = class2

    def draw(self):
        canvas.create_line(self.in_x, self.in_y, self.out_x, self.out_y)


class Start_versh:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.out_x = x
        self.out_y = y + 15
        self.value = None

    def paint(self):
        canvas.create_oval(self.x - 15, self.y - 15, self.x + 15, self.y + 15)
        canvas.create_oval(self.x - 4, self.y + 15 - 4, self.x + 4, self.y + 15 + 4, fill="black", outline="black")
        canvas.create_text(self.x, self.y, text="S" + str(len(START_LIST)))


class Finish_versh:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.in_x = x
        self.in_y = y - 15
        self.check = False

    def paint(self):
        canvas.create_oval(self.x - 15, self.y - 15, self.x + 15, self.y + 15)
        canvas.create_oval(self.x - 4, self.y - 15 - 4, self.x + 4, self.y - 15 + 4, fill="black", outline="black")
        canvas.create_text(self.x, self.y, text="F" + str(len(FINALL_LIST)))


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

    def paint(self):
        canvas.create_oval(self.x - 15, self.y - 15, self.x + 15, self.y + 15)
        canvas.create_oval(self.x - 4, self.y - 15 - 4, self.x + 4, self.y - 15 + 4, fill="black", outline="black")
        canvas.create_oval(self.x - 4, self.y + 15 - 4, self.x + 4, self.y + 15 + 4, fill="black", outline="black")
        canvas.create_text(self.x, self.y, text="NO")


def check_versh(x, y, flag):
    global BUFFER_TIP
    for FE in FUNCTIONAL_ELEMENT:
        if (x - FE.in1_x) ** 2 + (y - FE.in1_y) ** 2 <= 16 and not FE.check_in1:
            if flag == 1:
                BUFFER_TIP = 1
            return FE
    for FE in FUNCTIONAL_ELEMENT:
        if (x - FE.in2_x) ** 2 + (y - FE.in2_y) ** 2 <= 16 and not FE.check_in2:
            if flag == 1:
                BUFFER_TIP = 1
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
        if (x - FL.in_x) ** 2 + (y - FL.in_y) ** 2 <= 16 and not FL.check:
            if flag == 1:
                BUFFER_TIP = 4
            return FL
    for NOE in NO_ELEMENT:
        if (x - NOE.in_x) ** 2 + (y - NOE.in_y) ** 2 <= 16 and not NOE.check:
            if flag == 1:
                BUFFER_TIP = 5
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
            v = canvas.create_oval(50, 50, 75, 75, outline="green", fill="green")
    elif FUNCELEMENT == "EDGE" and BUFFER_X is not None and BUFFER_Y is not None and BUFFER_TIP is not None:
        tip = BUFFER_TIP
        class1 = check_versh(BUFFER_X, BUFFER_Y, 1)
        if check_versh(event.x, event.y, 0):
            class2 = check_versh(event.x, event.y, 1)
            if BUFFER_TIP != tip and (class1.x != class2.x and class1.y != class2.y) and (
                    BUFFER_TIP != 3 or tip != 2) and (BUFFER_TIP != 2 or tip != 3) and (
                    BUFFER_TIP != 5 or tip != 1) and (BUFFER_TIP != 1 or tip != 5):
                if BUFFER_TIP == 1:
                    class2.check_in(event.x, event.y)
                elif tip == 1:
                    class1.check_in(BUFFER_X, BUFFER_Y)
                elif BUFFER_TIP == 4 and ((event.x - class2.in_x) ** 2 + (event.y - class2.in_y) ** 2 <= 9):
                    class2.check = True
                elif tip == 4 and ((BUFFER_X - class1.in_x) ** 2 + (BUFFER_Y - class1.in_y) ** 2 <= 9):
                    class1.check = True
                elif BUFFER_TIP == 5:
                    class2.check = True
                elif tip == 5:
                    class1.check = True
                flag = check_edge()
                if flag:
                    a = func_edge(BUFFER_X, BUFFER_Y, event.x, event.y, class2, class1)
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
        BUFFER_X = None
        BUFFER_Y = None
        BUFFER_TIP = None
        canvas.delete(v)
    elif FUNCELEMENT == "Start":
        a = Start_versh(event.x, event.y)
        EDGE.append([])
        ALL_TRANSISTIR.append([3, len(START_LIST), a])
        VERSH.append([3, len(START_LIST)])
        START_LIST.append(a)
        START.append(-1)
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


def TEST(event):
    print(VERSH)  # Массив вершин
    print(EDGE)  # Массив рёбер
    print(START)  # Массив стартовых вершин
    print(FINALL)  # Массив финальных вершин


def BUTTON(event):
    global FUNCELEMENT
    FUNCELEMENT = event.widget.cget('text')
    bAND['bg'] = 'SystemButtonFace'
    bOR['bg'] = 'SystemButtonFace'
    bNO['bg'] = 'SystemButtonFace'
    bEDGE['bg'] = 'SystemButtonFace'
    bSTART['bg'] = 'SystemButtonFace'
    bFINISH['bg'] = 'SystemButtonFace'
    event.widget['bg'] = '#00ff00'


def CREATE(event):
    try:
        result = calculate_finish_sign(START, FINALL, VERSH, EDGE)
    except:
        result = [None]
    if None not in result:
        lFINISH.config(text=result)
    else:
        lFINISH.config(text="Error")
    bCREATE.grid_remove()


def fSTART(event):
    if len(lSTART.get()) == len(START):
        text = list(lSTART.get())
        for i in range(len(START_LIST)):
            START[i] = int(text[i])
        bCREATE.grid()
    else:
        bCREATE.grid_remove()


def CLEAR(event):
    global FUNCELEMENT, BUFFER_X, BUFFER_Y, BUFFER_TIP, v
    global FUNCTIONAL_ELEMENT, EDGE_ELEMENT, FINALL, START_LIST, ALL_TRANSISTIR, NO_ELEMENT, EDGE, START, VERSH, FINALL_LIST
    FUNCELEMENT = None
    BUFFER_X = None
    BUFFER_Y = None
    BUFFER_TIP = None
    v = None
    FUNCTIONAL_ELEMENT = list()
    EDGE_ELEMENT = list()
    START_LIST = list()
    FINALL_LIST = list()
    NO_ELEMENT = list()
    ALL_TRANSISTIR = list()
    START = []
    VERSH = []
    EDGE = []
    FINALL = []
    canvas.delete("all")


root = Tk()
root.title("Functional element network")

canvas = Canvas(root, width=canvas_width, height=canvas_height, bg="white")
bAND = Button(text="AND", command=None)
bOR = Button(text="OR", command=None)
bNO = Button(text="NO", command=None)
bEDGE = Button(text="EDGE", command=None)
bSTART = Button(text="Start", command=None)
bFINISH = Button(text="Finish", command=None)
bCREATE = Button(text="Построить", command=None)
bCHECK = Button(text="Тест", command=None)
bCLEAR = Button(text="Очистить поле", command=None)
lSTART = Entry()
lFINISH = Label()
LabelFinish = Label(text="Finish:")
bCREATESTART = Button(text="Задать Start", command=None)

bAND.grid(row=0, column=0, sticky=N + S + W + E)
bOR.grid(row=0, column=1, sticky=N + S + W + E)
bNO.grid(row=0, column=2, sticky=N + S + W + E)
bEDGE.grid(row=0, column=3, sticky=N + S + W + E)
bSTART.grid(row=0, column=4, sticky=N + S + W + E)
bFINISH.grid(row=0, column=5, sticky=N + S + W + E)
bCHECK.grid(row=2, column=0, sticky=N + S + W + E)
bCREATE.grid(row=2, column=1, columnspan=3, sticky=N + S + W + E)
bCREATE.grid_remove()
bCLEAR.grid(row=2, column=4, columnspan=2, sticky=N + S + W + E)
bCREATESTART.grid(row=3, column=0, sticky=N + S + W + E)
lSTART.grid(row=3, column=1, columnspan=2, sticky=N + S + W + E)
LabelFinish.grid(row=3, column=3, sticky=N + S + W + E)
lFINISH.grid(row=3, column=4, columnspan=2, sticky=N + S + W + E)
canvas.grid(row=1, column=0, columnspan=6)

bAND.bind("<Button-1>", BUTTON)
bOR.bind("<Button-1>", BUTTON)
bNO.bind("<Button-1>", BUTTON)
bEDGE.bind("<Button-1>", BUTTON)
bSTART.bind("<Button-1>", BUTTON)
bFINISH.bind("<Button-1>", BUTTON)
bCREATE.bind("<Button-1>", CREATE)
bCHECK.bind("<Button-1>", TEST)
bCLEAR.bind("<Button-1>", CLEAR)
bCREATESTART.bind("<Button-1>", fSTART)
canvas.bind("<Button-1>", paint)
canvas.bind("<Button-3>", back_line)

print(bAND["bg"])

root.mainloop()
