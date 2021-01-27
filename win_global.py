"""Модуль, содержащий в себе окно программы"""

from tkinter import *

canvas_width = 700
canvas_height = 500
brush_size = 3  # Размер кисти
brush_color = "black"  # Цвет кисти

root = Tk()
root.title("Functional element network")  # Имя окна
# file_menu = Menu(root)
# root.config(menu=file_menu)
# file_menu.add_command(label='Файл')
root.resizable(True, True)
root.minsize(360, 240)
root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(0, weight=1)

frame_1 = Frame(root)
frame_2 = LabelFrame(root)
frame_3 = Frame(root)

canvas = Canvas(frame_2, bg="white", width=canvas_width, height=canvas_height)

bAND = Button(frame_1, text="AND", command=None, width=13)
bOR = Button(frame_1, text="OR", command=None, width=13)
bNO = Button(frame_1, text="NO", command=None, width=13)
bEDGE = Button(frame_1, text="EDGE", command=None, width=13)
bSTART = Button(frame_1, text="Start", command=None)
bFINISH = Button(frame_1, text="Finish", command=None)
bONE = Button(frame_1, text="0", command=None)
bZERO = Button(frame_1, text="1", command=None)
bCREATE = Button(frame_3, text="Посчитать", command=None)
bDEL = Button(frame_3, text="Удалить", command=None)
bCHECK = Button(frame_3, text="Информация", command=None, width=13)
bCLEAR = Button(frame_3, text="Очистить поле", command=None)
lSTART = Entry(frame_3, width=13)
lFINISH = Label(frame_3, bg='#ffffff')
LabelFinish = Label(frame_3, text="Finish:", anchor="center", width=13)
bCREATE_START = Button(frame_3, text="Задать Start", command=None, state=DISABLED)


def button_place():
    frame_1.grid(row=0, sticky=W + E)
    frame_1.columnconfigure((0, 1, 2, 3), weight=1)
    bAND.grid(row=0, column=0, sticky=N + S + W + E)
    bOR.grid(row=0, column=1, sticky=N + S + W + E)
    bNO.grid(row=0, column=2, sticky=N + S + W + E)
    bEDGE.grid(row=0, column=3, sticky=N + S + W + E)
    bSTART.grid(row=1, column=0, sticky=N + S + W + E)
    bFINISH.grid(row=1, column=1, sticky=N + S + W + E)
    bONE.grid(row=1, column=2, sticky=N + S + W + E)
    bZERO.grid(row=1, column=3, sticky=N + S + W + E)

    frame_2.grid(row=1, sticky=N + S + W + E)
    frame_2.columnconfigure(0, weight=1)
    frame_2.rowconfigure(0, weight=1)
    canvas.grid(sticky=N + S + W + E)

    frame_3.grid(row=2, sticky=W + E)
    frame_3.columnconfigure((0, 1, 2, 3), weight=1)
    bCHECK.grid(row=0, column=0, sticky=N + S + W + E)
    bDEL.grid(row=0, column=1, sticky=N + S + W + E)
    bCREATE.grid(row=0, column=2, sticky=N + S + W + E)
    bCREATE.grid_remove()
    bCLEAR.grid(row=0, column=3, sticky=N + S + W + E)
    bCREATE_START.grid(row=1, column=0, sticky=N + S + W + E)
    lSTART.grid(row=1, column=1, sticky=N + S + W + E)
    LabelFinish.grid(row=1, column=2, sticky=N + S + W + E)
    lFINISH.grid(row=1, column=3, sticky=N + S + W + E)


button_place()
