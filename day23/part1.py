#!/usr/bin/env python3

import re

def first_can_reach_second(p1, p2):
    x1, y1, z1, r1 = p1
    x2, y2, z2, r2 = p2

    dist = abs(x1-x2) + abs(y1-y2) + abs(z1-z2)

    return r1 >= dist

points = set()
maxpoint = None
rmax = -1
with open("input.txt") as f:
    for line in f:
        x, y, z, r = map(int, re.findall("-?[0-9]+", line))
        points.add((x, y, z, r))
        if r > rmax:
            maxpoint = (x, y, z, r)
            rmax = r

can_reach_cnt = 0
for p in points:
    if first_can_reach_second(maxpoint, p):
        can_reach_cnt += 1


print(can_reach_cnt)



