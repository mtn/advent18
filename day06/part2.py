#!/usr/bin/env python3

from collections import defaultdict

min_x = min_y = max_x = max_y = None

grid = defaultdict(int)
counts = defaultdict(int)
coords = set()
infinite = set()


def dist(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)


with open("input.txt") as f:
    for coord in f:
        x, y = map(int, coord.split(","))
        coords.add((x, y))

        if min_x is None or x < min_x:
            min_x = x
        if max_x is None or x > max_x:
            max_x = x
        if min_y is None or y < min_y:
            min_y = y
        if max_y is None or y > max_y:
            max_y = y


region_size = 0
for x in range(min_x, max_x + 1):
    grid[x] = {}
    for y in range(min_y, max_y):
        dist_sum = 0
        for coord in coords:
            dist_sum += dist(x, y, coord[0], coord[1])

            if dist_sum > 10000:
                break
        else:
            if dist_sum < 10000:
                region_size += 1

print(region_size)
