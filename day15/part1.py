#!/usr/bin/env python3

from enum import Enum
from collections import deque


class GridSlot(Enum):
    GRID_WALL = 1
    GRID_OPEN = 2

    def __repr__(self):
        return "#" if self.value == 1 else "."


class Goblin(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.hp = 200

    def bfs(self):
        "Search for reachable enemies"

        return bfs((self.y, self.x), Elf)

    def step(self):
        "move/attack"

        if self.hp <= 0:
            return

        old = (self.y, self.x)

        next_step = choose_move(self.bfs())
        if next_step is None:
            self.attack()
            return

        grid[old[0]][old[1]] = GridSlot.GRID_OPEN
        _, (self.y, self.x) = next_step
        grid[self.y][self.x] = self

        self.attack()

    def attack(self):
        attack((self.y, self.x), Elf)

    def __repr__(self):
        return "G"


class Elf(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.hp = 200

    def bfs(self):
        "Search for reachable enemies"

        return bfs((self.y, self.x), Goblin)

    def step(self):
        "move/attack"
        global grid

        if self.hp <= 0:
            return

        old = (self.y, self.x)
        next_step = choose_move(self.bfs())
        if next_step is None:
            self.attack()
            return

        grid[old[0]][old[1]] = GridSlot.GRID_OPEN
        _, (self.y, self.x) = next_step
        grid[self.y][self.x] = self

        self.attack()

    def attack(self):
        attack((self.y, self.x), Goblin)

    def __repr__(self):
        return "E"


grid = []
movers = []
with open("input.txt") as f:
    for y, row in enumerate(f):
        grid_row = []
        for x, c in enumerate(row.strip()):
            if c == "#":
                grid_row.append(GridSlot.GRID_WALL)
            elif c == ".":
                grid_row.append(GridSlot.GRID_OPEN)
            elif c == "G":
                new_goblin = Goblin(x, y)
                grid_row.append(new_goblin)
                movers.append(new_goblin)
            elif c == "E":
                new_elf = Elf(x, y)
                grid_row.append(new_elf)
                movers.append(new_elf)
        grid.append(grid_row)

grid_width = len(grid[0])
grid_height = len(grid)


def print_grid(grid):
    grid_strs = list(map(lambda x: "".join(map(lambda y: y.__repr__(), x)), grid))

    for i, row in enumerate(grid):
        line_movers = list(filter(lambda x: isinstance(x, Elf) or isinstance(x, Goblin), row))

        for m in line_movers:
            grid_strs[i] += f" G({m.hp})" if isinstance(m, Goblin) else f" E({m.hp})"

    print("\n".join(grid_strs))


def enemy_adjacent(pos, enemytype):
    "pos :: (y, x)"
    global grid

    y = pos[0]
    x = pos[1]
    if y - 1 >= 0 and isinstance(grid[y - 1][x], enemytype):
        return True
    if y + 1 < grid_height and isinstance(grid[y + 1][x], enemytype):
        return True
    if x - 1 >= 0 and isinstance(grid[y][x - 1], enemytype):
        return True
    if x + 1 < grid_width and isinstance(grid[y][x + 1], enemytype):
        return True

    return False


def add_initial(move_queue, start):
    global grid_width
    global grid_height
    global grid

    x = start[1]
    y = start[0]

    if y - 1 >= 0 and grid[y-1][x] == GridSlot.GRID_OPEN:
        move_queue.append(((y - 1, x), (y - 1, x), 1))
    if x - 1 >= 0 and grid[y][x-1] == GridSlot.GRID_OPEN:
        move_queue.append(((y, x - 1), (y, x - 1), 1))
    if x + 1 < grid_width and grid[y][x+1] == GridSlot.GRID_OPEN:
        move_queue.append(((y, x + 1), (y, x + 1), 1))
    if y + 1 < grid_height and grid[y+1][x] == GridSlot.GRID_OPEN:
        move_queue.append(((y + 1, x), (y + 1, x), 1))


def bfs(start, enemytype):
    "start :: (y, x); returns None if we should attack"
    global grid

    if enemy_adjacent(start, enemytype):
        return None

    destinations = []
    move_queue = deque()
    add_initial(move_queue, start)

    visited = {start}
    while move_queue:
        (first_y, first_x), (y, x), pathlen = move_queue.popleft()
        visited.add((y, x))

        if enemy_adjacent((y, x), enemytype):
            destinations.append(((first_y, first_x), (y, x), pathlen))

        dests = list(map(lambda x: x[1], move_queue))
        if (
            (y - 1, x) not in visited
            and (y - 1, x) not in dests
            and y - 1 >= 0
            and grid[y - 1][x] == GridSlot.GRID_OPEN
        ):
            move_queue.append(((first_y, first_x), (y - 1, x), pathlen + 1))
        if (
            (y, x - 1) not in visited
            and (y, x - 1) not in dests
            and x - 1 >= 0
            and grid[y][x - 1] == GridSlot.GRID_OPEN
        ):
            move_queue.append(((first_y, first_x), (y, x - 1), pathlen + 1))
        if (
            (y, x + 1) not in visited
            and (y, x + 1) not in dests
            and x + 1 < grid_width
            and grid[y][x + 1] == GridSlot.GRID_OPEN
        ):
            move_queue.append(((first_y, first_x), (y, x + 1), pathlen + 1))
        if (
            (y + 1, x) not in visited
            and (y + 1, x) not in dests
            and y + 1 < grid_height
            and grid[y + 1][x] == GridSlot.GRID_OPEN
        ):
            move_queue.append(((first_y, first_x), (y + 1, x), pathlen + 1))

    return destinations


def first_reading(options):
    "first_moves :: [(y, x)]; uses default tuple comparison (first, tiebreak on second)"
    assert options

    return min(options)


def choose_move(destinations):
    "consumes output from bfs"
    global grid

    if not destinations:
        return

    destinations.sort(key=lambda x: x[2])
    min_dist = destinations[0][2]

    destinations = list(filter(lambda x: x[2] == min_dist, destinations))
    first_steps = list(map(lambda x: x[0], destinations))
    finals = list(map(lambda x: x[1], destinations))

    dest = first_reading(finals)
    first_step = list(filter(lambda x: x[1] == dest, destinations))[0][0]

    return (dest, first_step)

def attack(pos, enemytype):
    "pos :: (y, x)"
    global grid
    global movers

    y = pos[0]
    x = pos[1]

    targets = [grid[y-1][x], grid[y+1][x], grid[y][x-1], grid[y][x+1]]
    targets = [x for x in targets if isinstance(x, enemytype)]

    if not targets:
        return

    min_hp = min(targets, key=lambda x: x.hp)
    mins = list(filter(lambda x: x.hp == min_hp.hp, targets))
    attackee = min(mins, key=lambda x: (x.y, x.x))

    attackee.hp -= 3
    if attackee.hp <= 0:
        grid[attackee.y][attackee.x] = GridSlot.GRID_OPEN
        movers = [m for m in movers if m != attackee]

# print_grid(grid)
# print("")

round_no = 0
num_elves = len(list(filter(lambda x: isinstance(x, Elf), movers)))
while num_elves != 0 and num_elves != len(movers):
    # Sort the movers in reading order
    movers.sort(key=lambda x: (x.y, x.x))
    for i, m in enumerate(movers):
        m.step()

        num_elves = len(list(filter(lambda x: isinstance(x, Elf), movers)))
        if num_elves == 0 or num_elves == len(movers):
            if i == len(movers):
                round_no += 1
            sum_hp = sum(map(lambda x: x.hp, movers))
            print(round_no * sum_hp)
            exit()

    round_no += 1
