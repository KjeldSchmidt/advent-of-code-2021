folds = [
    ("x", 655),
    ("y", 447),
    ("x", 327),
    ("y", 223),
    ("x", 163),
    ("y", 111),
    ("x", 81),
    ("y", 55),
    ("x", 40),
    ("y", 27),
    ("y", 13),
    ("y", 6),
]

points = set()
with open("13-input.txt", "r") as f:
    for line in f.readlines():
        line = line.strip().split(",")
        points.add(tuple(map(int, line)))


def fold_x(points, fold_index):
    new_points = set()
    for point in points:
        if point[0] > fold_index:
            new_x = fold_index - (point[0] - fold_index)
        else :
            new_x = point[0]

        new_points.add((new_x, point[1]))

    return new_points


def fold_y(points, fold_index):
    new_points = set()
    for point in points:
        if point[1] > fold_index:
            new_y = fold_index - (point[1] - fold_index)
        else:
            new_y = point[1]

        new_points.add((point[0], new_y))

    return new_points


def plot(points):
    max_x = max(points)[0]
    max_y = max(map(lambda x: x[1], points))
    for col in range(max_y + 1):
        for row in range(max_x + 1):
            if (row, col) in points:
                print("#", end="")
            else:
                print(" ", end="")
        print()

print("Solution part 1:")
print(len(fold_x(points, folds[0][1])))


for dir, index in folds:
    if dir == "x":
        points = fold_x(points, index)

    if dir == "y":
        points = fold_y(points, index)


print("Solution part 2:")
plot(points)
