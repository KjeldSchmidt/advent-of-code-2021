import numpy as np

energy_levels = np.array([
    [2, 5, 6, 6, 8, 8, 5, 4, 3, 2],
    [3, 8, 5, 7, 4, 1, 4, 3, 5, 7],
    [6, 7, 6, 1, 5, 4, 3, 2, 4, 7],
    [5, 4, 7, 7, 3, 3, 2, 1, 1, 4],
    [3, 7, 3, 1, 5, 8, 5, 3, 8, 5],
    [1, 7, 1, 6, 7, 8, 3, 1, 7, 3],
    [1, 2, 7, 7, 3, 2, 1, 6, 1, 2],
    [3, 3, 7, 1, 1, 7, 6, 1, 4, 8],
    [1, 1, 6, 2, 5, 7, 8, 2, 8, 5],
    [6, 1, 4, 4, 7, 2, 6, 3, 6, 7]
])

n = 10


def step(arr: np.ndarray):
    flashed = np.zeros(arr.shape)
    arr = arr + 1

    while True:
        new_flashed = False
        flashing = np.argwhere(arr > 9)
        for flasher in flashing:
            i, j = flasher[0], flasher[1]

            if flashed[i, j] == 1:
                continue

            new_flashed = True

            arr[max(0, i-1):min(n, i+2), max(0, j-1):min(n, j+2)] += 1
            flashed[i, j] = 1

        if not new_flashed:
            break

    arr[arr > 9] = 0
    return arr, int(np.sum(flashed))


energy_levels_1 = energy_levels

total_flashes = 0
for i in range(100):
    energy_levels_1, flashes = step(energy_levels_1)
    total_flashes += flashes

print("Solution part 1:")
print(total_flashes)

energy_levels_2 = energy_levels

i = 0
while True:
    energy_levels_2, flashes = step(energy_levels_2)
    i += 1
    if flashes == 100:
        print("Solution part 2:")
        print(i)
        break
