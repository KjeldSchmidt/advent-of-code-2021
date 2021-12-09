import time
from functools import reduce

lines = []

lengths = {
    0: 6,
    1: 2,
    2: 5,
    3: 5,
    4: 4,
    5: 5,
    6: 6,
    7: 3,
    8: 7,
    9: 6
}

unique_lengths = {
    1: 2,
    4: 4,
    7: 3,
    8: 7,
}

segments = {
    0: [0, 1, 2, 4, 5, 6],
    1: [2, 5],
    2: [0, 2, 3, 4, 6],
    3: [0, 2, 3, 5, 6],
    4: [1, 2, 3, 5],
    5: [0, 1, 3, 5, 6],
    6: [0, 1, 3, 4, 5, 6],
    7: [0, 2, 5],
    8: [0, 1, 2, 3, 4, 5, 6],
    9: [0, 1, 2, 3, 5, 6]
}

with open("08-input.txt") as f:
    for line in f.readlines():
        line = line.strip().split("|")
        line = list(map(lambda x: x.split(), line))
        lines.append(line)

outputs = reduce(lambda a, b: a+b, map(lambda x: x[1], lines))
lengths = map(len, outputs)
unique = list(filter(lambda x: x in [2, 4, 3, 7], lengths))

print("Solution part 1")
print(len(unique))

base_candidates = [0, 1, 2, 3, 4, 5, 6]
wires = ["a", "b", "c", "d", "e", "f", "g"]


start = time.time()

total = 0
for line in lines:
    candidates = {}
    inputs = line[0]
    outputs = line[1]
    inputs: list[str] = sorted(inputs, key=len)
    # candidates for segments 2 and 5 derived from 1-display
    candidates[2] = [c for c in inputs[0]]
    candidates[5] = [c for c in inputs[0]]
    # Determine segment 0 by subtracting 1-display from 7-display
    candidates[0] = [c for c in inputs[1] if c not in inputs[0]]


    # determine segment 2 by comparing the single missing value for 0, 6, 9
    single_missing = { letter: 0 for letter in wires }
    for letters in [inputs[6], inputs[7], inputs[8]]:
        for letter in letters:
            single_missing[letter] += 1

    single_missing = [ letter for letter, c in single_missing.items() if c == 2]
    candidates[2] = [l for l in single_missing if l in candidates[2]]
    candidates[5].remove(candidates[2][0])
    single_missing.remove(candidates[2][0])

    # Use 4 to tell the assignment for the other single missing ones
    candidates[3] = [l for l in single_missing if l in inputs[2]]
    candidates[4] = [l for l in single_missing if l not in inputs[2]]


    # Compare 2, 3, 5 to figure out wires for 1 and 6
    double_missing = { letter: 0 for letter in wires }
    for letters in [inputs[3], inputs[4], inputs[5]]:
        for letter in letters:
            double_missing[letter] += 1

    candidates[1] = [l for l, c in double_missing.items() if c == 1 and l not in candidates[4]]
    candidates[6] = [l for l in wires if l not in [v[0] for k, v in candidates.items()]]

    mappings = {v[0]: k for k, v in candidates.items()}

    active_segments = [sorted([mappings[c] for c in output]) for output in outputs]

    nums = [[k for k, v in segments.items() if v == a][0] for a in active_segments]
    full_num = int(''.join(map(str, nums)))

    total += full_num

end = time.time()

print("Solution part 2")
print(total)
print("Runtime")
print(end-start)