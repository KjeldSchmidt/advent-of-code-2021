from functools import lru_cache

p1_pos = 7
p2_pos = 10


def deterministic_game(p1_pos, p2_pos):
    p1_score = 0
    p2_score = 0

    roll_count = 0
    die = 0
    die_max = 100

    p1_turn = True

    while max(p1_score, p2_score) < 1000:
        roll = 0
        for i in range(3):
            roll += die + 1
            roll_count += 1
            die = (die + 1) % die_max

        if p1_turn:
            for _ in range(roll):
                p1_pos += 1
                if p1_pos == 11:
                    p1_pos = 1
            p1_score += p1_pos
            p1_turn = False
            if p1_score >= 1000:
                return p2_score * roll_count
        else:
            for _ in range(roll):
                p2_pos += 1
                if p2_pos == 11:
                    p2_pos = 1
            p2_score += p2_pos
            p1_turn = True
            if p2_score >= 1000:
                return p1_score * roll_count


print("Solution part 1:")
print(deterministic_game(p1_pos, p2_pos))


def add_to_pos(pos, moves):
    new_pos = pos+moves
    if new_pos > 10:
        new_pos -= 10
    return new_pos


@lru_cache(maxsize=None)
def dirac_dice_win_count(p1_pos, p1_score, p2_pos, p2_score, until_move):
    assert min(p1_score, p2_score) < 21
    if p2_score >= 21:
        return 1, 0
    p1_wins = 0
    p2_wins = 0

    throws = [1, 2, 3]
    nested_wins = []
    for throw in throws:
        new_p1_pos = add_to_pos(p1_pos, throw)
        if until_move == 0:
            nested_wins.append(dirac_dice_win_count(p2_pos, p2_score, new_p1_pos, p1_score+new_p1_pos, 2)),
        else:
            nested_wins.append(dirac_dice_win_count(new_p1_pos, p1_score, p2_pos, p2_score, until_move-1)),

    for win in nested_wins:
        p2_wins += win[0]
        p1_wins += win[1]

    return p1_wins, p2_wins

print("Solution Part 2:")
print(max(dirac_dice_win_count(p1_pos, 0, p2_pos, 0, 2)))


