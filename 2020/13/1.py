import sys
from typing import Dict, TextIO


def handler(raw_instructions: TextIO) -> int:
    raw_earliest_timestamp, raw_buses = map(str.strip, raw_instructions.readlines())
    earliest_timestamp = int(raw_earliest_timestamp)
    buses = list(map(int, filter(lambda x: x != "x", raw_buses.split(","))))

    schedule: Dict[int, int] = dict(zip(buses, [0] * len(buses)))
    multiplier = 1

    for bus in schedule.keys():
        while True:
            bus_arrival = bus * multiplier
            multiplier += 1

            if bus_arrival >= earliest_timestamp:
                schedule[bus] = bus_arrival
                multiplier = 1
                break

    earliest_bus_arrival_timestamp = min(schedule.values())
    earliest_bus_id = list(schedule.keys())[list(schedule.values()).index(earliest_bus_arrival_timestamp)]

    return (earliest_bus_arrival_timestamp - earliest_timestamp) * earliest_bus_id


if __name__ == "__main__":
    print(handler(sys.stdin))
