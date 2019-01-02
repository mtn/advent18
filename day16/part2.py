#!/usr/bin/env python3

import re


with open("input.txt") as f:
    lines = f.read().strip()


def addr(reg, inarr):
    reg = list(reg)
    reg[inarr[3]] = reg[inarr[1]] + reg[inarr[2]]
    return reg


def addi(reg, inarr):
    reg = list(reg)
    reg[inarr[3]] = reg[inarr[1]] + inarr[2]
    return reg


def mulr(reg, inarr):
    reg = list(reg)
    reg[inarr[3]] = reg[inarr[1]] * reg[inarr[2]]
    return reg


def muli(reg, inarr):
    reg = list(reg)
    reg[inarr[3]] = reg[inarr[1]] * inarr[2]
    return reg


def banr(reg, inarr):
    reg = list(reg)
    reg[inarr[3]] = reg[inarr[1]] & reg[inarr[2]]
    return reg


def bani(reg, inarr):
    reg = list(reg)
    reg[inarr[3]] = reg[inarr[1]] & inarr[2]
    return reg


def borr(reg, inarr):
    reg = list(reg)
    reg[inarr[3]] = reg[inarr[1]] | reg[inarr[2]]
    return reg


def bori(reg, inarr):
    reg = list(reg)
    reg[inarr[3]] = reg[inarr[1]] | inarr[2]
    return reg


def setr(reg, inarr):
    reg = list(reg)
    reg[inarr[3]] = reg[inarr[1]]
    return reg


def seti(reg, inarr):
    reg = list(reg)
    reg[inarr[3]] = inarr[1]
    return reg


def gtir(reg, inarr):
    reg = list(reg)
    reg[inarr[3]] = 1 if inarr[1] > reg[inarr[2]] else 0
    return reg


def gtri(reg, inarr):
    reg = list(reg)
    reg[inarr[3]] = 1 if reg[inarr[1]] > inarr[2] else 0
    return reg


def gtrr(reg, inarr):
    reg = list(reg)
    reg[inarr[3]] = 1 if reg[inarr[1]] > reg[inarr[2]] else 0
    return reg


def eqir(reg, inarr):
    reg = list(reg)
    reg[inarr[3]] = 1 if inarr[1] == reg[inarr[2]] else 0
    return reg


def eqri(reg, inarr):
    reg = list(reg)
    reg[inarr[3]] = 1 if reg[inarr[1]] == inarr[2] else 0
    return reg


def eqrr(reg, inarr):
    reg = list(reg)
    reg[inarr[3]] = 1 if reg[inarr[1]] == reg[inarr[2]] else 0
    return reg


ops = [
    addr,
    addi,
    mulr,
    muli,
    banr,
    bani,
    borr,
    bori,
    setr,
    seti,
    gtir,
    gtri,
    gtrr,
    eqir,
    eqri,
    eqrr,
]
assert len(ops) == 16

total_same = 0
to_run = []

mapped = set()
op_map = {}
solved = set()
possible = {}
for i in range(16):
    if i in op_map:
        possible[i] = {op_map[i]}
    else:
        possible[i] = set(ops) - set(solved)

part1_input, part2_input = lines.split("\n\n\n\n")

part1_lines = part1_input.split("\n")
solved = set()
possible = {i: set(ops) - solved for i in range(16)}

for i, l in enumerate(part1_lines):
    if "Before" not in l:
        continue

    before = list(map(int, re.findall("[0-9]+", l)))
    opline = list(map(int, re.findall("[0-9]+", part1_lines[i + 1])))
    after = list(map(int, re.findall("[0-9]+", part1_lines[i + 2])))

    opcode = opline[0]
    for op in ops:
        if op(before, opline) != after:
            if op in possible[opcode]:
                possible[opcode].remove(op)

while len(solved) < len(ops):
    for i in range(16):
        possible[i] -= solved

        if len(possible[i]) == 1:
            op = list(possible[i])[0]
            solved.add(op)
            op_map[i] = op

reg = [0] * 4
for line in part2_input.split("\n"):
    opline = list(map(int, re.findall("[0-9]+", line)))
    opcode = opline[0]
    reg = op_map[opcode](reg, opline)

print(reg[0])
