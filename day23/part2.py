#!/usr/bin/env python3

import re
from z3 import *

points = set()
radii = {}
with open("input.txt") as f:
    for line in f:
        x, y, z, r = map(int, re.findall("-?[0-9]+", line))
        point = (x, y, z)
        points.add(point)
        radii[point] = r

def zabs(x):
    return If(x >= 0, x, -x)

def zdist(a, b):
    "a, b :: (x, y z)"
    return zabs(a[0] - b[0]) + zabs(a[1] - b[1])  + zabs(a[2] - b[2])

def dist(a, b):
    "a, b :: (x, y z)"
    return abs(a[0] - b[0]) + abs(a[1] - b[1])  + abs(a[2] - b[2])

x, y, z = Ints("x y z") # variable coord
pt = (x, y, z)

o = Optimize()
in_range = Int("in_range")
in_range = x * 0
for point in points:
    in_range += If(zdist(pt, point) <= radii[point], 1, 0)

num_in_range = Int("num_in_range")
o.add(num_in_range == in_range)
o.maximize(num_in_range)
o.check()

model = o.model()
best = model[x].as_long(), model[y].as_long(), model[z].as_long()
print(dist((0,0,0), best))

