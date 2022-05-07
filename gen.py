from random import choice, randint


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


def lab_print_gen(stop, a):
    global m, n
    for i in range(m):
        for j in range(n):
            for k in stop[i][j][1]:
                if k == 'up':
                    a[i*2][j*2+1] = ' '
                if k == 'right':
                    a[i*2+1][j*2+2] = ' '
                if k == 'down':
                    a[i*2+2][j*2+1] = ' '
                if k == 'left':
                    a[i*2+1][j*2] = ' '
    return a


def main():
    global m, n
    m, n = input('Размер: ').split()
    m = int(m)
    n = int(n)
    a0, b0 = randint(0, m), randint(0, n)
    gen_map = generator(m, n, 0, 0)
    x, y = m * 2 - 1, n * 2 - 1
    ch = chr(127)

    a = []
    b = []
    for i in range(m * 2 + 1):
        b = []
        for j in range(n * 2 + 1):
            if i % 2 == 1 and j % 2 == 1:
                b.append(' ')
            else:
                b.append(ch)
        a.append(b)

    a = lab_print_gen(gen_map, a)

    a[a0 * 2 + 1][b0 * 2 + 1] = '0'
    a[m * 2 - 1][n * 2 - 1] = '*'
    ghost = False

    while True:
        for i in a:
            print(''.join(i))
        for i in gen_map:
            for j in i:
                print(j[2], end=" ")
        hod = input()
        if hod == 'w':
            x_d, y_d = x - 1, y
        elif hod == 'd':
            x_d, y_d = x, y + 1
        elif hod == 's':
            x_d, y_d = x + 1, y
        elif hod == 'a':
            x_d, y_d = x, y - 1
        elif hod == 'ghost':
            ghost = True
            hod = input()
            if hod == 'w':
                x_d, y_d = x - 1, y
            elif hod == 'd':
                x_d, y_d = x, y + 1
            elif hod == 's':
                x_d, y_d = x + 1, y
            elif hod == 'a':
                x_d, y_d = x, y - 1
        if not (ghost):
            if a[x_d][y_d] == '0':
                print('Победа')
                break
            elif a[x_d][y_d] == '#':
                pass
            else:
                a[x][y] = ' '
                x, y = x_d, y_d
                a[x][y] = '*'
        elif ghost:
            if a[x_d][y_d] == '0':
                print('Победа')
                break
            else:
                a = lab_print_gen(gen_map, a)
                a[x][y] = ' '
                x, y = x_d, y_d
                a[x][y] = '*'

        else:
            a = lab_print_gen(gen_map, a)
            a[x][y] = ' '
            x, y = x_d, y_d
            a[x][y] = '*'
    input()


if __name__ == '__main__':
    main()
