#!/usr/bin/env python3

import heapq


nodes = {}
starters = set()
non_starters = set()


class Node(object):
    def __init__(self, name):
        self.name = name
        self.waiters = []
        self.waitees = []


with open("input.txt") as f:
    for req in f:
        req_split = req.strip().split()
        # then depends on first
        first, then = req_split[1], req_split[7]

        if first not in nodes:
            nodes[first] = Node(first)
        if then not in nodes:
            nodes[then] = Node(then)

        if first not in non_starters:
            starters.add(first)
        nodes[first].waiters.append(then)
        nodes[then].waitees.append(first)
        if then in starters:
            starters.remove(then)
        non_starters.add(then)

available = list(starters)
heapq.heapify(available)
done = []
num_workers = 5
working = [None] * num_workers
tick = -1
while available or (len(set(working)) - 1):
    tick += 1
    for i in range(num_workers):
        if working[i] is not None:
            job, start_time, required_time = working[i]
            if tick - start_time == required_time:
                working[i] = None
                done.append(job)

                for edge in nodes[job].waiters:
                    if edge not in available and edge not in done:
                        for w in nodes[edge].waitees:
                            if w not in done:
                                break
                        else:
                            heapq.heappush(available, edge)

        if working[i] is None:
            if not available:
                continue
            else:
                next_job = heapq.heappop(available)
                # print(f"{i}, t {tick}: Starting to work on {next_job}")
                working[i] = (next_job, tick, ord(next_job) - ord("A") + 1 + 60)

print(tick - 1)
