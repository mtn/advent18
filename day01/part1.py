#!/usr/bin/env python3

total = 0
with open("inp1") as f:
    for line in f:
        total += int(line.strip())

print(total)


