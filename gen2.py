from random import choice


class Cell:
    """ Класс клетки """
    walls = ['up', 'right', 'left', 'down']
    dirs = ['up', 'right', 'left', 'down']              # Доступный направления
    visited = False


field = []
width, height = 5, 5

for i in range(height):
    temp = []
    for j in range(width):
        temp.append(Cell())
    field.append(temp)


x, y = 0, 0                                             # Начальные координаты
cells = []
cells.append([x, y])
i = 0
""" Основной цикл генерации """
while True:
    if len(cells) == 0:                                 # Если клеток в пути нет, то выйти из цикла
        break
    x, y = cells[-1]
    current_cell = field[x][y]                          # Выбираем клетку
    current_cell.visited = True
    dirs = current_cell.dirs
    if len(current_cell.dirs) == 0:                     # Если направлений не осталось
        cells.pop()                                     # то вернутся к прошлой клетке
        continue
    x_d, y_d = x, y
    dir = choice(current_cell.dirs)                     # Выборка доступных направлений
    dirm = ''
    if dir == 'up':
        x_d -= 1
        dirm = 'down'
    elif dir == 'down':
        x_d += 1
        dirm = 'up'
    elif dir == 'left':
        y_d -= 1
        dirm = 'right'
    elif dir == 'right':
        y_d += 1
        dirm = 'left'
    if not ((0 <= x_d < height) and (0 <= y_d < width)):    # Если выходит за ганицы
        current_cell.dirs.remove(dir)                   # то удалить это направление
        continue
    next_cell = field[x_d][y_d]                         # Слудующая клетка
    dirsm = next_cell.dirs
    if next_cell.visited:                               # Если следующая клетка посещённая
        current_cell.dirs.remove(dir)                   # то удалить это направление
        continue
    dirs.remove(dir)
    dirsm.remove(dirm)
    current_cell.walls = dirs                           # Удаляем
    next_cell.walls = dirsm                             # стены
    next_cell.dirs = dirsm                              # Удаляем у следующей клетки направление назад
    x, y = x_d, y_d
    cells.append([x, y])                                # Добавляем координаты клетки в путь
    i += 1
    print(i)
    print(dir)
    print(current_cell.walls)
    print(current_cell.dirs)
    print(next_cell.walls)
    print(next_cell.dirs)

print('End')
