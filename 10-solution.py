lines = []
with open("10-input.txt", "r") as f:
    for line in f.readlines():
        lines.append(line.strip())

paren_count = {
    "{": 0,
    "(": 0,
    "[": 0,
    "<": 0,
}

close_match = {
    "{": "}",
    "(": ")",
    "[": "]",
    "<": ">",
}

open_match = {
    "}": "{",
    ")": "(",
    "]": "[",
    ">": "<",
}

error_scores = {
    ")": 3,
    "]": 57,
    "}": 1197,
    ">": 25137,
}

complete_scores = {
    "(": 1,
    "[": 2,
    "{": 3,
    "<": 4
}

score = 0
corrupted_c = 0
for line in lines:
    open_stack = []
    for paren in line:
        if paren in close_match.keys():
            open_stack.append(paren)
        else:
            previous_opened_paren = open_stack.pop()
            if previous_opened_paren != open_match[paren]:
                score += error_scores[paren]
                corrupted_c += 1
                break

print(score)


completion_scores = []
for line in lines:
    open_stack = []
    corrupted = False
    for paren in line:
        if paren in close_match.keys():
            open_stack.append(paren)
        else:
            previous_opened_paren = open_stack.pop()
            if previous_opened_paren != open_match[paren]:
                corrupted = True
                break

    completion_score = 0
    if not corrupted:
        to_close = open_stack[::-1]
        for closer in to_close:
            completion_score *= 5
            completion_score += complete_scores[closer]

        completion_scores.append(completion_score)

print(sorted(completion_scores)[int((len(completion_scores)-1)/2)])






