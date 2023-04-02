import numpy as np
from matplotlib import pyplot as plt
from matplotlib.widgets import Slider

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


cell = Cell(FILENAME)
print(f' Part 1: {cell.render_map()}')
