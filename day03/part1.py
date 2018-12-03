#!/usr/bin/env python3

import collections

counts = collections.defaultdict(int)

with open("input.txt") as f:
    for claim in f:
        claim_split = claim.strip().split()
        left_offset, top_offset = map(int, claim_split[2][:-1].split(","))
        width, height = map(int, claim_split[3].split("x"))

        for x in range(width):
            for y in range(height):
                counts[(x + left_offset, y + top_offset)] += 1

total = 0
for k in counts:
    if counts[k] >= 2:
        total += 1

print(total)
