#!/usr/bin/env python3


words = set()
with open("input.txt") as f:
    for word in f:
        word = word.strip()
        for seen in words:
            diff = [c for i, c in enumerate(seen) if word[i] != c]
            if len(diff) == 1:
                print("".join([c for i, c in enumerate(seen) if word[i] == c]))
                exit()

        words.add(word.strip())

