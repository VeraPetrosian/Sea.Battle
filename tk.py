from glob import glob
from tkinter import *
from tkinter import messagebox
import time
import random
from turtle import color
import requests
import internet

adress = 'http://127.0.0.1:5000/'

stat = '0'
def check_winner():
    return internet.status()
def on_closing():
    global app_running
    if messagebox.askokcancel("Exit", "R U sure?"):
        app_running = False
        tk.destroy()

def draw_table():
    for i in range(0, s_x + 1):
        canvas.create_line(step_x * i, 0, step_x * i, size_canvas_y)
    for i in range(0, s_y + 1):
        canvas.create_line(0, step_y * i, size_canvas_x, step_y * i)

'''def button_show_enemy():
    for i in range(0, s_x):
        for j in range(0, s_y):
            if enemy_ships[j][i] > 0:
                color = "grey"
                if points[j][i] != -1:
                    color = "green"
                _id = canvas.create_rectangle(i * step_x, j * step_y, (i + 1) * step_x, (j + 1) * step_y, fill = color)
                list_ids.append(_id)'''

def button_restart():
    global list_ids
    for elem in list_ids:
        canvas.delete(elem)
    global points
    points = [[-1 for i in range(s_x)] for i in range(s_y)]
    internet.restart()

def draw_point(x, y):
    c = internet.hit(x, y)
    if c == 'Miss':
        color = "red"
        id1 = canvas.create_oval(x * step_x, y * step_y, (x + 1) * step_x, (y + 1) * step_y, fill = color)
        id2 = canvas.create_oval((x + 0.3) * step_x, (y  + 0.3) * step_y, (x + 0.7) * step_x, (y + 0.7) * step_y, fill = "white")
        list_ids.append(id1)
        list_ids.append(id2)
    elif c == 'Damaged':
        color = "green"
        id1 = canvas.create_rectangle(x * step_x, y * step_y, (x + 1) * step_x, (y + 1) * step_y, fill = color)
        id2 = canvas.create_rectangle((x + 0.3) * step_x, (y  + 0.3) * step_y, (x + 0.7) * step_x, (y + 0.7) * step_y, fill = "white")
        list_ids.append(id1)
        list_ids.append(id2)
    else:
        color = "grey"
        x0 = int(c[0])
        y0 = int(c[1])
        dir = int(c[2])
        len = int(c[3])
        for i in range(len):
            if dir == 1:
                id1 = canvas.create_rectangle((x0 + i) * step_x, y0 * step_y, (x0 + i + 1) * step_x, (y0 + 1) * step_y, fill = color)
                list_ids.append(id1)
            else:
                id1 = canvas.create_rectangle((x0) * step_x, (y0 + i) * step_y, (x0 + 1) * step_x, (y0 + 1 + i) * step_y, fill = color)
                list_ids.append(id1)


def add_to_all(event):
    global points
    _type = 0 #left
    if event.num == 3:
        _type = 1 #right
    mouse_x = canvas.winfo_pointerx() - canvas.winfo_rootx()
    mouse_y = canvas.winfo_pointery() - canvas.winfo_rooty()
    gc_x = mouse_x // step_x
    gc_y = mouse_y // step_y
    if gc_x < s_x and gc_y < s_y:
        if points[gc_y][gc_x] == -1:
            points[gc_y][gc_x] = _type
            draw_point(gc_x, gc_y)
            status = check_winner()
            if status == '20':
                if messagebox.askretrycancel("Congrats!!!", "Want 1 more game?"):
                    button_restart()
                else:
                    on_closing()
                points = [[10 for i in range(s_x)] for i in range(s_y)]

        
tk = Tk()
app_running = True

size_canvas_x = 500
size_canvas_y = 500
s_x = s_y = 10
step_x = size_canvas_x // s_x
step_y = size_canvas_y // s_y
size_canvas_x = step_x * s_x
size_canvas_y = step_y * s_y
menu_x = step_x * 4
enemy_ships = [[0 for i in range(s_x + 1)] for i in range(s_y + 1)]
list_ids = []
points = [[-1 for i in range(s_x)] for i in range(s_y)]

tk.protocol("WM_DELETE_WINDOW", on_closing)
tk.title("Game WS")
tk.resizable(0, 0)
#tk.wm_attributes("-topmost", 1)
canvas = Canvas(tk, width=size_canvas_x + menu_x, height=size_canvas_y, bd=0, highlightthickness=0)
canvas.create_rectangle(0, 0 ,size_canvas_x, size_canvas_y, fill="white")
canvas.pack()
tk.update()

draw_table()

b1 = Button(tk, text="Restart", command = button_restart)
b1.place(x = size_canvas_x + 20, y = 70)

canvas.bind_all(" <Button-1>", add_to_all) #left mouse
canvas.bind_all("<Button-3>", add_to_all) #right mouse





while app_running:
    if app_running:
        tk.update_idletasks()
        tk.update()
    time.sleep(0.05)
