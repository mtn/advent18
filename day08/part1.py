#!/usr/bin/env python3

with open("input.txt") as f:
    inp = f.read().strip()
    inp = list(map(int, inp.split()))


def read_child(inp):
    num_children = inp[0]
    num_meta = inp[1]

    if num_children == 0:
        return sum(inp[2 : num_meta + 2]), 2 + num_meta

    child_sum = 0
    child_advanced = 2
    for child_num in range(num_children):
        meta_sum, advance = read_child(inp[child_advanced:])
        child_sum += meta_sum
        child_advanced += advance

    return sum(inp[child_advanced:][0:num_meta]) + child_sum, child_advanced + num_meta


print(read_child(inp)[0])
