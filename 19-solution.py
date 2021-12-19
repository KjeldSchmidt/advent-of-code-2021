from collections import defaultdict

scanners = []

with open("19-input.txt", "r") as f:
    beacons = []
    for line in f.readlines():
        line = line.strip()

        if line.startswith("--- scanner"):
            continue

        if line == "":
            scanners.append(beacons)
            beacons = []
            continue

        beacons.append(tuple(map(int, line.split(","))))


def generate_rotations(scanner):
    rotations = []

    rotations.append([(x, y, z) for x, y, z in scanner])
    rotations.append([(x, z, -y) for x, y, z in scanner])
    rotations.append([(x, -y, -z) for x, y, z in scanner])
    rotations.append([(x, -z, y) for x, y, z in scanner])

    rotations.append([(-x, y, -z) for x, y, z in scanner])
    rotations.append([(-x, -z, -y) for x, y, z in scanner])
    rotations.append([(-x, -y, z) for x, y, z in scanner])
    rotations.append([(-x, z, y) for x, y, z in scanner])

    rotations.append([(y, z, x) for x, y, z in scanner])
    rotations.append([(y, x, -z) for x, y, z in scanner])
    rotations.append([(y, -z, -x) for x, y, z in scanner])
    rotations.append([(y, -x, z) for x, y, z in scanner])

    rotations.append([(-y, x, z) for x, y, z in scanner])
    rotations.append([(-y, z, -x) for x, y, z in scanner])
    rotations.append([(-y, -x, -z) for x, y, z in scanner])
    rotations.append([(-y, -z, x) for x, y, z in scanner])

    rotations.append([(z, y, -x) for x, y, z in scanner])
    rotations.append([(z, -x, -y) for x, y, z in scanner])
    rotations.append([(z, -y, x) for x, y, z in scanner])
    rotations.append([(z, x, y) for x, y, z in scanner])

    rotations.append([(-z, x, -y) for x, y, z in scanner])
    rotations.append([(-z, -y, -x) for x, y, z in scanner])
    rotations.append([(-z, -x, y) for x, y, z in scanner])
    rotations.append([(-z, y, x) for x, y, z in scanner])

    return rotations


known_scanners = [scanners[0]]
unknown_scanners = scanners[1:]

known_offsets = {
    scanners.index(known_scanners[0]): (0, 0, 0)
}

known_scanner_index = {
    0: 0
}


def find_offset(unknown_scanner, known_scanner):
    possible_orientations = generate_rotations(unknown_scanner)
    for orientation in possible_orientations:
        offsets = defaultdict(lambda: 0)
        for x1, y1, z1 in orientation:
            for x2, y2, z2 in known_scanner:

                offsets[(x2-x1, y2-y1, z2-z1)] += 1

        for offset, count in offsets.items():
            if count >= 12:
                return offset, orientation

    return None, None


def find_first_match(known_scanner, unknown_scanners):
    for unknown_scanner in unknown_scanners:
        offset, correct_orientation = find_offset(unknown_scanner, known_scanner)
        if offset is not None:
            return offset, unknown_scanner, correct_orientation

    return None, None, None


while len(unknown_scanners) != 0:
    for known_index, known_scanner in enumerate(known_scanners):
        offset, previously_unknown, correct_orientation = find_first_match(known_scanner, unknown_scanners)
        if previously_unknown is not None:
            known_scanners.append(correct_orientation)
            unknown_scanners.remove(previously_unknown)
            base_offset = known_offsets[known_scanner_index[known_index]]
            base_scanner_index = scanners.index(previously_unknown)
            known_scanner_index[len(known_scanners) - 1] = base_scanner_index
            known_offsets[base_scanner_index] = (
                (base_offset[0] - offset[0]),
                (base_offset[1] - offset[1]),
                (base_offset[2] - offset[2])
            )
            break

known_offsets = { key: (-p[0], -p[1], -p[2]) for key, p in known_offsets.items()}

absolute_beacons = set()
for i, scanner in enumerate(known_scanners):
    off_x, off_y, off_z = known_offsets[known_scanner_index[i]]
    for x, y, z in scanner:
        absolute_point = x + off_x, y + off_y, z + off_z
        absolute_beacons.add(absolute_point)

print("Solution part 1:")
print()

print(known_offsets)
