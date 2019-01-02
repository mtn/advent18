#!/usr/bin/env python3

import re


def addr(reg, a, b):
    return reg[a] + reg[b]


def addi(reg, a, b):
    return reg[a] + b


def mulr(reg, a, b):
    return reg[a] * reg[b]


def muli(reg, a, b):
    return reg[a] * b


def banr(reg, a, b):
    return reg[a] & reg[b]


def bani(reg, a, b):
    return reg[a] & b


def borr(reg, a, b):
    return reg[a] | reg[b]


def bori(reg, a, b):
    return reg[a] | b


def setr(reg, a, b):
    return reg[a]


def seti(reg, a, b):
    return a


def gtir(reg, a, b):
    return 1 if a > reg[b] else 0


def gtri(reg, a, b):
    return 1 if reg[a] > b else 0


def gtrr(reg, a, b):
    return 1 if reg[a] > reg[b] else 0


def eqir(reg, a, b):
    return 1 if a == reg[b] else 0


def eqri(reg, a, b):
    return 1 if reg[a] == b else 0


def eqrr(reg, a, b):
    return 1 if reg[a] == reg[b] else 0


with open("input.txt") as f:
    lines = f.read().strip().split("\n")

instructions = []
for line in lines:
    if "#" in line:
        ipr = int(re.findall("[0-9]+", line)[0])
    else:
        op = globals()[line.split()[0]]
        a, b, c = map(int, line.split()[1:])
        instructions.append([op, a, b, c])

ip = 0
registers = [1, 0, 0, 0, 0, 0]
instructions_run = 0
while ip >= 0 and ip <= len(instructions):
    registers[ipr] = ip

    op, a, b, c = instructions[ip]
    registers[c] = op(registers, a, b)

    ip = registers[ipr] + 1

    instructions_run += 1
    if instructions_run > 10000:
        break

to_factor = max(registers)

factor_sum = 0
for i in range(1, to_factor + 1):
    if to_factor % i == 0:
        factor_sum += i

print(factor_sum)
