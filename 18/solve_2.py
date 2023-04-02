import numpy as np
from matplotlib import pyplot as plt
from matplotlib.widgets import Slider
import sys
sys.setrecursionlimit(1_000_000)

FILENAME = 'input'


class Cell:
    def __init__(self, filename):
        coordinates = []
        with open(filename) as f:
            line = f.readline()
            while line != '':
                numbers_str = line.split(',')
                numbers = [int(x) for x in numbers_str]
                coordinates.append(numbers)
                line = f.readline()

        self.coordinates = np.array(coordinates, dtype=int)
        cell_shape = np.max(coordinates, axis=0) + 1
        self.cell = np.full(cell_shape, False)
        self.cell_water = np.full(cell_shape, False)
        self.total_surface = 0

    def count_droplets_around(self, x, y, z):
        shape = self.cell.shape
        droplets_around = 0

        # x axis
        if x > 0 and self.cell[x-1, y, z]:
            droplets_around += 1
        if x < shape[0]-1 and self.cell[x+1, y, z]:
            droplets_around += 1
        # y axis
        if y > 0 and self.cell[x, y-1, z]:
            droplets_around += 1
        if y < shape[1]-1 and self.cell[x, y+1, z]:
            droplets_around += 1
        # z axis
        if z > 0 and self.cell[x, y, z-1]:
            droplets_around += 1
        if z < shape[2]-1 and self.cell[x, y, z+1]:
            droplets_around += 1

        return droplets_around

    def render_map(self):
        for i in range(self.coordinates.shape[0]):
            current_coordinates = self.coordinates[i,:]
            x = current_coordinates[0]
            y = current_coordinates[1]
            z = current_coordinates[2]
            self.cell[x,y,z] = True
            droplets_around = self.count_droplets_around(x, y, z)
            self.total_surface += 6 - 2*droplets_around
            print(f'On ({x+1},{y+1},{z+1}), {droplets_around} droplets around - surface = {self.total_surface}')
        return self.total_surface

    def flood(self, x=0, y=0, z=0):
        self.cell_water[x,y,z] = True
        if x > 0 and not self.cell[x-1, y, z] and not self.cell_water[x-1, y, z]:
            self.flood(x-1, y, z)
        if x < self.cell.shape[0]-1 and not self.cell[x+1, y, z] and not self.cell_water[x+1, y, z]:
            self.flood(x+1, y, z)
        if y > 0 and not self.cell[x, y-1, z] and not self.cell_water[x, y-1, z]:
            self.flood(x, y-1, z)
        if y < self.cell.shape[1]-1 and not self.cell[x, y+1, z] and not self.cell_water[x, y+1, z]:
            self.flood(x, y+1, z)
        if z > 0 and not self.cell[x, y, z-1] and not self.cell_water[x, y, z-1]:
            self.flood(x, y, z-1)
        if z < self.cell.shape[2]-1 and not self.cell[x, y, z+1] and not self.cell_water[x, y, z+1]:
            self.flood(x, y, z+1)

    def calculate_corrected_surface(self):
        corrected_surface = self.total_surface
        locations = np.argwhere(np.logical_not(np.logical_or(self.cell, self.cell_water)))

        for i in range(locations.shape[0]):
            corrected_surface -= self.count_droplets_around(locations[i,0],
                                                            locations[i,1],
                                                            locations[i,2])

        return corrected_surface


cell = Cell(FILENAME)
print(f'Part 1: {cell.render_map()}')
print(cell.cell.shape)
cell.flood()
print(f'Part 2: {cell.calculate_corrected_surface()}')

# The following plot shows cavities inside...
plt.ion()
fig, ax = plt.subplots()
fig.subplots_adjust(bottom=0.25)
ax.pcolor(cell.cell[:,:,0])
plt.show()

def update(val):
    ax.clear()
    ax.pcolor(cell.cell[:,:,int(val)])
    fig.canvas.draw_idle()

axsld = fig.add_axes([0.25, 0.1, 0.65, 0.03])
slider = Slider(
    ax=axsld,
    label="z",
    valmin=0,
    valmax=cell.cell.shape[2]-1,
    valstep=1,
    valinit=0,
    orientation="horizontal",
    color="green"
)
slider.on_changed(update)
