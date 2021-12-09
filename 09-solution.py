from queue import Queue

import numpy as np

lines = []
with open("09-input.txt") as file:
    for line in file.readlines():
        line = [int(d) for d in line.strip()]
        lines.append(line)

basin: np.ndarray = np.array(lines)


def get_neighbour_values(arr, i, j):
    dim = basin.shape
    neighbours = []
    if i > 0:
        neighbours.append(arr[i-1, j])
    if i < dim[0]-1:
        neighbours.append(arr[i+1, j])
    if j > 0:
        neighbours.append(arr[i, j-1])
    if j < dim[1]-1:
        neighbours.append(arr[i, j+1])
    return neighbours


def get_neighbour_indices(arr, i, j):
    dim = basin.shape
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


low_points = []
for i in range(basin.shape[0]):
    for j in range(basin.shape[1]):
        neighbours = get_neighbour_values(basin, i, j)
        value = basin[i, j]
        if all(map(lambda x: x > value, neighbours)):
            low_points.append(value+1)

print("Solution part 1:")
print(sum(low_points))

visited = set()

def get_basin_size(arr, i, j):
    to_visit = Queue()
    to_visit.put((i, j))

    size = 0
    while not to_visit.empty():
        y, x = to_visit.get()
        if (y, x) in visited or arr[y, x] == 9:
            continue
        visited.add((y, x))
        size += 1

        neighbours = get_neighbour_indices(arr, y, x)
        for neighbour in neighbours:
            if neighbour not in visited:
                to_visit.put(neighbour)

    return size



sub_basin_sizes = []
for i in range(basin.shape[0]):
    for j in range(basin.shape[1]):
        if (i, j) in visited or basin[i, j] == 9:
            continue

        sub_basin_sizes.append(get_basin_size(basin, i, j))

print("Solution part 2:")
print(np.prod(sorted(sub_basin_sizes)[-3:]))



