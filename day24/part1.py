#!/usr/bin/env python3

import re

TYPE_IMMUNE = 0
TYPE_INFECTION = 1

immune_uid = 1
infection_uid = 1


class Unit(object):
    def __init__(
        self,
        unit_type,
        number,
        hitpoints_per,
        attack_type,
        attack_dmg,
        initiative,
        weaknesses,
        immunities,
    ):
        global immune_uid
        global infection_uid
        if unit_type == TYPE_IMMUNE:
            self.uid = immune_uid
            immune_uid += 1
        if unit_type == TYPE_INFECTION:
            self.uid = infection_uid
            infection_uid += 1

        self.num = number
        self.type = unit_type
        self.hp = hitpoints_per  # hitpoints EACH; total = self.hp * self.num
        self.attack = attack_type
        self.attack_dmg = attack_dmg
        self.initiative = initiative
        self.weaknesses = weaknesses
        self.immunities = immunities

        self.chosen = False  # changed each round; is this a target
        self.choice = None

    def power(self):
        return self.num * self.attack_dmg

    def would_damage(self, u2):
        "how much u1 would damage u2"

        if self.attack in u2.immunities:
            return 0

        if self.attack in u2.weaknesses:
            return 2 * self.power()
        return self.power()

    def choose_target(self, verbose=False):
        global units

        choice = None
        max_dmg = 0
        for u in units:
            if u.type == self.type or u.chosen:
                continue

            prospective = self.would_damage(u)
            if prospective > max_dmg:
                choice = u
                max_dmg = prospective

            if verbose:
                print(self, "would deal defending group", u.uid, prospective, "damage")

        if choice:
            choice.chosen = True
            self.choice = choice

    def full_str(self):
        repr_str = ""
        repr_str += "Unit({}, n={}, hp={} attack_type={}, attack_dmg={}, initiative={}, weaknesses={}, immunities={}".format(
            "Infection" if self.type == TYPE_INFECTION else "Immune",
            self.num,
            self.hp,
            self.attack,
            self.attack_dmg,
            self.initiative,
            self.weaknesses,
            self.immunities,
        )
        return repr_str

    def __repr__(self):
        return "{} group {}".format(
            "Infection" if self.type == TYPE_INFECTION else "Immune System", self.uid
        )


units = []
unit_type = TYPE_IMMUNE  # my input starts with immune
with open("input.txt") as f:
    for line in f:
        if not line.strip():
            continue
        if "Immune System:" in line or "Infection:" in line:
            if "Immune System:" in line:
                assert unit_type == TYPE_IMMUNE
            if "Infection:" in line:
                unit_type = TYPE_INFECTION
            continue

        atk = line.split()[-5]
        weaknesses = []
        immunities = []
        if "(" in line:
            substr = line[line.find("(") + 1 : line.find(")")]
            lst = substr.split(";")
            for l in lst:
                l = l.strip()
                if "weak" in l:
                    offset = len("weak to ")
                    weaknesses = list(map(lambda x: x.strip(), l[offset:].split(",")))
                if "immune" in l:
                    offset = len("immune to ")
                    immunities = list(map(lambda x: x.strip(), l[offset:].split(",")))

        n, hp, dmg, init = map(int, re.findall("-?[0-9]+", line))
        units.append(Unit(unit_type, n, hp, atk, dmg, init, weaknesses, immunities))


def step(verbose=False):
    "verbose summarizes a battle step"
    global units

    units = [unit for unit in units if unit.num > 0]
    for unit in units:
        unit.chosen = False
        unit.choice = None

    if verbose:
        units.sort(key=lambda x: x.type)
        print("Immune System:")
        group_cnt = 1
        first_infection = False
        for unit in units:
            if unit.type == TYPE_INFECTION and not first_infection:
                print("Infection:")
                group_cnt = 1
                first_infection = True

            print("Group {} has {} units".format(group_cnt, unit.num))
            group_cnt += 1

        print("")

    # just matters that they are sorted within groups
    units.sort(key=lambda x: (-x.power(), -x.initiative))
    for unit in units:
        unit.choose_target(verbose=verbose)

    if verbose:
        print("")

    units.sort(key=lambda x: -x.initiative)
    for unit in units:
        if unit.choice:
            num_killed = unit.would_damage(unit.choice) // unit.choice.hp
            if num_killed > unit.choice.num:
                num_killed = unit.choice.num  # just so they print out right
            unit.choice.num -= num_killed
            if verbose:
                print(
                    unit,
                    "attacks defending group",
                    unit.choice.uid,
                    "killing",
                    num_killed,
                    "units",
                )

    if verbose:
        print("")


while True:
    if len(list(filter(lambda x: x.type == TYPE_IMMUNE, units))) in [0, len(units)]:
        break
    step()

print(sum(map(lambda x: x.num, units)))
