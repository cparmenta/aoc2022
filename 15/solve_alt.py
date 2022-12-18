# A FASTER SOLUTION
import re

FILENAME = 'input' # 'input'
ROW = 2_000_000

def manhattan_distance(p1, p2):
    return abs(p2[0] - p1[0]) + abs(p2[1] - p1[1])

sensors = []
beacons = []
with open(FILENAME) as file:
    line = file.readline()
    while line != '':
        coords = [int(i) for i in re.findall(r'-?\d+', line)]
        sensors.append((coords[0], coords[1]))
        beacons.append((coords[2], coords[3]))

        line = file.readline()


x = [p[0] for p in sensors + beacons]
y = [p[1] for p in sensors + beacons]

min_x = min(x)
max_x = max(x)
min_y = min(y)
max_y = max(y)

# Find max distances and expand map
max_distances = []
for sensor, beacon in zip(sensors, beacons):
    d = manhattan_distance(sensor, beacon)
    max_distances.append(d)
    right = sensor[0] + d
    left  = sensor[0] - d
    up    = sensor[1] + d
    down  = sensor[1] - d
    if  left < min_x: min_x = left
    if right > max_x: max_x = right
    if  down < min_y: min_y = down
    if    up < max_y: max_y = up

# print(min_x, max_x, min_y, max_y)

cant_positions = set()
total_x = max_x - min_x + 1
for sensor, beacon, max_distance, i in zip(sensors, beacons, max_distances, range(len(sensors))):
    dy = abs(ROW - sensor[1])
    dx = max_distance - dy
    if dx > 0:
        update_set = {x for x in range(sensor[0]-dx, sensor[0]+dx+1) if (x, ROW) not in beacons}
        cant_positions.update(update_set)
    print(f'{i}/{len(sensors)}')

print(f'Cannot be in {len(cant_positions)} positions.')
