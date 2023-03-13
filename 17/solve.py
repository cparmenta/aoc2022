import numpy as np
# I just felt like doing it with Numpy ¯\(ツ)/¯

FILENAME = 'input'


class Cave:
    def __init__(self, jet_pattern):
        self.shapes = [
            np.array([[2, 2, 2, 2]], ndmin=2, dtype=int),
            np.array([[0, 2, 0], [2, 2, 2], [0, 2, 0]], ndmin=2, dtype=int),
            np.array([[0, 0, 2], [0, 0, 2], [2, 2, 2]], ndmin=2, dtype=int),
            np.array([[2], [2], [2], [2]], ndmin=2, dtype=int),
            np.array([[2, 2], [2, 2]], ndmin=2, dtype=int)
        ]
        self.jet_pattern = jet_pattern
        self.chamber = np.full((4, 7), 0, dtype=int)
        self.saved_height = 0

    def print_chamber(self):
        cave_chars = {
            0: '.',
            1: '#',
            2: '@'
        }

        rows = self.chamber.shape[0]
        cols = self.chamber.shape[1]

        for i in range(rows):
            for j in range(cols):
                print(cave_chars[self.chamber[i,j]], end='')
            print()

    def simulate(self, max_rocks=None):

        i_shape = 0
        i_step = 0
        i_pattern = 0
        stopped_rocks = 0
        falling = False
        process_jet = True

        while stopped_rocks < max_rocks:
            if not falling:
                highest_point = self.get_highest_y()
                next_shape = self.shapes[i_shape]

                needed_cave_height =  (self.chamber.shape[0] - highest_point) + 3 + next_shape.shape[0]

                if needed_cave_height > self.chamber.shape[0]:
                    appended_height = needed_cave_height - self.chamber.shape[0]
                    appended_cave = np.zeros((appended_height, 7))
                    self.chamber = np.concatenate((appended_cave, self.chamber))
                elif needed_cave_height < self.chamber.shape[0]:
                    removed_height = self.chamber.shape[0] - needed_cave_height
                    self.chamber = np.delete(self.chamber, slice(removed_height), axis=0)

                self.chamber[0:next_shape.shape[0], 2:2+next_shape.shape[1]] = next_shape
                i_shape = (i_shape + 1) % len(self.shapes)
                falling = True
                # print(f'\nSTEP = {i_step}:')
                # self.print_chamber()
            else:
                I, J = np.nonzero(self.chamber == 2)
                if process_jet:
                    min_j = np.min(J)
                    if self.jet_pattern[i_pattern] == '>':
                        # Check wall
                        touches_wall = np.max(J) == (self.chamber.shape[1] - 1)
                        if not touches_wall:
                            # Check shape on right
                            touches_shape = False
                            for i, j in zip(I,J):
                                touches_shape = self.chamber[i,j+1] == 1
                                if touches_shape: break
                            if not touches_shape:
                                self.chamber[I,J] = 0
                                J += 1
                                self.chamber[I,J] = 2
                    elif self.jet_pattern[i_pattern] == '<':
                        touches_wall = np.min(J) == 0
                        if not touches_wall:
                            # Check shape on right
                            touches_shape = False
                            for i, j in zip(I,J):
                                touches_shape |= (self.chamber[i,j-1] == 1)
                                if touches_shape: break
                            if not touches_shape:
                                self.chamber[I,J] = 0
                                J -= 1
                                self.chamber[I,J] = 2
                    else:
                        print(f'THIS SHOULD NOT HAVE HAPPENED: {self.jet_pattern[i_pattern]}')
                        exit(1)
                    i_pattern = (i_pattern + 1) % len(self.jet_pattern)
                    process_jet = False
                else:
                    max_i = np.max(I)
                    touches_floor = (max_i == self.chamber.shape[0] - 1)
                    touches_shape = False

                    if not touches_floor:
                        for i,j in zip(I,J):
                            touches_shape |= (self.chamber[i+1,j] == 1)
                            if touches_shape: break

                    if not touches_floor and not touches_shape:
                            self.chamber[I,J] = 0
                            I += 1
                            self.chamber[I,J] = 2
                    else:
                        self.chamber[I,J] = 1
                        falling = False
                        stopped_rocks += 1
                        if (stopped_rocks % 1000) == 0: print(f'{stopped_rocks = }')
                        while self.check_lastline_blocked():
                            self.chamber = np.delete(self.chamber, self.chamber.shape[0]-1, axis=0)
                            self.saved_height += 1
                        # print(f'\nSTEP = {i_step}:')
                        # self.print_chamber()
                    process_jet = True

            i_step += 1

    def get_highest_y(self):
        I, J = np.nonzero(self.chamber == 1)
        if I.size > 0:
            return np.min(I)
        else:
            return self.chamber.shape[0]

    def check_lastline_blocked(self):
        line_is_blocked = True
        for j in range(7):
            current_is_blocked = False
            for i in reversed(range(self.chamber.shape[0])):
                current_is_blocked |= (self.chamber[i,j] != 0)
                if current_is_blocked: break
            line_is_blocked &= current_is_blocked
            if not line_is_blocked: break
        return line_is_blocked

with open(FILENAME) as file:
    jet_pattern = file.readline()
    jet_pattern = jet_pattern[:-1]  # Remove \n


cave = Cave(jet_pattern)
cave.print_chamber()
cave.simulate(1_000_000_000_000)
cave.print_chamber()

height = cave.chamber.shape[0] - cave.get_highest_y() + cave.saved_height
print(f'The tower is {height} units tall.')
