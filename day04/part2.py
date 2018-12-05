#!/usr/bin/env python3

import collections
from datetime import datetime
from enum import Enum
import heapq
import numpy as np


events = []
heapq.heapify(events)
guards = {}


class EventType(Enum):
    WakeUp = 1
    FallAsleep = 2
    BeginShift = 3


class Event(object):
    def __init__(self, time, event_type, new_guard=None):
        self.time = time
        self.type = event_type
        self.new_guard = new_guard

    def __lt__(self, other):
        return self.time < other.time


with open("input.txt") as f:
    for line in f:
        line_split = line.strip().split()
        datetime_object = datetime.strptime(line.strip()[:18], "[%Y-%m-%d %H:%M]")

        if "begins shift" in line:
            current_guard = line_split[3][1:]

            if current_guard not in guards:
                guards[current_guard] = [0] * 60

            heapq.heappush(
                events, Event(datetime_object, EventType.BeginShift, current_guard)
            )
        elif "wakes up" in line:
            heapq.heappush(events, Event(datetime_object, EventType.WakeUp))
        elif "falls asleep" in line:
            heapq.heappush(events, Event(datetime_object, EventType.FallAsleep))

current_guard = None
sleepers = []

while events:
    event = heapq.heappop(events)

    if event.type == EventType.BeginShift:
        current_guard = event.new_guard

    elif event.type == EventType.FallAsleep:
        sleepers.append((event.time.minute, current_guard))

    elif event.type == EventType.WakeUp:
        sleep_minute, guard = sleepers.pop()

        for i in range(sleep_minute, event.time.minute):
            guards[guard][i] += 1

maxed_minute = None
time_slept_max = 0
maxed_guard = None
for guard in guards:
    time_slept = max(guards[guard])
    if time_slept_max < time_slept:
        time_slept_max = time_slept
        maxed_minute = np.argmax(guards[guard])
        maxed_guard = int(guard)

print(maxed_guard * maxed_minute)
