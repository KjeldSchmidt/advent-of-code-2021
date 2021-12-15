from collections import defaultdict

import numpy as np

lines = []
with open("15-input.txt") as f:
    for line in f.readlines():
        line = line.strip()
        line = map(int, line)
        lines.append(list(line))

cave = np.array(lines)


def get_neighbour_indices(arr, i, j):
    dim = arr.shape
    neighbours = []
    if i > 0:
        neighbours.append((i-1, j))
    if i < dim[0]-1:
        neighbours.append((i+1, j))
    if j > 0:
        neighbours.append((i, j-1))
    if j < dim[1]-1:
        neighbours.append((i, j+1))
    return neighbours


def path_find(cave: np.ndarray):
    path_cost = np.ones(cave.shape) * np.infty
    visited = np.zeros(cave.shape)
    path_cost[0, 0] = 0
    i, j = 0, 0
    while True:
        neighbours = get_neighbour_indices(path_cost, i, j)
        for y, x in neighbours:
            old_cost = path_cost[y, x]
            new_cost = path_cost[i, j] + cave[y, x]
            if new_cost < old_cost:
                path_cost[y, x] = new_cost

        visited[i, j] = 1

        if visited[visited.shape[0] - 1, visited.shape[1] - 1] == 1:
            break

        candidate_nodes = np.copy(path_cost)
        candidate_nodes[np.where(visited == 1)] = np.infty
        i, j = np.argwhere(candidate_nodes == np.min(candidate_nodes))[0]

    return path_cost[path_cost.shape[0] - 1, path_cost.shape[1] - 1]


def path_find_fast(cave: np.ndarray):

    def h(i, j):
        return np.abs(j-i) * 5

    open_set = {(0, 0)}
    came_from = {}

    path_cost = np.ones(cave.shape) * np.infty
    visited = np.zeros(cave.shape)
    path_cost[0, 0] = 0

    estimated_path_cost = defaultdict(lambda: np.infty)
    estimated_path_cost[(0, 0)] = h(0, 0)

    while len(open_set) != 0:
        min_f_score = np.infty
        current = None
        for node in open_set:
            if estimated_path_cost[node] < min_f_score:
                min_f_score = estimated_path_cost[node]
                current = node

        if current == (cave.shape[0] - 1, cave.shape[1] -1):
            return path_cost[current]

        open_set.remove(current)
        i, j = current


        neighbours = get_neighbour_indices(path_cost, i, j)
        for y, x in neighbours:
            t_path_cost = path_cost[current] + cave[y, x]
            if t_path_cost < path_cost[y, x]:
                came_from[(y, x)] = current
                path_cost[y, x] = t_path_cost
                estimated_path_cost[(y, x)] = t_path_cost + h(y, x)
                open_set.add((y, x))

    raise Exception("No more candiate paths, but goal not reached")

print("Solution Part 1:")
print(int(path_find_fast(cave)))


larger_cave = np.zeros((cave.shape[0] * 5, cave.shape[1] * 5))

for i in range(0, larger_cave.shape[0], cave.shape[0]):
    for j in range(0, larger_cave.shape[1], cave.shape[1]):
        mod_cave = (cave + i / cave.shape[0] + j / cave.shape[1]) % 10
        mod_cave[mod_cave < cave] += 1
        larger_cave[i:i + cave.shape[0], j:j + cave.shape[0]] = mod_cave


print("Solution Part 2:")
print(int(path_find_fast(larger_cave)))

