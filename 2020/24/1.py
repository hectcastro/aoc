import fileinput
from collections import Counter
from fileinput import FileInput
from typing import Dict, Tuple

DIRS: Dict[str, Tuple[int, int]] = {
    "e": (2, 0),
    "se": (1, 1),
    "sw": (-1, 1),
    "w": (-2, 0),
    "nw": (-1, -1),
    "ne": (1, -1),
}


def handler(raw_tiles: FileInput) -> int:
    end_position = []

    for tile in raw_tiles:
        tile = tile.strip()
        position = 0
        x, y = (0, 0)

        while position < len(tile):
            for offset in range(1, 3):
                direction = tile[position : position + offset]

                if direction in DIRS:
                    dx, dy = DIRS[direction]
                    x += dx
                    y += dy
                    position += offset
                    break

        end_position.append((x, y))

    blacks = set()
    for pos, answer in Counter(end_position).items():
        if answer % 2 == 1:
            blacks.add(pos)

    return len(blacks)


if __name__ == "__main__":
    print(handler(fileinput.input()))
