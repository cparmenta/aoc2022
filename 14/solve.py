import numpy as np

FILENAME = 'example'
EMPTY = '.' # ' '
ROCK = '#' # '█'
SAND = 'o' #'▒'
START = '⌧'

START_POINT = (500, 0)

def print_array(array):
    for i in range(array.shape[0]):
        for j in range(array.shape[1]):
            print(array[i,j], end='')
        print()

def coords2array(coords):
    list_x = [p[0] for p in coords]
    list_y = [p[1] for p in coords]
    _min_x = min(list_x)
    _max_x = max(list_x)
    _min_y = min(list_y)
    _max_y = max(list_y)
    coord_range = (_min_x, _max_x, _min_y, _max_y)

    shape = (_max_y - _min_y + 1, _max_x - _min_x + 1)
    array = np.full(shape, fill_value=EMPTY, dtype=np.str_)

    for i in range(len(coords) - 1):
        if coords[i][1] == coords[i+1][1]:
            if coords[i][0] <= coords[i+1][0]:
                ix_ini = coords[i][0] - _min_x
                ix_end = coords[i+1][0] - _min_x + 1
            else:
                ix_end = coords[i][0] - _min_x + 1
                ix_ini = coords[i+1][0] - _min_x
            iy = coords[i+1][1] - _min_y
            array[iy, ix_ini:ix_end] = ROCK
        elif coords[i][0] == coords[i+1][0]:
            if coords[i][1] <= coords[i+1][1    ]:
                iy_ini = coords[i][1] - _min_y
                iy_end = coords[i+1][1] - _min_y + 1
            else:
                iy_end = coords[i][1] - _min_y + 1
                iy_ini = coords[i+1][1] - _min_y
            ix = coords[i+1][0] - _min_x
            array[iy_ini:iy_end, ix] = ROCK
    return coord_range, array

def merge_arrays(array1, range1, array2, range2):
    _min_x = min(range1[0], range2[0])
    _max_x = max(range1[1], range2[1])
    _min_y = min(range1[2], range2[2])
    _max_y = max(range1[3], range2[3])
    coord_range = (_min_x, _max_x, _min_y, _max_y)

    new_shape = (_max_y - _min_y + 1, _max_x - _min_x + 1)
    new_array_b = np.full(new_shape, fill_value=False, dtype=np.bool8)
    new_array = np.full(new_shape, fill_value=EMPTY, dtype=np.str_)

    new_array_b[
        range1[2] - _min_y : range1[3] - _min_y + 1,
        range1[0] - _min_x : range1[1] - _min_x + 1,
    ] |= (array1 == ROCK)

    new_array_b[
        range2[2] - _min_y : range2[3] - _min_y + 1,
        range2[0] - _min_x : range2[1] - _min_x + 1,
    ] |= (array2 == ROCK)

    new_array[new_array_b] = ROCK

    return coord_range, new_array

def in_bounds(coord_range, point):
    return coord_range[0] <= point[0] <= coord_range[1] \
           and coord_range[2] <= point[1] <= coord_range[3]

def in_bounds_bare(shape, point):
    return 0 <= point[0] < shape[0] \
           and 0 <= point[1] < shape[1]

def find_fall_point(cave, start):
    i_row = start[0]
    i_col = start[1]
    while 0 <= i_row < cave.shape[0] \
      and 0 <= i_col < cave.shape[1]:
        if cave[i_row, i_col] in (SAND, ROCK):
            if i_col > 0 and cave[i_row, i_col-1] == EMPTY:
                i_col -= 1
                #i_row -= 1
                continue
                #return (i_row, i_col)
            elif i_col == 0:
                return (i_row, i_col - 1)
            elif i_col < cave.shape[1] - 1 and cave[i_row, i_col+1] == EMPTY:
                #i_row -= 1
                i_col += 1
                continue
                #return (i_row, i_col)
            elif i_col == cave.shape[1] - 1:
                return (i_row, i_col + 1)
            else:
                break
        i_row += 1
    if i_row == cave.shape[0]:
        return (i_row, i_col)
    return (i_row - 1, i_col)


# Parse file and convert to array
with open(FILENAME) as file:
    line = file.readline()
    previous_array = None
    previous_range = None
    while line != '':
        coords = [eval(p) for p in line.split(sep='->')]
        coord_range, cave = coords2array(coords)
        print(coord_range)
        print_array(cave)
        if previous_array is not None:
            coord_range, cave = merge_arrays(previous_array, previous_range, cave, coord_range)

        previous_array = cave
        previous_range = coord_range

        line = file.readline()

# Include coord y=0
coord_range, cave = merge_arrays(np.array([['.', '.'],['.', '.']]), (START_POINT[0], START_POINT[0]+1, START_POINT[1], START_POINT[1]+1), cave, coord_range)


ix_start = max(0, START_POINT[0]-coord_range[0])
iy_start = max(0, START_POINT[1]-coord_range[2])
start_bare = (iy_start, ix_start)

cave[iy_start, ix_start] = START
coord_range_bare = (0, cave.shape[0]-1, 0, cave.shape[1]-1)
print(coord_range)
print_array(cave)


# Simulate sand flow
point = find_fall_point(cave, start_bare)
step = 0
while in_bounds_bare(cave.shape, point):
    cave[point] = SAND
    point = find_fall_point(cave, start_bare)
    step += 1

print(f'\n{step=}')
print_array(cave)
