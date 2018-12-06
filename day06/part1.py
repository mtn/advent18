#!/usr/bin/env python3

from collections import defaultdict

min_x = min_y = max_x = max_y = None

grid = defaultdict(int)
counts = defaultdict(int)
coords = set()
infinite = set()


def dist(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)


def find_nearest(x, y, coords):
    min_dist = None
    closest_coord = None
    cur_dist_count = 0

    for coord in coords:
        coord_dist = dist(coord[0], coord[1], x, y)

        if min_dist is None or coord_dist < min_dist:
            min_dist = coord_dist
            closest_coord = coord
            cur_dist_count = 1
        elif coord_dist == min_dist:
            cur_dist_count += 1

    if cur_dist_count != 1:
        return None

    return closest_coord


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

for x in range(min_x, max_x + 1):
    grid[x] = {}
    for y in range(min_y, max_y + 1):
        grid[x][y] = find_nearest(x, y, coords)

        if x == min_x or x == max_x or y == min_y or y == max_y:
            infinite.add(grid[x][y])

        counts[grid[x][y]] += 1

max_area = None
max_coord = None
for coord in coords - infinite:
    if max_area is None or counts[coord] > max_area:
        max_area = counts[coord]
        max_coord = coord

print(max_area)
