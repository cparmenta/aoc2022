import re
from graph import *
from time import time

FILENAME = 'input'
TOTAL_TIME_1 = 30
TOTAL_TIME_2 = 26


def print_elapsed_time(text, start, end):
    elapsed_time = end - start
    print(f'{text} - Elapsed time: {elapsed_time // 3600 % 60:.0f} h {elapsed_time// 60 % 60:.0f} min {elapsed_time % 60:.2f} s')

if __name__ == '__main__':
    # Apparently code needs to be guarded in main clause for Futures multiproc.
    nodes = {}

    with open(FILENAME) as file:
        line = file.readline()
        while line != '':
            sline = line.split(); sline[-1] += ' '
            node_name = sline[1]
            flow_rate = int(sline[4][5:-1])
            children = [s[:-1] for s in sline[9:]]
            nodes[node_name] = Node(node_name, flow_rate, children)

            line = file.readline()

    start_time = time()
    map = Graph(nodes)
    maximum_release = map.explore_recursive('AA', TOTAL_TIME_1, [], 0)
    end_time = time()

    print(f'Part 1 (Recursive Dynamic Programming) - {maximum_release = }')
    print_elapsed_time('Part 1 (rdp)', start_time, end_time)

    start_time = time()
    map = Graph(nodes)
    map.calculate_distances()
    maximum_release = map.explore_simplified_recursive(minutes_left=TOTAL_TIME_1)
    end_time = time()
    print(f'Part 1 - (Simplified RDP) {maximum_release = }')
    print_elapsed_time('Part 1 (srdp)', start_time, end_time)

    start_time = time()
    map = Graph(nodes)
    maximum_release = map.explore_with_help(minutes_left=TOTAL_TIME_2)
    end_time = time()
    print(f'Part 2 - (Simplified RDP with help) {maximum_release = }')
    print_elapsed_time('Part 2 (srdp w/help)', start_time, end_time)
