from tkinter import *
from random import randint ,seed
import gen


def print_map(a, b, x_r, y_r, x_f, y_f):
    global map_
    map_.delete(ALL)
    c = max(a, b)
    n = x_map // (c * 3)
    if n % 2 == 0:
        m = n // 2
    else:
        m = n // 2 + 1
    for i in range(b):
        for j in range(a):
            cell = map_walls[i][j]
            x, y = (x_map // c) * j + 3, (y_map // c) * i + 3
            for wall in cell:
                if j == x_f and i == y_f:
                    map_.create_rectangle(x + m, y + m, x + x_map // c - m, y + y_map // c - m, fill="#f05050",
                                          outline="#f05050")
                if j == x_r and i == y_r:
                    map_.create_rectangle(x + m, y + m, x + x_map // c - m, y + y_map // c - m, fill="lightgreen",
                                          outline="lightgreen")
                if wall == 'up':
                    map_.create_line(x - n // 2, y, x + x_map // c + n // 2, y, width=n)
                if wall == 'right':
                    map_.create_line(x + x_map // c, y - n // 2, x + x_map // c, y + y_map // c + n // 2, width=n)
                if wall == 'down':
                    map_.create_line(x - n // 2, y + y_map // c, x + x_map // c + m, y + y_map // c, width=n)
                if wall == 'left':
                    map_.create_line(x, y - n // 2, x, y + y_map // c + n // 2, width=n)
    map_.focus_set()


def generate_map():
    global map_walls, x, y
    seed_map = seed_input.get()
    if len(seed_map) != 0:
        seed(seed_map)
    map_walls = []
    a, b = x_scale.get(), y_scale.get()
    if var.get():
        x_r, y_r = randint(0, a-1), randint(0, b-1)
    else:
        x_r, y_r = 0, 0
    x, y = x_r, y_r
    map_gen, x_f, y_f = gen.generator(b, a, y_r, x_r)
    for i in range(b):
        temp = []
        for j in range(a):
            temp.append(map_gen[i][j][2])
        map_walls.append(temp)
    x_f, y_f = b - 1, a - 1
    print_map(a, b, x_r, y_r, y_f, x_f)


def change_direction(event):
    global x, y, map_walls
    x_d, y_d = x, y
    if event.keysym == 'w':
        if not ('up' in map_walls[y][x]):
            y_d -= 1
    elif event.keysym == 's':
        if not ('down' in map_walls[y][x]):
            y_d += 1
    elif event.keysym == 'a':
        if not ('left' in map_walls[y][x]):
            x_d -= 1
    elif event.keysym == 'd':
        if not ('right' in map_walls[y][x]):
            x_d += 1
    if 0 <= x_d < x_scale.get():
        x = x_d
    if 0 <= y_d < y_scale.get():
        y = y_d
    print(x, y , map_walls[x][y], event.keysym)
    print_map(x_scale.get(), y_scale.get(), x, y, x_scale.get() - 1, y_scale.get() - 1)
    if x == x_scale.get() - 1 and y == y_scale.get() - 1:
        generate_map()


map_walls = []

root = Tk()
root.title("Maze")
root.minsize(width=1000, height=656)
root.resizable(False, False)

x_map, y_map = 650, 650
map_ = Canvas(root, width=x_map+3, height=y_map+3, bg="#ffffff")

x, y = 0, 0

x_lbl = Label(text="X")
y_lbl = Label(text="Y")
seed_lbl = Label(text="Seed:")

x_scale = Scale(root, orient=HORIZONTAL, length=300, from_=5, to=100, tickinterval=10, resolution=1)
y_scale = Scale(root, orient=HORIZONTAL, length=300, from_=5, to=100, tickinterval=10, resolution=1)

gen_btn = Button(text="Generate", command=generate_map)
gen_btn.bind('<Return>', generate_map)

var = BooleanVar(root)
var.set(False)
rand_check = Checkbutton(text="Рандомный старт", variable=var)

seed_input = Entry(width=14)

map_.place(relx=0, rely=0, x=-1, y=-1)
map_.bind("<KeyPress>", change_direction)

x_lbl.place(relx=1, rely=0, x=-330, y=20)
x_scale.place(relx=1, rely=0, x=-310)
y_lbl.place(relx=1, rely=0, x=-330, y=90)
y_scale.place(relx=1, rely=0, x=-310, y=70)

gen_btn.place(relx=1, rely=0, x=-180, y=160)

rand_check.place(relx=1, rely=0, x=-330, y=160)
seed_lbl.place(relx=1, rely=0, x=-330, y=130)
seed_input.place(relx=1, rely=0, x=-295, y=130)

root.mainloop()
