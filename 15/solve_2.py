# PART 2
import re
import time

start_time = time.time()

FILENAME = 'input'
ROW = 2_000_000
MAX = 4_000_000

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

min_x = 0
max_x = MAX
min_y = 0
max_y = MAX

# Find max distances and expand map
max_distances = []
for sensor, beacon in zip(sensors, beacons):
    d = manhattan_distance(sensor, beacon)
    max_distances.append(d)
    # right = sensor[0] + d
    # left  = sensor[0] - d
    # up    = sensor[1] + d
    # down  = sensor[1] - d
    # if  left < min_x: min_x = left
    # if right > max_x: max_x = right
    # if  down < min_y: min_y = down
    # if    up < max_y: max_y = up

def point_in_range(point, min_x, max_x, min_y, max_y):
    return min_x <= point[0] <= max_x and min_y <= point[1] <= max_y

def check_point(point, current_sensor, sensors, beacons, max_distances):
    point_empty = True
    for _sensor, _max_distance, _i in zip(sensors, max_distances, range(len(sensors))):
        print(f'    sensor {_i+1}/{len(sensors)} checked')
        if _sensor != current_sensor:
            point_empty &= manhattan_distance(_sensor, point) > _max_distance
            if not point_empty: break
    return point_empty

def print_found(solution):
    print(f'point: {solution}')
    print(f'Solution = {4_000_000 * solution[0] + solution[1]}.')
    end_time = time.time()
    print(f'Elapsed time: {end_time - start_time}')
    exit(0)

for sensor, max_distance, i in zip(sensors, max_distances, range(len(sensors))):
    point = [sensor[0], sensor[1] + max_distance + 1]
    print(f'Rounding sensor {i+1}/{len(sensors)}:')
    # Navigate from N to E clockwise
    while point[1] > sensor[1]:
        print(f'  {point[1] - sensor[1]} points left')
        if point_in_range(point, min_x, max_x, min_y, max_y) and check_point(point, sensor, sensors, beacons, max_distances):
            print_found(point)
        point[0] += 1
        point[1] -= 1
    print(1)
    # Navigate from E to S clockwise
    while point[0] > sensor[0]:
        print(f'  {point[0] - sensor[0]} points left')
        if point_in_range(point, min_x, max_x, min_y, max_y) and point_in_range(point, min_x, max_x, min_y, max_y) and check_point(point, sensor, sensors, beacons, max_distances):
            print_found(point)
        point[0] -= 1
        point[1] -= 1
    print(2)
    # Navigate from S to W clockwise
    while point[1] < sensor[1]:
        print(f'  {sensor[1] - point[1]} points left')
        if point_in_range(point, min_x, max_x, min_y, max_y) and check_point(point, sensor, sensors, beacons, max_distances):
            print_found(point)
        point[0] -= 1
        point[1] += 1
    print(3)
    # Navigate from W to N clockwise
    while point[0] < sensor[0]:
        print(f'  {sensor[0] - point[0]} points left')
        if point_in_range(point, min_x, max_x, min_y, max_y) and check_point(point, sensor, sensors, beacons, max_distances):
            print_found(point)
        point[0] += 1
        point[1] += 1
    print(4)

print('SOLUTION NOT FOUND :(')
