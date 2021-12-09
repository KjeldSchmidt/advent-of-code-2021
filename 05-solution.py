import numpy as np

vent_lines = []
with open("05-input.txt", "r") as f:
    for line in f.readlines():
        line = line.strip().split(" -> ")
        line = map(lambda x: x.split(","), line)
        line = list(map(lambda x: list(map(int, x)), line))
        vent_lines.append(line)

vent_map = np.zeros((1000, 1000))


def is_diagonal(vent_line):
    return vent_line[0][0] != vent_line[1][0] and vent_line[0][1] != vent_line[1][1]


def extract_straight(vent_line):
    x0 = min(vent_line[0][0], vent_line[1][0])
    x1 = max(vent_line[0][0], vent_line[1][0])+1
    y0 = min(vent_line[0][1], vent_line[1][1])
    y1 = max(vent_line[0][1], vent_line[1][1])+1
    return x0, x1, y0, y1


for vent_line in vent_lines:
    if is_diagonal( vent_line ):
        continue
    x0, x1, y0, y1 = extract_straight(vent_line)
    vent_map[x0:x1, y0:y1] += 1


print(f"Answer part 1: {len(np.where(vent_map > 1)[0])}")


def diagonal_steps(vent_line):
    x0 = vent_line[0][0]
    x1 = vent_line[1][0]
    y0 = vent_line[0][1]
    y1 = vent_line[1][1]
    x_step = 1 if x0 < x1 else -1
    y_step = 1 if y0 < y1 else -1

    while x0 != x1:
        yield x0, y0
        x0 += x_step
        y0 += y_step
    yield x1, y1


for vent_line in vent_lines:
    if not is_diagonal( vent_line ):
        continue

    for x, y in diagonal_steps(vent_line):
        vent_map[x, y] += 1

print(f"Answer part 2: {len(np.where(vent_map > 1)[0])}")