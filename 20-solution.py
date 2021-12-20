import numpy as np


with open("20-input-small.txt", "r") as f:
    rules = f.readline().strip()
    rules = [0 if char == "." else 1 for char in rules.strip()]
    f.readline()

    image_data = []
    for line in f.readlines():
        image_data.append([0 if char == "." else 1 for char in line.strip()])

    image_data = np.array(image_data)


def area_to_dec(array):
    return int("".join(map(str, array.flatten())), 2)


def transform(array: np.array, rules):
    padded = np.pad(array, ((2, 2), (2, 2)))
    n, m = padded.shape

    tranformed = np.copy(padded)
    for i in range(1, n-1):
        for j in range(1, m-1):
            area = padded[i-1:i+2, j-1:j+2]
            index = area_to_dec(area)
            tranformed[i, j] = rules[index]

    return tranformed[1:-1, 1:-1]


def show_image(array):
    for row in array:
        for col in row:
            print("." if col == 0 else "#", end="")
        print()


show_image(image_data)
image_data = transform(image_data, rules)

print()
show_image(image_data)
image_data = transform(image_data, rules)

print()
show_image(image_data)

print("Solution part 1:")
print(np.sum(image_data))

