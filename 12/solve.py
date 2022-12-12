import numpy as np
import itertools
from collections import deque
from time import sleep
from matplotlib import pyplot as plt

FILENAME = 'input'
PLOT_EVERY = 100

def can_jump(current_level, next_level):
    return next_level - 1 <= current_level

def get_neighbors(levels, pos):
    neighbors = []
    shape = levels.shape
    current_level = levels[pos]
    if pos[0] > 0: # up
        next_level = levels[pos[0] - 1, pos[1]]
        if can_jump(current_level, next_level):
            neighbors.append((pos[0] - 1, pos[1]))
    if pos[0] < shape[0] - 1: # down
        next_level = levels[pos[0] + 1, pos[1]]
        if can_jump(current_level, next_level):
            neighbors.append((pos[0] + 1, pos[1]))
    if pos[1] > 0: # left
        next_level = levels[pos[0], pos[1] - 1]
        if can_jump(current_level, next_level):
            neighbors.append((pos[0], pos[1] - 1))
    if pos[1] < shape[1] - 1: # Right
        next_level = levels[pos[0], pos[1] + 1]
        if can_jump(current_level, next_level):
            neighbors.append((pos[0], pos[1] + 1))
    return neighbors

def get_uncompleted_neighbors(neighbors, completed_matrix):
    return [neighbor for neighbor in neighbors if not completed_matrix[neighbor]]

plt.ion()
plt.figure()
plt.show()
i_plot = 0
def update_plot(force=False):
    global i_plot
    if i_plot < PLOT_EVERY and not force:
        i_plot += 1
    else:
        i_plot = 0
        plt.clf()
        plt.pcolor(np.flipud(cum_path_matrix), cmap='jet')
        plt.colorbar()
        plt.text(S_pos[1], cum_path_matrix.shape[0] - S_pos[0] - 1, 'S', color='red')
        plt.text(E_pos[1], cum_path_matrix.shape[0] - E_pos[0] - 1, 'E', color='white')
        plt.title(f'Min. distance = {int(cum_path_matrix[E_pos]) if cum_path_matrix[E_pos] != np.inf else "inf"}')
        plt.gcf().canvas.draw()
        plt.gcf().canvas.flush_events()

with open(FILENAME) as file:
    lines = file.readlines()
    lines = [line[:-1] for line in lines] # Remove \n

rows = len(lines)
cols = len(lines[0])

level_matrix = np.zeros((rows,cols))
cum_path_matrix = np.full((rows,cols), np.inf)
completed_matrix = np.full((rows, cols), False)

S_pos = None
E_pos = None

for i, j in itertools.product(range(rows), range(cols)):
    letter = lines[i][j]
    if letter == 'S':
        S_pos = (i, j)
        letter = 'a'
    elif letter == 'E':
        E_pos = (i, j)
        letter = 'z'
    level_matrix[i, j] = ord(letter) - ord('a')

current_pos = S_pos
neighbors = get_neighbors(level_matrix, current_pos)
cum_path_matrix[S_pos] = 0
uncompleted_nodes = deque()
uncompleted_neighbors = get_uncompleted_neighbors(neighbors, completed_matrix)

while uncompleted_neighbors or uncompleted_nodes:
    for neighbor in neighbors:
        cum_path = cum_path_matrix[current_pos]
        if cum_path + 1 < cum_path_matrix[neighbor]:
            cum_path_matrix[neighbor] = cum_path + 1
            completed_matrix[neighbor] = False

    uncompleted_neighbors = get_uncompleted_neighbors(neighbors, completed_matrix)
    completed_matrix[current_pos] = True

    if len(uncompleted_neighbors) > 1:
        uncompleted_nodes += uncompleted_neighbors[1:]
        current_pos = uncompleted_neighbors[0]
    elif len(uncompleted_neighbors) == 1:
        current_pos = uncompleted_neighbors[0]
    elif uncompleted_nodes:
        current_pos = uncompleted_nodes.pop()

    neighbors = get_neighbors(level_matrix, current_pos)
    uncompleted_neighbors = get_uncompleted_neighbors(neighbors, completed_matrix)
    update_plot()
    print(f'Processing... {100*completed_matrix.nonzero()[0].size/completed_matrix.size:.2f} % completed')

update_plot(True)
print(f'Length of shortest path: {int(cum_path_matrix[E_pos])}')
wait = input("Press Enter to continue.")
