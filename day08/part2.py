#!/usr/bin/env python3

with open("input.txt") as f:
    inp = f.read().strip()
    # inp = "2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2"
    inp = list(map(int, inp.split()))

nodes = {}


def read_child(node_id, inp):
    num_children = inp[0]
    num_meta = inp[1]

    if num_children == 0:
        nodes[node_id] = (0, inp[2 : num_meta + 2], [])
        return 2 + num_meta, 1

    child_advanced = 2
    num_nested_children = 0
    children = []
    for child_num in range(num_children):
        advance, advance_id = read_child(
            node_id + num_nested_children + 1, inp[child_advanced:]
        )
        children.append(node_id + num_nested_children + 1)
        num_nested_children += advance_id
        child_advanced += advance

    nodes[node_id] = (num_nested_children, inp[child_advanced:][0:num_meta], children)

    return child_advanced + num_meta, num_nested_children + 1


def compute_value(ind):
    _, meta, children = nodes[ind]

    if len(children) == 0:
        return sum(meta)

    child_sum = 0
    for ind in meta:
        if ind > len(children):
            continue
        child_sum += compute_value(children[ind - 1])

    return child_sum


read_child(0, inp)
print(compute_value(0))

# for node in nodes:
