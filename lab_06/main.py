from tkinter import *
from tkinter import messagebox, ttk
import numpy as np
import matplotlib.pyplot as plt

from time import time, sleep

import colorutils as cu

def rgb_to_hex(rgb):
    return f'#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}'

WIN_WIDTH = 1600
WIN_HEIGHT = 900
WIN_COLOR = 'dark slate gray'

CV_WIDE = 900
CV_HEIGHT = 900
CV_COLOR = "#000000" #rgb_to_hex((253, 245, 230)) #f3e6ff" #"#cce6ff"
MAIN_TEXT_COLOR = "#b566ff" #"lightblue" a94dff
FONT_COLOR = 'linen'

BTN_TEXT_COLOR = "#4d94ff"


LINES = []
FIRST_POINT = []
LOG = []

win = Tk()
win['bg'] = WIN_COLOR
win.geometry("%dx%d" %(WIN_WIDTH, WIN_HEIGHT))
win.attributes("-fullscreen", True)

canv = Canvas(win, width = CV_WIDE, height = CV_HEIGHT, bg = CV_COLOR)
canv.place(x = 0, y = 0)

canv.delete("all")

image_canvas = PhotoImage(width = CV_WIDE + 100, height = CV_HEIGHT + 100)
canv.create_image((CV_WIDE // 2 + 50, CV_HEIGHT // 2 + 50) , image = image_canvas, state = NORMAL)
print(image_canvas.get(450, 450))


def sign(a):
    if (a < 0):
        return -1
    elif (a == 0):
        return 0
    else:
        return 1

def brez_int(x1, y1, x2, y2, color):
    x = x1
    y = y1
    dx = x2 - x1
    dy = y2 - y1
    sx = sign(dx)
    sy = sign(dy)
    dx = abs(dx)
    dy = abs(dy)
    obmen = 0
    if dx < dy:
        obmen = 1
        dx, dy = dy, dx
    e = 2 * dy - dx
    points = []
    for _ in range (0, int(dx) + 1):
        points.append([x, y, color])
        if e >= 0:
            if obmen == 1:
                x += sx
            else:
                y += sy
            e = e - 2 * dx
        if obmen == 1:
            y += sy
        else:
            x += sx
        e = e + 2 * dy
    return points

def render_line(coords):
    for point in coords:
        x = point[0]
        y = point[1]
        c = point[2]
        image_canvas.put(rgb_to_hex(c), to=(x, y))

def point_io():
    try:
        x = int(x_entry.get()) + CV_WIDE // 2
        y = -int(y_entry.get()) + CV_HEIGHT // 2
    except:
        messagebox.showerror("Ошибка", "Неверно введены координаты точки")
        return
    add_dot(x, y)

def add_dot_click(event):
    x = int(event.x)
    y = int(event.y)

    add_dot(x, y)

def add_dot(x, y):
    global LINES, FIRST_POINT, LOG
    LOG.append([LINES, FIRST_POINT])
    if len(LINES) == 0 or len((LINES[-1])[-1]) > 1:
        LINES.append([])
        FIRST_POINT = [x, y]
    if len(LINES[-1]) and len((LINES[-1])[-1]) < 2:
        ((LINES[-1])[-1]).append([x, y])
    LINES[-1].append([[x, y]])
    if len(LINES[-1]) > 1:
        l = brez_int((LINES[-1])[-2][0][0], (LINES[-1])[-2][0][1], (LINES[-1])[-2][1][0], (LINES[-1])[-2][1][1], (255, 255, 255))
        render_line(l)

def close_dot_click(event):
    close_lines()

def close_lines():
    global LINES
    LOG.append([LINES.copy(), FIRST_POINT])
    if len((LINES[-1])[-1]) < 2:
        ((LINES[-1])[-1]).append(FIRST_POINT)
        l = brez_int((LINES[-1])[-1][0][0], (LINES[-1])[-1][0][1], (LINES[-1])[-1][1][0], (LINES[-1])[-1][1][1], (255, 255, 255))
        render_line(l)

def fill_io(event, color_i, delay):
    canv.update()
    if delay == 1:
        d = True
    else:
        d = False

    x = int(event.x)
    y = int(event.y)

    for line in LINES:
        for point in line:
            if len(point) != 2:
                return

    match color_i:
        case 0:
            color = (0, 0, 255)
        case 1:
            color = (255, 0, 0)
        case 2:
            color = (0, 255, 0)
    fill_func(x, y, color, d)




def reboot_prog():
    global LINES, FIRST_POINT, LOG, image_canvas

    canv.delete(ALL)

    LINES = []
    FIRST_POINT = []
    LOG = []

    image_canvas = PhotoImage(width = CV_WIDE, height = CV_HEIGHT)
    canv.create_image((CV_WIDE / 2, CV_HEIGHT / 2), image = image_canvas, state = NORMAL)

def cancel_action():
    global LINES, FIRST_POINT, LOG
    print(LINES)
    print(FIRST_POINT)
    print(LOG)
    LINES = LOG[-1][0]
    FIRST_POINT = LOG[-1][1]
    print(LINES)
    print(FIRST_POINT)
    LOG.pop()
    canv.delete(ALL)
    canv.create_image((CV_WIDE / 2, CV_HEIGHT / 2), image = image_canvas, state = NORMAL)
    for fig in LINES:
        for line in fig:
            print(line)
            if len(line) == 2:
                l = canv.create_line(tuple(line))

def fill_func(xs, ys, fill_c, delay = 0):
    start = time()
    stack = []
    stack.append((xs, ys))
    while len(stack) > 0:
        # print(stack)
        point = stack.pop()
        x = point[0]
        y = point[1]
        if x < 0 or x > CV_WIDE or y < 0 or y > CV_HEIGHT:
            continue
        pix_color = image_canvas.get(x, y)
        while pix_color != (255, 255, 255) and x > 0:
            image_canvas.put(rgb_to_hex(fill_c), to=(x, y))
            x -= 1
            pix_color = image_canvas.get(x, y)
        x_left = x + 1
        x = point[0]
        pix_color = image_canvas.get(x, y)
        while pix_color != (255, 255, 255) and x < CV_WIDE:
            image_canvas.put(rgb_to_hex(fill_c), to=(x, y))
            x += 1
            pix_color = image_canvas.get(x, y)
        x_right = x - 1
        x = x_left
        flag = False
        while x <= x_right:
            pix_color = image_canvas.get(x, y + 1)
            while pix_color != (255, 255, 255) and pix_color != fill_c and x <= x_right:
                flag = True
                x += 1
                pix_color = image_canvas.get(x, y + 1)
            if flag:
                if x == x_right and pix_color != (255,255,255) and pix_color != fill_c and y + 1 < CV_HEIGHT:
                    stack.append((x, y + 1)) 
                else:
                    stack.append((x - 1, y + 1))
                flag = False
            x_start = x

            while (pix_color == (255,255,255) or pix_color == fill_c) and x < x_right:
                x += 1
                pix_color = image_canvas.get(x, y + 1)
            if x == x_start:
                x += 1
        x = x_left
        flag = False
        while x <= x_right:
            pix_color = image_canvas.get(x, y - 1)
            while pix_color != (255,255,255) and pix_color != fill_c and x <= x_right:
                flag = True
                x += 1
                pix_color = image_canvas.get(x, y - 1)

            if flag:
                if x == x_right and pix_color != (255,255,255) and pix_color != fill_c and y - 1 > 0:
                    stack.append((x, y - 1))
                else:
                    stack.append((x - 1, y - 1))
                flag = False

            x_start = x
            while (pix_color == (255,255,255) or pix_color == fill_c) and x < x_right:
                x += 1
                pix_color = image_canvas.get(x, y - 1)

            if x == x_start:
                x += 1
        if delay == 1:
            canv.update()
            res = time() - start
            time_label.configure(text='Время: {:.2f} с'.format(res))
    time_label.configure(text='Время: {:.2f} с'.format(time() - start))

def config_rbs(a):
    match a:
        case 0:
            draw_delay.configure(fg='pink')
            draw_without_delay.configure(fg=FONT_COLOR)
        case 1:
            draw_without_delay.configure(fg='pink')
            draw_delay.configure(fg=FONT_COLOR)

def aboutprog():
    messagebox.showinfo(title='О программе', message='Демонстрация работы алгоритма заполнения по ребрам.')
# Add dot

color_text = Label(win, text = "Цвет отрезка", width = 43, font="-size 16", bg=WIN_COLOR, fg=FONT_COLOR)
color_text.place(x = CV_WIDE + 20, y = 240)

color_cmbb = ttk.Combobox(win, state='readonly', width=40, font="-size 16")
win.option_add('*TCombobox*Listbox.font', '-size 14')
color_cmbb['values'] = ['Синий', 'Красный', 'Зеленый']
color_cmbb.place(x = CV_WIDE + 60, y = 280)
color_cmbb.current(0)

add_dot_text = Label(win, text = "Добавить точку", width = 43, font="-size 16", bg=WIN_COLOR, fg=FONT_COLOR)
add_dot_text.place(x = CV_WIDE + 20, y = 20)

x_text = Label(text = "x: ", font="-size 14", bg=WIN_COLOR, fg=FONT_COLOR)
x_text.place(x = CV_WIDE + 70, y = 70)

x_entry = Entry(font="-size 14", width = 9)
x_entry.place(x = CV_WIDE + 90, y = 70)

y_text = Label(text = "y: ", font="-size 14", bg=WIN_COLOR, fg=FONT_COLOR)
y_text.place(x = CV_WIDE + 330, y = 70)

y_entry = Entry(font="-size 14", width = 9)
y_entry.place(x = CV_WIDE + 350, y = 70)

add_dot_btn = Button(win, text = "Добавить точку", font="-size 14", command = lambda: point_io())
add_dot_btn.place(x = CV_WIDE + 200, y = 120)

make_figure_btn = Button(win, text = "Замкнуть фигуру", font="-size 14", command = lambda: close_lines())
make_figure_btn.place(x = CV_WIDE + 190, y = 190)

# Fill figure

color_text = Label(win, text = "Выбрать тип закраски", width = 43, font="-size 16", bg=WIN_COLOR, fg=FONT_COLOR)
color_text.place(x = CV_WIDE + 20, y = 370)

option_filling = IntVar()
option_filling.set(1)

draw_delay = Radiobutton(text = "С задержкой", font="-size 14", variable = option_filling, value = 1, indicatoron=True, bg = WIN_COLOR, fg=FONT_COLOR, activebackground=WIN_COLOR, highlightbackground = WIN_COLOR, command=lambda: config_rbs(0))
draw_delay.place(x = CV_WIDE + 25, y = 410)

draw_without_delay = Radiobutton(text = "Без задержки", font="-size 14", variable = option_filling, value = 2, indicatoron=True, bg = WIN_COLOR, fg=FONT_COLOR, activebackground=WIN_COLOR, highlightbackground = WIN_COLOR, command=lambda: config_rbs(1))
draw_without_delay.place(x = CV_WIDE + 350, y = 410)

# fill_figure_btn = Button(win, text = "Закрасить выбранную область", font="-size 14", command = lambda: fill_io(color_cmbb.current(), option_filling.get()))
# fill_figure_btn.place(x = CV_WIDE + 150, y = 460)

# Time and clear

time_label = Label(text = f"Время: {0.00} с", font="-size 16", bg = "lightgrey")
time_label.place(x = 20, y = CV_HEIGHT - 100)

clear_win_btn = Button(win, text = "Очистить экран", font="-size 15", command = lambda: reboot_prog(), width = 15, height=2)
clear_win_btn.place(x = CV_WIDE + 240, y = 540)

exit_btn = Button(win, text = "Выход", font="-size 15", command = lambda: win.quit(), width = 12, height=2)
exit_btn.place(x = CV_WIDE + 40, y = 540)

# back_btn = Button(win, text='Отмена действия', font='-size 15', command=lambda: cancel_action(), width=15, height=2)
# back_btn.place(x = CV_WIDE + 40, y = 620)

credits = Button(win, text = "Об авторе", font="-size 8", command = lambda: messagebox.showinfo(title='Об авторе', message='Золотухин Алексей ИУ7-44Б'), width = 15, height = 2)
credits.place(x = 10, y = 10)

about_prog = Button(win, text = "О программе", font="-size 8", command = lambda: aboutprog(), width = 15, height = 2)
about_prog.place(x = 10, y = 55)

canv.bind("<1>", add_dot_click)
win.bind("<space>", close_dot_click)
canv.bind("<3>", lambda event: fill_io(event, color_cmbb.current(), option_filling.get()))


win.mainloop()