from tkinter import *
from random import randint ,seed, choice
from time import sleep

def generator(m: int, n: int, a: int = 0, b: int = 0):
    # m, n высота и ширина
    # a, b координаты начала генерации
    dirs = ['up', 'right', 'down', 'left']  # Допустимые направления движения
    walls = ['up', 'right', 'down', 'left']
    tupik, netupik, xt, yt = False, True, 0, 0
    x, y = a, b                             # Начальное положение
    x_d, y_d = x, y                         # Временное положение
    cells = []                              # Клетки правильного пути
    stop = []                               # Поле посещения(False - не посещен, True - посещен)
    for i in range(m):                      # Генерация поля посещения
        b = []
        for j in range(n):
            b.append([False, [], []])
        stop.append(b)
    stop[x][y] = [True, [], []]
    cells.append([x, y, dirs, '', walls])   # Начальная клетка

    while True:
        while True:
            if len(cells) == 0:
                break
            else:
                cell = cells[-1]            # Последняя клетка
                x, y = cell[0], cell[1]
            if len(cell[2]) == 0 or (x == m-1 and y == n-1):
                stop[x][y][2] = cell[4]     # Если направлений движений нет, то убрать последнюю клетку
                if tupik and netupik:
                    xt, yt = x, y
                tupik = True
                netupik = False
                cells.pop()
                continue

            w = ['up', 'right', 'down', 'left']
            d = ['up', 'right', 'down', 'left']
            move = choice(cell[2])          # Выборка из допустимых направлений
            if move == 'up':                
                x_d, y_d = x-1, y           # Обновление времменых координат
                d.remove('down')
                w.remove('down')
            elif move == 'down':
                x_d, y_d = x+1, y           # Обновление времменых координат
                d.remove('up')
                w.remove('up')
            elif move == 'left':
                x_d, y_d = x, y-1           # Обновление времменых координат
                d.remove('right')
                w.remove('right')
            elif move == 'right':
                x_d, y_d = x, y+1           # Обновление времменых координат
                d.remove('left')
                w.remove('left')
            if x_d < 0 or x_d >= m or y_d < 0 or y_d >= n:  # Если направление выходит за границы,
                cell[2].remove(move)                        # то удаляем это направление
                continue
            if stop[x_d][y_d][0]:
                cell[2].remove(move)        # Если выбранная клетка уже посещена, то удаляем это направление
                continue
            netupik = True
            wall = cell[4]
            wall.remove(move)
            stop[x][y][1].append(move)      # Помечаем клетку как посещенную
            stop[x][y][2] = wall
            x, y = x_d, y_d
            stop[x][y][0] = True
            cell[3] = move                  # Добавляем направление движения
            cell[2].remove(move)
            cells.append([x, y, d, '', w])     # Добавляем новую клетку
            break
        if len(cells) == 0:
            break
    return stop, xt, yt


def print_map(a, b, x_r, y_r, x_f, y_f):
    global map_, player, finish
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
                    finish = map_.create_rectangle(x + m, y + m, x + x_map // c - m, y + y_map // c - m, fill="#f05050",
                                          outline="#f05050")
                if j == x_r and i == y_r:
                    player = map_.create_rectangle(x + m, y + m, x + x_map // c - m, y + y_map // c - m, fill="lightgreen",
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
    map_gen, x_f, y_f = generator(b, a, y_r, x_r)
    for i in range(b):
        temp = []
        for j in range(a):
            temp.append(map_gen[i][j][2])
        map_walls.append(temp)
    x_f, y_f = b - 1, a - 1
    print_map(a, b, x_r, y_r, y_f, x_f)


def change_direction(event):
    global x, y, map_walls, dirx, diry
    x_d, y_d = x, y
    dirx, diry = 0, 0
    if event.keysym == 'w' or event.keysym == 'W' or event.keysym == 'ц' or event.keysym == 'Ц':
        if not ('up' in map_walls[y][x]):
            y_d -= 1
            diry = -1
    elif event.keysym == 's' or event.keysym == 'S' or event.keysym == 'ы' or event.keysym == 'S':
        if not ('down' in map_walls[y][x]):
            y_d += 1
            diry = 1
    elif event.keysym == 'a' or event.keysym == 'A' or event.keysym == 'ф' or event.keysym == 'Ф':
        if not ('left' in map_walls[y][x]):
            x_d -= 1
            dirx = -1
    elif event.keysym == 'd' or event.keysym == 'D' or event.keysym == 'в' or event.keysym == 'В':
        if not ('right' in map_walls[y][x]):
            x_d += 1
            dirx = 1
    if 0 <= x_d < x_scale.get():
        x = x_d
    else:
        dirx = 0
    if 0 <= y_d < y_scale.get():
        y = y_d
    else:
        diry = 0
    print(x, y , map_walls[x][y], event.keysym)
    map_.move(player, dirx*x_map/x_scale.get(), diry*y_map/y_scale.get())
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
