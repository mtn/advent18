#!/usr/bin/env python3

import re
import heapq

with open("input.txt") as f:
    depth_line, target_line = f.read().strip().split("\n")

depth = int(re.findall("[0-9]+", depth_line)[0])

coords = re.findall("[0-9]+", target_line)
tx, ty = int(coords[0]), int(coords[1])

erosion = {}
# just go way beyond the target, hope it's big enough
# doesn't take very long to compute
for y in range(1000):
    for x in range(2000):
        if x == y == 0: gi = 0
        elif x == tx and y == ty:
            gi = 0
        elif y == 0:
            gi = x * 16807
        elif x == 0:
            gi = y * 48271
        else:
            gi = erosion[(x-1, y)] * erosion[(x, y-1)]

        erosion_level = (gi + depth) % 20183
        erosion[(x, y)] = erosion_level

GEAR_TORCH = 0
GEAR_CLIMBING = 1
GEAR_NONE = 2

REGION_ROCK = 0
REGION_WET = 1
REGION_NARROW = 2

def check_gear(region, gear_type):
    if region == REGION_ROCK:
        return gear_type in [GEAR_CLIMBING, GEAR_TORCH]
    elif region == REGION_WET:
        return gear_type in [GEAR_CLIMBING, GEAR_NONE]
    elif region == REGION_NARROW:
        return gear_type in [GEAR_TORCH, GEAR_NONE]
    assert False, "bad region value to check_gear"


reached = set() # ((x, y), gear_type)
q = [(0, (0,0), GEAR_TORCH)] # (time, (x, y), gear_type), sorted by time (ties safely arbitrary)
heapq.heapify(q) # a min heap

while q:
    t, (x, y), gear_type = heapq.heappop(q)

    if gear_type == GEAR_TORCH and x == tx and y == ty:
        print(t)
        break

    if ((x, y), gear_type) in reached:
        continue
    reached.add(((x, y), gear_type))

    region_type = erosion[(x, y)] % 3
    # Spawn changers
    for change_gear in [GEAR_TORCH, GEAR_CLIMBING, GEAR_NONE]:
        if check_gear(region_type, change_gear):
            heapq.heappush(q, (t+7, (x, y), change_gear))

    if x + 1 < 2000 and check_gear(erosion[(x+1, y)]%3, gear_type):
        heapq.heappush(q, (t+1, (x+1, y), gear_type))
    if x - 1 >= 0 and check_gear(erosion[(x-1, y)]%3, gear_type):
        heapq.heappush(q, (t+1, (x-1, y), gear_type))
    if y + 1 >= 0 and check_gear(erosion[(x, y+1)]%3, gear_type):
        heapq.heappush(q, (t+1, (x, y+1), gear_type))
    if y - 1 >= 0 and check_gear(erosion[(x, y-1)]%3, gear_type):
        heapq.heappush(q, (t+1, (x, y-1), gear_type))




