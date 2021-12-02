import sys
from typing import TextIO

MOVES = 100


def handler(raw_cups: TextIO) -> str:
    cups = [int(cup) for cup in raw_cups.read().strip()]

    for move in range(MOVES):
        current_cup = cups[move % len(cups)]
        pick_up = [
            cups[(move + 1) % len(cups)],
            cups[(move + 2) % len(cups)],
            cups[(move + 3) % len(cups)],
        ]

        for cup in pick_up:
            del cups[cups.index(cup)]

        seek = current_cup - 1

        while seek not in cups:
            seek -= 1
            if seek < 1:
                seek = 9

        destination = cups.index(seek)
        cups = cups[: destination + 1] + pick_up + cups[destination + 1 :]

        while cups[move % len(cups)] != current_cup:
            cups = cups[1:] + [cups[0]]

    split = cups.index(1)
    return "".join([str(cup) for cup in cups[split + 1 :] + cups[:split]])


if __name__ == "__main__":
    print(handler(sys.stdin))
