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


def run(node_name, done):
    if node_name in done:
        return
    print(node_name)
    available = nodes[node_name].waiters
    for edge in nodes[node_name].waiters:
        available.append(edge)
    available.sort()

    for job in available:
        run(done, done)
    done.append(node_name)


available = list(starters)
heapq.heapify(available)
done = []
while available:
    next_job = heapq.heappop(available)
    done.append(next_job)

    for edge in nodes[next_job].waiters:
        if edge not in available and edge not in done:
            for w in nodes[edge].waitees:
                if w not in done:
                    break
            else:
                heapq.heappush(available, edge)

print("".join(done))
