#!/usr/bin/env python3

import re

with open("input.txt") as f:
    depth_line, target_line = f.read().strip().split("\n")

depth = int(re.findall("[0-9]+", depth_line)[0])

coords = re.findall("[0-9]+", target_line)
tx, ty = int(coords[0]), int(coords[1])

erosion = {}
risk_level = 0
for y in range(ty + 1):
    for x in range(tx + 1):
        if x == y == 0:
            gi = 0
        elif x == tx and y == ty:
            gi = 0
        elif y == 0:
            gi = x * 16807
        elif x == 0:
            gi = y * 48271
        else:
            gi = erosion[(x - 1, y)] * erosion[(x, y - 1)]

        erosion_level = (gi + depth) % 20183
        erosion[(x, y)] = erosion_level

for y in range(ty + 1):
    for x in range(tx + 1):
        risk_level += erosion[(x, y)] % 3

print(risk_level)
