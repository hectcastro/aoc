import sys
from typing import TextIO

MOD = 20201227


def card_loop_size(subject: int, public_key: int) -> int:
    for n in range(MOD):
        if pow(subject, n, MOD) == public_key:
            return n

    return -1


def handler(raw_public_keys: TextIO) -> int:
    door_public_key, card_public_key = map(
        int, raw_public_keys.read().strip().split("\n")
    )

    return pow(door_public_key, card_loop_size(7, card_public_key), MOD)


if __name__ == "__main__":
    print(handler(sys.stdin))
