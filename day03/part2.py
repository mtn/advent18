#!/usr/bin/env python3

import collections

counts = collections.defaultdict(set)
overlapped = {}


with open("input.txt") as f:
    for claim in f:
        claim_split = claim.strip().split()
        claim_id = claim_split[0]
        left_offset, top_offset = map(int, claim_split[2][:-1].split(","))
        width, height = map(int, claim_split[3].split("x"))

        for x in range(width):
            for y in range(height):
                if (x + left_offset, y + top_offset) not in counts:
                    counts[(x + left_offset, y + top_offset)].add(claim_id)

                    if claim_id not in overlapped or not overlapped[claim_id]:
                        overlapped[claim_id] = False
                else:
                    counts[(x + left_offset, y + top_offset)].add(claim_id)
                    for elem in counts[(x + left_offset, y + top_offset)]:
                        overlapped[elem] = True
                    counts[(x + left_offset, y + top_offset)] = set()


for k in overlapped:
    if overlapped[k] == False:
        print(k[1:])
