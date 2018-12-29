#!/usr/bin/env python3

import re

from sys import setrecursionlimit
setrecursionlimit(10000)

grid = {}

with open("input.txt") as f:
    for line in f:
        if "x" == line[0]:
            x, y_start, y_end = list(map(int, re.findall("[0-9]+", line)))

            for y in range(y_start, y_end + 1):
                grid[(x, y)] = "#"
        else:
            y, x_start, x_end = list(map(int, re.findall("[0-9]+", line)))

            for x in range(x_start, x_end + 1):
                grid[(x, y)] = "#"

xs = [x for x, _ in grid.keys()]
ys = [y for _, y in grid.keys()]
xmin, xmax = min(xs), max(xs)
ymin, ymax = min(ys), max(ys)

def print_grid():
    print("")
    for y in range(0, ymax+1):
        row_str = ""
        for x in range(xmin, xmax+1):
            if (x, y) in grid:
                row_str += grid[(x, y)]
            else:
                row_str += "."
        print(row_str)
    print("")


def fall(pos):
    "fall downwards, if possible"
    global grid
    x, y = pos
    if y >= ymax:
        return

    if (x, y+1) not in grid:
        # space below => fall downwards
        grid[(x, y+1)] = "|"
        fall((x, y+1))

    # expand left and right, if possible
    if grid[(x, y+1)] in "~#" and (x-1, y) not in grid:
        # solid below and empty to left => expand left
        grid[(x-1, y)] = "|"
        fall((x-1, y))
    if grid[(x, y+1)] in "~#" and (x+1, y) not in grid:
        # solid below and empty to right => expand right
        grid[(x+1, y)] = "|"
        fall((x+1, y))

    try_expand((x, y))

def try_expand(pos):
    x, y = pos

    lx = rx = x
    lwall = rwall = False
    while True:
        if (lx, y) not in grid:
            lwall = False
            break
        elif grid[(lx, y)] == "#":
            lwall = True
            break
        lx -= 1
    while True:
        if (rx, y) not in grid:
            rwall = False
            break
        elif grid[(rx, y)] == "#":
            rwall = True
            break
        rx += 1

    bounded = lwall and rwall
    if bounded:
        expand(pos)

def expand(pos):
    global grid

    x, y = pos
    lx = rx = x
    while True:
        if (lx, y) in grid and grid[(lx, y)] == "#":
            break
        grid[(lx, y)] = "~"
        lx -= 1
    while True:
        if (rx, y) in grid and grid[(rx, y)] == "#":
            break
        grid[(rx, y)] = "~"
        rx += 1

fall((500, 0))
print(len([(x, y) for x, y in grid.keys() if grid[(x, y)] in "|~" and y <= ymax and y >= ymin]))
