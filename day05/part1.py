#!/usr/bin/env python3

letter_stack = []


def can_explode(l1, l2):
    return l1.lower() == l2.lower() and (
        (l1.isupper() and l2.islower()) or (l1.islower() and l2.isupper())
    )


with open("input.txt") as f:
    polymer = f.read().strip()

    for c in polymer:
        if letter_stack and can_explode(c, letter_stack[-1]):
            letter_stack.pop()
        else:
            letter_stack.append(c)


print(len(letter_stack))
