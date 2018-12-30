#!/usr/bin/env python3

with open("input.txt") as f:
    inp = int(f.read().strip().split("\n")[8].split()[1])

seen = set()
c = 0
while True:
    a = c | 65536
    c = inp

    while True:
        c += a & 255
        c &= 16777215
        c *= 65899
        c &= 16777215

        if 256 > a:
            if c not in seen:
                seen.add(c)
                last = c
                break
            else:
                print(last)
                exit()
        else:
            a //= 256
