#!/usr/bin/env python3

inp = 3214


def power_level(x, y):
    rack_id = x + 10
    power_level = rack_id * y
    power_level += inp
    power_level *= rack_id

    as_str = str(power_level)
    assert len(as_str) >= 3
    hundreds_digit = int(as_str[-3])

    return hundreds_digit - 5


max_power = None
topx, topy = 0, 0
for x in range(1, 298):
    for y in range(1, 298):
        total_power = 0
        for dx in range(3):
            for dy in range(3):
                total_power += power_level(x + dx, y + dy)
        if max_power is None or total_power >= max_power:
            max_power = total_power
            topx = x
            topy = y

print(f"{topx},{topy}")
