from collections import defaultdict
from typing import Tuple

scanners = []

with open("19-input-small.txt", "r") as f:
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

def find_offset(unknown_scanner, known_scanner):
    possible_orientations = generate_rotations(unknown_scanner)
    for orientation in possible_orientations:
        offsets = defaultdict(lambda: 0)
        for x1, y1, z1 in orientation:
            for x2, y2, z2 in known_scanner:

                offsets[(x2-x1, y2-y1, z2-z1)] += 1

        for offset, count in offsets.items():
            if count >= 12:
                return offset

    return None


def find_first_match(known_scanner, unknown_scanners):
    for unknown_scanner in unknown_scanners:
        offset = find_offset(unknown_scanner, known_scanner)
        if offset is not None:
            return offset, unknown_scanner

    return None, None


while len(unknown_scanners) != 0:
    for known_scanner in known_scanners:
        offset, previously_unknown = find_first_match(known_scanner, unknown_scanners)
        if previously_unknown is not None:
            known_scanners.append(previously_unknown)
            unknown_scanners.remove(previously_unknown)
            base_offset = known_offsets[scanners.index(known_scanner)]
            known_offsets[scanners.index(previously_unknown)] = (
                offset[0] - base_offset[0],
                offset[1] - base_offset[1],
                offset[2] - base_offset[2]
            )
            break

print(known_offsets)
