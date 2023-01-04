"""
TIL: https://en.wikipedia.org/wiki/Dynamic_programming
Top-down approach: This is the direct fall-out of the recursive formulation of
any problem. If the solution to any problem can be formulated recursively using
the solution to its sub-problems, and if its sub-problems are overlapping, then
one can easily memoize or store the solutions to the sub-problems in a table.
Whenever we attempt to solve a new sub-problem, we first check the table to see
if it is already solved. If a solution has been recorded, we can use it direct-
ly, otherwise we solve the sub-problem and add its solution to the table.
"""
from dataclasses import dataclass
from itertools import combinations
from math import factorial
from concurrent.futures import ProcessPoolExecutor, wait


def opened2str(opened):
    s = ''
    for c in sorted(opened):
        s += c
    return s


@dataclass
class Node:
    name: str
    flow_rate: int
    children: list


class Graph:
    def __init__(self, nodes):
        self.nodes = nodes
        self.subpaths_done = [{}, {}]
        self.non_broken_nodes = {k:v for (k,v) in nodes.items() if v.flow_rate > 0 or k == 'AA'}
        self.non_broken_distances = None

    def explore_recursive(self, start_node, minutes_left, opened, id=0):
        # Early returns
        if minutes_left <= 0:
            return 0
        sp_key = (start_node, minutes_left, opened2str(opened))
        if sp_key in self.subpaths_done[id]:
            return self.subpaths_done[id][sp_key]

        # Without opening
        no_opening = max([
        self.explore_recursive(child, minutes_left-1, opened)
        for child in self.nodes[start_node].children
        ])
        # Opening
        opening = 0
        if self.nodes[start_node].flow_rate > 0 and start_node not in opened:
            current_release = self.nodes[start_node].flow_rate * (minutes_left - 1)
            opening = max([
                self.explore_recursive(child, minutes_left-2, opened + [start_node])
                for child in self.nodes[start_node].children
            ])
            opening += current_release

        best = max(opening, no_opening)
        self.subpaths_done[id][sp_key] = best
        return best

    def explore_simplified(self, start_node, minutes_left, id=0):
        def print_progress(current, total):
            text = f'Trying... ({current}/{total})'
            print(text, end='')
            for i in range(len(text)): print('\r', end='')

        non_broken_nodenames = [nodename for nodename in self.non_broken_nodes if nodename != 'AA']
        num_nodes = len(non_broken_nodenames)
        if self.non_broken_distances is None:
            self.calculate_distances()

        best_release = 0
        perms = permutations(non_broken_nodenames)
        count = 0
        total = factorial(len(non_broken_nodenames))
        for sequence in perms:
            current_minutes_left = minutes_left
            current_release = 0
            releases_track = [0 for j in range(num_nodes)]
            minutes_track = [0 for j in range(num_nodes)]
            i = 0
            while current_minutes_left > 0 and i < len(sequence):
                minutes_track[i] = current_minutes_left
                sp_key = (str(sequence[i:]), current_minutes_left)
                if sp_key in self.subpaths_done[id]:
                    current_release += self.subpaths_done[id][sp_key]
                    break
                else:
                    previous_node = 'AA' if i == 0 else sequence[i-1]
                    current_minutes_left -= self.non_broken_distances[previous_node][sequence[i]]
                    if current_minutes_left > 0:
                        current_minutes_left -= 1
                        releases_track[i] = self.non_broken_nodes[sequence[i]].flow_rate * current_minutes_left
                        current_release += releases_track[i]
                    i += 1
            # Register subpaths
            for j in range(num_nodes):
                if minutes_track[j] == 0: break
                sp_key = (str(sequence[j:]), minutes_track[j])
                if sp_key not in self.subpaths_done[id]:
                    self.subpaths_done[id][sp_key] = sum(releases_track[j:])
                    #print(f'DEBUG - Registered {sp_key} with release {self.subpaths_done[sp_key]}')

            count += 1
            print_progress(count, total)
            if current_release > best_release:
                best_release = current_release
                print(f'DEBUG - seq: {sequence} - curr: {current_release} - best: {best_release}')

    def explore_simplified_recursive(self, start_node='AA',  minutes_left=0, opened=[], nodes=None, id=0):
        # Early returns
        if minutes_left <= 0:
            return 0

        sp_key = (start_node, minutes_left, opened2str(opened))
        if sp_key in self.subpaths_done[id]:
            return self.subpaths_done[id][sp_key]

        next_opened = opened + [start_node]
        _nodes = nodes.copy() if nodes is not None else self.non_broken_nodes.keys()
        _nodes = [n for n in _nodes if n not in next_opened]

        # Open node
        open_time = 0 if start_node == 'AA' else 1

        this_release = (minutes_left - open_time) * self.nodes[start_node].flow_rate

        # Travel to every node
        best_release = 0
        for node in _nodes:
            release = self.explore_simplified_recursive(node,
                                              minutes_left - open_time - self.non_broken_distances[start_node][node],
                                              next_opened,
                                              _nodes)
            if release > best_release: best_release = release

        total_release = best_release + this_release

        # Register route and return
        self.subpaths_done[id][sp_key] = total_release
        return total_release

    def explore_with_help(self, start_node='AA', minutes_left=0):
        self.calculate_distances()
        nodes_to_explore = [n for n in self.non_broken_nodes.keys() if n != 'AA']
        best_release = 0
        N = len(nodes_to_explore)
        for k in range(N):
            print(f'{k = }, {N = }')
            for my_combination in combinations(nodes_to_explore, k):
                elephant_combination = [n for n in nodes_to_explore if n not in my_combination]

                self.subpaths_done = [{}, {}]

                # my_release = self.explore_simplified_recursive(start_node=start_node, minutes_left=minutes_left, nodes=list(my_combination), id=0)
                # elephant_release = self.explore_simplified_recursive(start_node=start_node, minutes_left=minutes_left, nodes=list(elephant_combination), id=1)

                with ProcessPoolExecutor() as executor:
                    my_release = executor.submit(self.explore_simplified_recursive, start_node=start_node, minutes_left=minutes_left, nodes=list(my_combination), id=0)
                    elephant_release = executor.submit(self.explore_simplified_recursive, start_node=start_node, minutes_left=minutes_left, nodes=list(elephant_combination), id=1)

                wait((my_release, elephant_release))

                total_release = my_release.result() + elephant_release.result()
                if total_release > best_release: best_release = total_release

        return best_release

    def calculate_distances(self):
        INF = 1_000_000_000
        # Initialize
        base_row = {k:INF for k in self.nodes}
        matrix = {k:base_row.copy() for k in self.nodes}
        for node in self.nodes:
            matrix[node][node] = 0
            for child in self.nodes[node].children:
                matrix[node][child] = 1
                matrix[child][node] = 1

        # Floyd-Warshall (https://en.wikipedia.org/wiki/Floyd%E2%80%93Warshall_algorithm)
        for k_node in self.nodes:
            for i_node in self.nodes:
                for j_node in self.nodes:
                    matrix[i_node][j_node] = min(
                        matrix[i_node][j_node],
                        matrix[i_node][k_node] + matrix[k_node][j_node]
                    )

        # Keep non broken nodes only
        self.non_broken_distances = {
            i_node:{
                j_node:matrix[i_node][j_node]
                for j_node in self.non_broken_nodes
            }
            for i_node in self.non_broken_nodes
        }

        return matrix

    def print_nodes(self):
        print(' === List of nodes ===')
        for k in self.nodes.keys():
            print(self.nodes[k])
        print(' =====================')

    def print_nbnodes(self):
        print(' === List of non broken nodes ===')
        for k in self.non_broken_nodes.keys():
            print(self.non_broken_nodes[k])
        print(' =====================')

    def print_subpaths(self, t=0):
        keys_t = [key for key in self.subpaths_done if key[1] == t]
        print(' === List of subpaths ===')
        for k in keys_t:
            print(k, self.subpaths_done[k])
        print(' =====================')
