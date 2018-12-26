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


# min_area = compute_area()
# min_ind = 0
# for tick in range(12000):
#     for i, (x, y, xvel, yvel) in enumerate(points):
#         points[i] = (x + xvel, y + yvel, xvel, yvel)
#     area = compute_area()
#     if area < min_area:
#         min_ind = tick
#         min_area = area

min_ind = 10476
for tick in range(min_ind):
    for i, (x, y, xvel, yvel) in enumerate(points):
        points[i] = (x + xvel, y + yvel, xvel, yvel)


def plot_sky():
    global points

    coords_x = list(map(lambda x: x[0], points))
    coords_y = list(map(lambda x: x[1], points))

    max_y = max(coords_y)
    coords_yy = list(map(lambda y: max_y - y, coords_y))

    plt.scatter(coords_x, coords_yy)
    plt.show()


plot_sky()
