#!/usr/bin/env python3

from collections import defaultdict

inp = 3214


def power_level(x, y):
    rack_id = x + 10
    power_level = rack_id * y
    power_level += inp
    power_level *= rack_id

    as_str = str(power_level)
    assert len(as_str) >= 3
    hundreds_digit = int(as_str[-3])

    return hundreds_digit - 5


def setup_table(inp):
    table = defaultdict(int)

    for y in range(1, 301):
        for x in range(1, 301):
            table[(x, y)] = (
                power_level(x, y)
                + table[(x, y - 1)]
                + table[(x - 1, y)]
                - table[(x - 1, y - 1)]
            )

    return table


table = setup_table(inp)


def grid_area(size, x, y):
    global table

    x0, y0, x1, y1 = x - 1, y - 1, x + size - 1, y + size - 1

    return table[(x0, y0)] + table[(x1, y1)] - table[(x1, y0)] - table[(x0, y1)]


def largest_sum(size):
    global table

    max_res = ()
    for x in range(1, 301 - size + 1):
        for y in range(1, 301 - size + 1):
            area = grid_area(size, x, y)
            if max_res == () or area > max_res[0]:
                max_res = (area, x, y)

    return max_res


largest = largest_sum(1)
largest_size = 0
for i in range(2, 301):
    max_isum = largest_sum(i)
    if max_isum > largest:
        largest = max_isum
        largest_size = i

print(f"{largest[1]},{largest[2]},{largest_size}")
