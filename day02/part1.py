#!/usr/bin/env python3

import collections

num_exactly_twice = num_exactly_thrice = 0


with open("input.txt") as f:
    for word in f:
        counts = collections.defaultdict(int)
        for letter in word:
            counts[letter] += 1

        if 2 in counts.values():
            num_exactly_twice += 1
        if 3 in counts.values():
            num_exactly_thrice += 1

print(num_exactly_twice * num_exactly_thrice)
