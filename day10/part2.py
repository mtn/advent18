#!/usr/bin/env python3

import re
import matplotlib.pyplot as plt


points = []
with open("input.txt") as f:
    for line in f:
        matches = re.findall("(-?[0-9]+)", line)
        x, y, xvel, yvel = map(int, matches)

        points.append((x, y, xvel, yvel))


def compute_area():
    global points

    min_x, min_y, max_x, max_y = points[0][0], points[0][1], points[0][0], points[0][1]

    for x, y, _, _ in points:
        min_x = min(min_x, x)
        max_x = max(max_x, x)
        min_y = min(min_y, y)
        max_y = max(max_y, y)

    return (max_x - min_x) * (max_y - min_y)


min_area = compute_area()
min_ind = 0
for tick in range(1, 12000):
    for i, (x, y, xvel, yvel) in enumerate(points):
        points[i] = (x + xvel, y + yvel, xvel, yvel)
    area = compute_area()
    if area < min_area:
        min_ind = tick
        min_area = area

print(min_ind)
