#!/usr/bin/env python3

from collections import defaultdict

open_parens = []
start_end = {}  # open paren to close paren ind
alt_starts = {}  # alternation to opening "("
alts = {}  # maps "(" ind to [alternations]
with open("input.txt") as f:
    inp = f.read().strip()

for i, ch in enumerate(inp):
    if ch == "$":
        break

    if ch == "(":
        open_parens.append(i)
    elif ch == ")":
        last_open = open_parens.pop()
        start_end[last_open] = i

    if ch == "|":
        alt_starts[i] = open_parens[-1]
        if open_parens[-1] in alts:
            alts[open_parens[-1]].append(i)
        else:
            alts[open_parens[-1]] = [i]

assert not open_parens  # all opened parens should be closed

g = defaultdict(set)  # graph represented as adjacency lists
visited = set()  # what we've visited so we don't cycle in inp


def run(point, ind):
    global g

    while True:
        if inp[ind] == "$" or (point, ind) in visited:
            break

        visited.add((point, ind))

        if inp[ind] == "N":
            new = (point[0], point[1] - 1)
            g[point].add(new)
            g[new].add(point)
            ind += 1
            point = new
        elif inp[ind] == "E":
            new = (point[0] + 1, point[1])
            g[point].add(new)
            g[new].add(point)
            ind += 1
            point = new
        elif inp[ind] == "S":
            new = (point[0], point[1] + 1)
            g[point].add(new)
            g[new].add(point)
            ind += 1
            point = new
        elif inp[ind] == "W":
            new = (point[0] - 1, point[1])
            g[point].add(new)
            g[new].add(point)
            ind += 1
            point = new

        elif inp[ind] == "|":
            # jump to the end of the alternation
            ind = start_end[alt_starts[ind]] + 1

        elif inp[ind] == "(":
            for alt in alts[ind]:
                run(point, alt + 1)
            ind += 1  # the first branch wasn't parsed as part of the alts
        elif inp[ind] == ")":
            ind += 1


run((0, 0), 1)

q = [((0, 0), 0)]
distances = {}
while q:
    (x, y), dist = q.pop()
    if (x, y) in distances and distances[(x, y)] <= dist:
        continue

    distances[(x, y)] = dist
    for neighbor in g[(x, y)]:
        q.append((neighbor, dist + 1))

print(max(distances.values()))
