import numpy as np
from scipy.signal import find_peaks
from matplotlib import pyplot as plt
# I just felt like doing it with Numpy ¯\(ツ)/¯

FILENAME = 'input'

SIMULATED_ROCKS = 25_000
MAX_ROCKS = 1_000_000_000_000
PEAK_THRES = 1e-3

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
        self.height_history = None

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

        self.height_history = np.zeros((max_rocks,))

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
                        self.height_history[stopped_rocks] = self.chamber.shape[0] - self.get_highest_y() + self.saved_height

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
cave.simulate(SIMULATED_ROCKS)
cave.print_chamber()

height = cave.chamber.shape[0] - cave.get_highest_y() + cave.saved_height
print(f'The tower is {height} units tall.')

# A pattern can be seen here - when does it start?
# plt.figure()
# plt.stem(np.arange(1,cave.height_history.size+1),cave.height_history)
# plt.ylabel('Height')
# plt.xlabel('Rocks')

height_increment = np.diff(cave.height_history)

# Now, here it is obvious. I need to detect the transient and the period.
# plt.figure()
# plt.stem(np.arange(1,cave.height_history.size), height_increment)
# plt.ylabel('Height increment')
# plt.xlabel('Rocks')

height_increment_ft = np.fft.fft(height_increment)/height_increment.size
height_increment_ft_mag = np.abs(height_increment_ft)
peak_positions, properties = find_peaks(height_increment_ft_mag, height=PEAK_THRES)
freq_axis = np.arange(0,height_increment.size)*2*np.pi/height_increment.size
print('DEBUG')
print(height_increment.size, height_increment_ft.size, freq_axis.size)

# For a sufficiently long simulation, this is approx. the Fourier Series of the
# signal. The spacing gives the frequency/period.
plt.figure()
plt.plot(freq_axis, height_increment_ft_mag)
plt.plot(freq_axis[peak_positions], height_increment_ft_mag[peak_positions], 'o')
plt.ylabel('DFT[Height increment]')
plt.xlabel('Discrete frequency')

df = np.diff(freq_axis[peak_positions])
N_array = 2*np.pi/df
plt.figure()
plt.plot(N_array, 'o')
plt.show()
N_array_ = np.delete(N_array, N_array < 1_000)
N_= np.rint(np.mean(N_array))
N = 1740 # It's between 1739 and 1742 - rounding errors prevent me from calculating the good one
print(f'Freq. spacing = {df}')
print(f'Period = {N}')

# Now, look for the transient
shift = 0
while shift < height_increment.size - N:
    if np.all(height_increment[shift:shift+N] == height_increment[shift+N:shift+2*N]):
        break
    shift += 1

print(f'Transient length = {shift}')

# And finally, the solution to the challenge:
rocks_in_pattern = MAX_ROCKS - shift
num_periods = rocks_in_pattern // N
remainder = rocks_in_pattern % N

height_transient = np.sum(height_increment[0:shift])
height_period = np.sum(height_increment[shift:shift+N])
height_remainder = np.sum(height_increment[shift:shift+remainder])

print(f'{height_transient = }')
print(f'{height_period = }')
print(f'{height_remainder = }')

solution = height_transient + num_periods*height_period + height_remainder
print(f'Solution = {int(solution)}')
