#!/usr/bin/env python3

grid = {}
height = width = 0
with open("input.txt") as f:
    for y, line in enumerate(f):
        height += 1
        for x, c in enumerate(line.strip()):
            grid[(x, y)] = c

width = len(grid.keys()) // height


def n_or_more(pos, ch, n=1):
    x, y = pos
    num_adjacent = 0
    for dx in range(-1, 2):
        for dy in range(-1, 2):
            if dx == dy == 0:
                continue
            if x + dx < 0 or y + dy < 0 or x + dx >= width or y + dy >= height:
                continue

            if grid[(x + dx, y + dy)] == ch:
                num_adjacent += 1

    return num_adjacent >= n


def step():
    next_grid = {}

    for y in range(height):
        for x in range(width):
            if grid[(x, y)] == ".":
                if n_or_more((x, y), "|", n=3):
                    next_grid[(x, y)] = "|"
                else:
                    next_grid[(x, y)] = "."
            elif grid[(x, y)] == "|":
                if n_or_more((x, y), "#", n=3):
                    next_grid[(x, y)] = "#"
                else:
                    next_grid[(x, y)] = "|"
            elif grid[(x, y)] == "#":
                if n_or_more((x, y), "|", n=1) and n_or_more((x, y), "#", n=1):
                    next_grid[(x, y)] = "#"
                else:
                    next_grid[(x, y)] = "."

    return next_grid


def print_grid(grid):
    print("")
    for y in range(height):
        row_str = ""
        for x in range(width):
            row_str += grid[(x, y)]
        print(row_str)
    print("")


for i in range(10):
    grid = step()

# print_grid(grid)
num_wooded = len([(x, y) for x, y in grid.keys() if grid[(x, y)] == "|"])
num_lumber = len([(x, y) for x, y in grid.keys() if grid[(x, y)] == "#"])

print(num_wooded * num_lumber)
