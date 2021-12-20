import numpy as np


with open("20-input.txt", "r") as f:
    rules = f.readline().strip()
    rules = [0 if char == "." else 1 for char in rules.strip()]
    f.readline()

    image_data = []
    for line in f.readlines():
        image_data.append([0 if char == "." else 1 for char in line.strip()])

    image_data = np.array(image_data)
    image_data = np.pad(image_data, ((10, 10), (10, 10)))


def area_to_dec(array):
    return int("".join(map(str, array.flatten())), 2)


def transform(array: np.array, rules, parity):
    n, m = array.shape
    tranformed = np.copy(array)
    for i in range(1, n-1):
        for j in range(1, m-1):
            area = array[i-1:i+2, j-1:j+2]
            index = area_to_dec(area)
            tranformed[i, j] = rules[index]

    edge_index = 0 if parity % 2 == 0 else 511
    tranformed[0, 0:m] = rules[edge_index]
    tranformed[n-1, 0:m] = rules[edge_index]
    tranformed[0:n, 0] = rules[edge_index]
    tranformed[0:n, m-1] = rules[edge_index]
    return tranformed


def show_image(array):
    for row in array:
        for col in row:
            print("." if col == 0 else "#", end="")
        print()


image_data = transform(image_data, rules, 0)
image_data = transform(image_data, rules, 1)

print("Solution part 1:")
print(np.sum(image_data))

