#!/usr/bin/env python3

from collections import deque

with open("input.txt") as f:
   inp = f.read().strip().split(" ")
   num_players = int(inp[0])
   last_worth = int(inp[6])

def run(num_players, last_worth):
    marbles = deque([0])
    scores = [0] * num_players
    i = 0

    for val in range(1, last_worth + 1):
        if val % 23 == 0:
            scores[i] += val

            for _ in range(7):
                m = marbles.pop()
                marbles.appendleft(m)

            scores[i] += marbles.popleft()

        else:
            for _ in range(2):
                m = marbles.popleft()
                marbles.append(m)
            marbles.appendleft(val)

        i += 1
        i %= num_players

    return max(scores)

print(run(num_players, last_worth * 100))
