#!/usr/bin/env python3

with open("input.txt") as f:
    inp = f.read().strip()
    lines = inp.split("\n")

initial_state = "..." + lines[0].split()[2] + "..."
initial_state = list(map(lambda x: 1 if x == "#" else 0, initial_state))

# Only track the growths, because we'll start assuming no growth
grows = set()
for rule in lines[2:]:
    pattern, _, outcome = rule.split()
    if outcome == "#":
        grows.add(pattern)

as_lists = {}
for rule in grows:
    as_lists[rule] = [1 if e == "#" else 0 for e in rule]


def state_as_str(state):
    return "".join(["#" if i == 1 else "." for i in state])


state = initial_state
num_plants = len(state)


front_ind = 3
for generation in range(20):
    new_state = [0] * len(state)
    for i in range(2, len(state) - 2):
        for rule in grows:
            if as_lists[rule] == state[i - 2 : i + 3]:
                new_state[i] = 1
                break

    if new_state[0:3] != [0, 0, 0]:
        front_ind += 3
        new_state = [0, 0, 0] + new_state
    if new_state[-3:] != [0, 0, 0]:
        new_state = new_state + [0, 0, 0]

    state = new_state

print(sum([i - front_ind for i, plant in enumerate(state) if plant == 1]))
