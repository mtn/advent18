#!/usr/bin/env python3

letter_stack = []
letters = set()
results = {}


def can_explode(l1, l2):
    return l1.lower() == l2.lower() and (
        (l1.isupper() and l2.islower()) or (l1.islower() and l2.isupper())
    )


with open("input.txt") as f:
    polymer = f.read().strip()

for c in polymer:
    letters.add(c.lower())

for letter in letters:
    letter_stack = []
    for c in polymer:
        if c.lower() == letter:
            continue

        if letter_stack and can_explode(c, letter_stack[-1]):
            letter_stack.pop()
        else:
            letter_stack.append(c)

    results[letter] = len(letter_stack)


min_letter = None
min_length = len(letter_stack)
for letter in results:
    if results[letter] <= min_length:
        min_length = results[letter]
        min_letter = letter

print(min_length)
