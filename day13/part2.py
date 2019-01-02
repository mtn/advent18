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


intersection_dirs = [DIR_LEFT, DIR_STRAIGHT, DIR_RIGHT]
dir_map = {"^": DIR_UP, "v": DIR_DOWN, ">": DIR_RIGHT, "<": DIR_LEFT}
track_map = {
    "-": STRAIGHT_HORIZ,
    "<": STRAIGHT_HORIZ,
    ">": STRAIGHT_HORIZ,
    "|": STRAIGHT_VERT,
    "^": STRAIGHT_VERT,
    "v": STRAIGHT_VERT,
    "+": INTERSECTION,
    "/": CURVE_RIGHT,
    "\\": CURVE_LEFT,
    " ": EMPTY,
}

back = {
    STRAIGHT_HORIZ: "-",
    STRAIGHT_VERT: "|",
    INTERSECTION: "+",
    CURVE_RIGHT: "/",
    CURVE_LEFT: "\\",
    EMPTY: " ",
}

tracks = []
trains = []  # stays ordered
train_map = {}  # positions => train


class Train(object):
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.dir = direction

        self.prevx = None
        self.prevy = None

        self.dir_ind = 0
        self.crashed = False

    def update_position(self):
        global train_map

        self.prevx = self.x
        self.prevy = self.y

        del train_map[(self.x, self.y)]

        if self.dir == DIR_UP:
            self.y -= 1
        elif self.dir == DIR_DOWN:
            self.y += 1
        elif self.dir == DIR_LEFT:
            self.x -= 1
        elif self.dir == DIR_RIGHT:
            self.x += 1
        else:
            assert False, self.dir

        # Remove trains on collision
        if (self.x, self.y) in train_map:
            train_map[(self.x, self.y)].remove()
            self.remove()
            del train_map[(self.x, self.y)]
        else:
            train_map[(self.x, self.y)] = self

        return True

    def update_direction(self):
        global tracks

        new_tile = tracks[self.y][self.x]

        if new_tile == INTERSECTION:
            new_dir = self.orient(intersection_dirs[self.dir_ind])
            self.dir_ind += 1
            self.dir_ind %= 3

            self.dir = new_dir

        elif new_tile == CURVE_RIGHT:
            if self.dir == DIR_UP:
                self.dir = DIR_RIGHT
            elif self.dir == DIR_RIGHT:
                self.dir = DIR_UP
            elif self.dir == DIR_DOWN:
                self.dir = DIR_LEFT
            elif self.dir == DIR_LEFT:
                self.dir = DIR_DOWN
            else:
                assert False, self.dir

        elif new_tile == CURVE_LEFT:
            if self.dir == DIR_UP:
                self.dir = DIR_LEFT
            elif self.dir == DIR_RIGHT:
                self.dir = DIR_DOWN
            elif self.dir == DIR_DOWN:
                self.dir = DIR_RIGHT
            elif self.dir == DIR_LEFT:
                self.dir = DIR_UP
            else:
                assert False, self.dir

    def step(self):
        if self.crashed:
            return False

        updated = self.update_position()
        self.update_direction()

        return updated

    def orient(self, new_dir):
        if new_dir == DIR_STRAIGHT:
            return self.dir

        if new_dir == DIR_RIGHT:
            return (self.dir + 1) % 4
        if new_dir == DIR_LEFT:
            return (self.dir - 1) % 4

        assert False

    def remove(self):
        self.crashed = True


# with open("input_sample_last.txt") as f:
with open("input.txt") as f:
    for y, line in enumerate(f):
        track_row = []
        for x, c in enumerate(line):
            LINE_LEN = len(line) - 1
            if c == "\n":
                continue
            if c in ["^", "v", "<", ">"]:
                trains.append(Train(x, y, dir_map[c]))
                assert (x, y) not in train_map
                train_map[(x, y)] = trains[-1]
            track_row.append(track_map[c])

        tracks.append(track_row)


def print_tracks():
    global tracks
    global train_positions
    global trains

    for y, row in enumerate(tracks):
        row_cpy = list(map(lambda x: back[x], row))
        for x in range(LINE_LEN):
            if (x, y) in train_map:
                row_cpy[x] = "*"

        print("".join(row_cpy))


while trains:
    # print("remaining to start round", len(list(filter(lambda x: not x.crashed, trains))))
    updated_cnt = 0
    last_updated = None
    trains.sort(key=lambda t: (t.x, t.y))
    for i, train in enumerate(trains):
        updated = trains[i].step()
        if updated:
            updated_cnt += 1
            last_updated = trains[i]

    if updated_cnt == 1:
        print(f"{last_updated.prevx},{last_updated.prevy}")
        exit()
