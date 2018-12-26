#!/usr/bin/env python3


# Directions go clockwise
DIR_UP = 0
DIR_RIGHT = 1
DIR_DOWN = 2
DIR_LEFT = 3

CURVE_LEFT = 4
CURVE_RIGHT = 5
STRAIGHT_VERT = 6
STRAIGHT_HORIZ = 7
INTERSECTION = 8
EMPTY = 9

DIR_STRAIGHT = 10


dir_map = {"^": DIR_UP, "v": DIR_DOWN, ">": DIR_RIGHT, "<": DIR_LEFT}
track_map = {
    "-":  STRAIGHT_HORIZ,
    "<":  STRAIGHT_HORIZ,
    ">":  STRAIGHT_HORIZ,
    "|":  STRAIGHT_VERT,
    "^":  STRAIGHT_VERT,
    "v":  STRAIGHT_VERT,
    "+":  INTERSECTION,
    "/":  CURVE_RIGHT,
    "\\": CURVE_LEFT,
    " ":  EMPTY,
}

back = {
    STRAIGHT_HORIZ: "-",
    STRAIGHT_VERT:  "|",
    INTERSECTION:   "+",
    CURVE_RIGHT:    "/",
    CURVE_LEFT:     "\\",
    EMPTY:          " ",
}

tracks = []
trains = []
train_positions = set()


with open("input.txt") as f:
    for y, line in enumerate(f):
        track_row = []
        for x, c in enumerate(line):
            LINE_LEN = len(line) - 1
            if c == "\n": continue
            if c in ["^", "v", "<", ">"]:
                trains.append((dir_map[c], x, y, 0))
                assert (x,y) not in train_positions
                train_positions.add((x,y))
            track_row.append(track_map[c])

        tracks.append(track_row)

intersection_dirs = [DIR_LEFT, DIR_STRAIGHT, DIR_RIGHT]

def orient(new_dir, cur_dir):
    if new_dir == DIR_STRAIGHT:
        return cur_dir

    if new_dir == DIR_RIGHT:
        return (cur_dir + 1) % 4
    if new_dir == DIR_LEFT:
        return (cur_dir - 1) % 4

    assert False

def train_after(cur_dir, new_tile, newx, newy, dir_ind):
    global intsection_dirs

    if new_tile == INTERSECTION:
        new_dir = orient(intersection_dirs[dir_ind], cur_dir)
        dir_ind += 1
        dir_ind %= 3
        return (new_dir, newx, newy, dir_ind)

    if new_tile == CURVE_RIGHT:
        if cur_dir == DIR_UP:
            return (DIR_RIGHT, newx, newy, dir_ind)
        if cur_dir == DIR_RIGHT:
            return (DIR_UP, newx, newy, dir_ind)
        if cur_dir == DIR_DOWN:
            return (DIR_LEFT, newx, newy, dir_ind)
        if cur_dir == DIR_LEFT:
            return (DIR_DOWN, newx, newy, dir_ind)
        assert False
    if new_tile == CURVE_LEFT:
        if cur_dir == DIR_UP:
            return (DIR_LEFT, newx, newy, dir_ind)
        if cur_dir == DIR_RIGHT:
            return (DIR_DOWN, newx, newy, dir_ind)
        if cur_dir == DIR_DOWN:
            return (DIR_RIGHT, newx, newy, dir_ind)
        if cur_dir == DIR_LEFT:
            return (DIR_UP, newx, newy, dir_ind)
        assert False


    return (cur_dir, newx, newy, dir_ind)

def print_tracks():
    global tracks
    global train_positions
    global trains

    for y, row in enumerate(tracks):
        row_cpy = list(map(lambda x: back[x], row))
        for x in range(LINE_LEN):
            if (x, y) in train_positions:
                row_cpy[x] = "*"

        print("".join(row_cpy))


while True:
    # print_tracks()
    for i, train in enumerate(trains):
        cur_dir, x, y, dir_ind = train
        train_positions.remove((x, y))
        if cur_dir == DIR_UP:
            new_pos = (x, y-1)
        elif cur_dir == DIR_DOWN:
            new_pos = (x, y+1)
        elif cur_dir == DIR_LEFT:
            new_pos = (x - 1, y)
        elif cur_dir == DIR_RIGHT:
            new_pos = (x + 1, y)
        else:
            assert False, cur_dir

        new_tile = tracks[new_pos[1]][new_pos[0]]
        trains[i] = train_after(cur_dir, new_tile, new_pos[0], new_pos[1], dir_ind)

        if new_pos in train_positions:
            print(f"{new_pos[0]},{new_pos[1]}")
            exit()
        else:
            train_positions.add((new_pos[0], new_pos[1]))
