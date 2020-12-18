import sys

from collections import defaultdict
from itertools import product
from typing import cast, Dict, Generator, TextIO, Tuple


def neighborhood(
    coord: Tuple[int, int, int, int]
) -> Generator[Tuple[int, int, int, int], None, None]:
    for offset in product([-1, 0, 1], repeat=len(coord)):
        yield cast(
            Tuple[int, int, int, int],
            tuple(pos + offset[index] for index, pos in enumerate(coord)),
        )


def handler(raw_region: TextIO) -> int:
    region: Dict[Tuple[int, int, int, int], str] = defaultdict(lambda: ".")

    for x, line in enumerate(raw_region.readlines()):
        for y, state in enumerate(line.strip()):
            for z in range(1):
                region[(x, y, z, z)] = state

    cycles = 0

    while True:
        active_region: Dict[Tuple[int, int, int, int], int] = defaultdict(int)

        for coords in region:
            if region[coords] == ".":
                continue

            for neighbor in neighborhood(coords):
                active_region[neighbor] += neighbor != coords and region[coords] == "#"

        for neighbor, count in active_region.items():
            if region[neighbor] == "#":
                if count in [2, 3]:
                    region[neighbor] = "#"
                else:
                    region[neighbor] = "."
            elif region[neighbor] == ".":
                if count == 3:
                    region[neighbor] = "#"

        cycles += 1
        if cycles == 6:
            break

    return sum(state == "#" for state in region.values())


if __name__ == "__main__":
    print(handler(sys.stdin))
