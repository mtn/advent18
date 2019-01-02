#!/usr/bin/env python3

points = []
with open("input.txt") as f:
    for line in f:
        points.append(tuple(map(int, line.strip().split(","))))


def manhattan_distance(p1, p2):
    assert len(p1) == 4 and len(p2) == 4
    return (
        abs(p1[0] - p2[0])
        + abs(p1[1] - p2[1])
        + abs(p1[2] - p2[2])
        + abs(p1[3] - p2[3])
    )


member_of = {p: None for p in points}
num_components = len(points)
for p1 in points:
    for p2 in points:
        if p1 == p2:
            continue

        if manhattan_distance(p1, p2) > 3:
            continue

        if member_of[p1] is None and member_of[p2] is None:
            equivalence_class = {p1, p2}
            member_of[p1] = member_of[p2] = equivalence_class
            num_components -= 1

        elif member_of[p1] is None:
            member_of[p2].add(p1)
            member_of[p1] = member_of[p2]
            num_components -= 1

        elif member_of[p2] is None:
            member_of[p1].add(p2)
            member_of[p2] = member_of[p1]
            num_components -= 1

        else:
            if p2 not in member_of[p1]:
                num_components -= 1

            union = member_of[p1].union(member_of[p2])
            for p3 in union:
                member_of[p3] = union

print(num_components)
