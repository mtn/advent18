#!/usr/bin/env python3

import re


with open("input.txt") as f:
    lines = f.read().strip().split("\n")

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

ops = [addr, addi, mulr, muli, banr, bani, borr, bori, setr, seti, gtir, gtri, gtrr, eqir, eqri, eqrr]
assert len(ops) == 16

line_iter = iter(lines)
total_same = 0
for line in line_iter:
    if "Before" in line:
        before = list(map(int, re.findall("[0-9]+", line)))
        opline = list(map(int, re.findall("[0-9]+", next(line_iter))))
        after = list(map(int, re.findall("[0-9]+", next(line_iter))))

        same_cnt = 0
        same_ops = []
        for op in ops:
            if op(before, opline) == after:
                same_cnt += 1
                same_ops.append(op)
            if same_cnt == 3:
                total_same += 1
                break

        next(line_iter)
    else:
        break # make sure nothign funny is happening with part2 inputs

print(total_same)
