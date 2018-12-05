#!/usr/bin/env python3

seen = set()
changes = []
with open("input.txt") as f:
    for line in f:
        changes.append(int(line.strip()))

total = 0
ind = 0
num_changes = len(changes)
while True:
    total += changes[ind]
    if total not in seen:
        seen.add(total)
    else:
        print(total)
        exit()

    ind += 1
    ind %= num_changes

print(total)
