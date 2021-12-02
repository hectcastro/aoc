import sys
from itertools import count
from typing import Dict, TextIO


def handler(raw_instructions: TextIO) -> int:
    buses: Dict[int, int] = {}
    for index, bus_id in enumerate(raw_instructions.readlines()[1].split(",")):
        if bus_id != "x":
            buses[int(bus_id)] = index

    starting_index = 0
    steps = 1
    for bus, offset in sorted(buses.items(), reverse=True):
        for timestamp in count(starting_index, steps):
            if not (timestamp + offset) % bus:
                starting_index = timestamp
                steps *= bus
                break

    return timestamp


def part2(buses):
    start_idx, steps = 0, 1
    for bus, offset in sorted(buses.items(), reverse=True):
        for tstamp in count(start_idx, steps):
            if not (tstamp + offset) % bus:
                start_idx = tstamp
                steps *= bus
                break
    return tstamp


if __name__ == "__main__":
    print(handler(sys.stdin))
