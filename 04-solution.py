import numpy as np
draws = [
    18,
    99,
    39,
    89,
    0,
    40,
    52,
    72,
    61,
    77,
    69,
    51,
    30,
    83,
    20,
    65,
    93,
    88,
    29,
    22,
    14,
    82,
    53,
    41,
    76,
    79,
    46,
    78,
    56,
    57,
    24,
    36,
    38,
    11,
    50,
    1,
    19,
    26,
    70,
    4,
    54,
    3,
    84,
    33,
    15,
    21,
    9,
    58,
    64,
    85,
    10,
    66,
    17,
    43,
    31,
    27,
    2,
    5,
    95,
    96,
    16,
    97,
    12,
    34,
    74,
    67,
    86,
    23,
    49,
    8,
    59,
    45,
    68,
    91,
    25,
    48,
    13,
    28,
    81,
    94,
    92,
    42,
    7,
    37,
    75,
    32,
    6,
    60,
    63,
    35,
    62,
    98,
    90,
    47,
    87,
    73,
    44,
    71,
    55,
    80,
]

with open("04-input.txt", "r") as f:
    board_lines = [list(map(int, l.strip().split())) for l in f.readlines() if l != '\n']


boards = []
for i in range(0, len(board_lines), 5):
    boards.append(board_lines[i:i+5])

boards: np.ndarray = np.array([np.array(board) for board in boards ])
masks: np.ndarray = np.zeros(boards.shape)

assert boards.shape == (100, 5, 5)
assert boards.shape == masks.shape


def get_winners(masks, dim):
    if masks.shape == (0, 5, 5):
        return []
    sums = np.apply_along_axis(sum, dim, masks)
    return np.argwhere(sums == 5)

winning_scores = []
for draw in draws:
    hits = np.argwhere(boards == draw)
    for hit in hits:
        masks[hit[0], hit[1], hit[2]] = 1

    for dim in [1, 2]:
        while len(winners := get_winners(masks, dim)) >= 1:
            if len(winners) >= 1:
                for winner in winners:
                    winning_board_index = winner[0]
                    drawn = masks[winning_board_index] * boards[winning_board_index]
                    board_sum = np.sum(boards[winning_board_index])
                    drawn_sum = np.sum(drawn)
                    winning_scores.append(int((board_sum - drawn_sum)*draw))
                    boards = np.delete(boards, winning_board_index, 0)
                    masks = np.delete(masks, winning_board_index, 0)
                    assert boards.shape == masks.shape
                    break

print(f"Answer part 1: {winning_scores[0]}")
print(f"Answer part 2: {winning_scores[-1]}")