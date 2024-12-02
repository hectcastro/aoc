import sys
from collections import defaultdict
from dataclasses import dataclass
from typing import Any, Dict, TextIO

CUP_NUMBER = 1000000
STEP_NUMBER = 10000000


@dataclass
class Cup:
    label: int
    next: Any


def handler(raw_cups: TextIO) -> Any:
    cups = [int(cup) for cup in raw_cups.read().strip()]
    lookup_table: Dict[int, Any] = defaultdict(lambda: None)

    for index in range(1, CUP_NUMBER + 1):
        lookup_table[index] = Cup(index, None)
        if index != 1:
            lookup_table[index - 1].next = lookup_table[index]

    lookup_table[1].next = lookup_table[2]
    lookup_table[CUP_NUMBER].next = lookup_table[cups[0]]

    for index in range(len(cups)):
        lookup_table[cups[index]].next = lookup_table[cups[(index + 1) % len(cups)]]

    if CUP_NUMBER > len(cups):
        lookup_table[cups[-1]].next = lookup_table[len(cups) + 1]

    current_cup = lookup_table[cups[0]]

    for _ in range(STEP_NUMBER):
        selection = current_cup.next
        current_cup.next = current_cup.next.next.next.next

        seek = current_cup.label - 1 if current_cup.label > 1 else CUP_NUMBER
        while seek in [
            current_cup.label,
            selection.label,
            selection.next.label,
            selection.next.next.label,
        ]:
            seek -= 1
            if seek < 1:
                seek = CUP_NUMBER

        next_cup = lookup_table[seek]
        selection.next.next.next = next_cup.next
        next_cup.next = selection
        current_cup = current_cup.next

    return lookup_table[1].next.label * lookup_table[1].next.next.label


if __name__ == "__main__":
    print(handler(sys.stdin))
