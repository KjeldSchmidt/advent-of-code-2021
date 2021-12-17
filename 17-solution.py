x_range = (150, 193)
y_range = (-136, -86)


def get_possible_x_speeds(min_x, max_x):
    possible_speeds = []
    for initial_speed in range(max_x+1):
        min_steps = -1
        max_steps = -1
        for step_count in range(initial_speed+1):
            distance_after_j_steps = initial_speed*step_count - step_count*(step_count-1)//2
            if min_x <= distance_after_j_steps <= max_x:
                if min_steps == -1:
                    min_steps = step_count
                max_steps = step_count
            if distance_after_j_steps >= max_x:
                break

        if min_steps != -1:
            possible_speeds.append((initial_speed, min_steps, max_steps))

    return possible_speeds


def y_pos_calc(y_speed, step_count):
    return sum([y_speed - i for i in range(step_count)])


def get_possible_y_speeds(min_steps, max_steps):
    possible_speeds = set()
    for step_count in range(min_steps, max_steps + 1):
        for speed in range(y_range[0], max_steps):
            if y_pos_calc(speed, step_count) in range(y_range[0], y_range[1] + 1):
                possible_speeds.add(speed)

    possible_speeds = sorted(list(possible_speeds))

    return possible_speeds


possible_x_speeds = get_possible_x_speeds(x_range[0], x_range[1])

possible_start_speeds = []
for x_speed, min_steps, max_steps in possible_x_speeds:
    if x_speed == max_steps:
        max_steps = 400
    y_speeds = get_possible_y_speeds(min_steps, max_steps)
    # print(f"For x_speed {x_speed}, there are {len(y_speeds)} possibilities:")
    # print(f"These occur within {min_steps} and {max_steps} steps")
    for y_speed in y_speeds:
        # print(f"{x_speed},{y_speed}")
        possible_start_speeds.append((x_speed, y_speed))

print("Solution part 2:")
print(len(possible_start_speeds))




