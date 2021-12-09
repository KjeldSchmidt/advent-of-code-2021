from collections import Counter
from time import time

timers = [3,5,4,1,2,1,5,5,1,1,1,1,4,1,4,5,4,5,1,3,1,1,1,4,1,1,3,1,1,5,3,1,1,3,1,3,1,1,1,4,1,2,5,3,1,4,2,3,1,1,2,1,1,1,4,1,1,1,1,2,1,1,1,3,1,1,4,1,4,1,5,1,4,2,1,1,5,4,4,4,1,4,1,1,1,1,3,1,5,1,4,5,3,1,4,1,5,2,2,5,1,3,2,2,5,4,2,3,4,1,2,1,1,2,1,1,5,4,1,1,1,1,3,1,5,4,1,5,1,1,4,3,4,3,1,5,1,1,2,1,1,5,3,1,1,1,1,1,5,1,1,1,1,1,1,1,2,2,5,5,1,2,1,2,1,1,5,1,3,1,5,2,1,4,1,5,3,1,1,1,2,1,3,1,4,4,1,1,5,1,1,4,1,4,2,3,5,2,5,1,3,1,2,1,4,1,1,1,1,2,1,4,1,3,4,1,1,1,1,1,1,1,2,1,5,1,1,1,1,2,3,1,1,2,3,1,1,3,1,1,3,1,3,1,3,3,1,1,2,1,3,2,3,1,1,3,5,1,1,5,5,1,2,1,2,2,1,1,1,5,3,1,1,3,5,1,3,1,5,3,4,2,3,2,1,3,1,1,3,4,2,1,1,3,1,1,1,1,1,1,]

timers = dict(Counter(timers))


time_pre = time()
for i in range(256):
    next_timers = {6:0}
    for key, value in sorted(timers.items(), reverse=True):
        if key != 0:
            next_timers[key-1] = value
        else:
            next_timers[6] += value
            next_timers[8] = value
    timers = next_timers
    # if i == 79:
    #     fish_count = sum(map(lambda x: x[1], timers.items()))
    #     print(f"Answer part 1: {fish_count}")

fish_count = sum(map(lambda x: x[1], timers.items()))
time_post = time()
print(f"Answer part 2: {fish_count}")

print(time_post-time_pre)