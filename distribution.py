__author__ = 'mark'

import random
random.seed(1776)

num_voters = 8820000

count = 10
prob = 0.99

correct = 0

over_8k = 0

for n in range(count):
    correct = 0
    for voter in range(num_voters):
        correct += int(random.uniform(0,1) < 0.9)
    print(correct)
    if correct > 8000000:
        over_8k += 1

print(over_8k)