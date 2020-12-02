import fileinput

from fileinput import FileInput
from typing import Iterable, Tuple


def parse_entries(entry: str) -> Tuple[Iterable, str, str]:
    policy, passwd = entry.split(":")
    rng, letter = policy.split(" ")
    start, end = rng.split("-")

    return (range(int(start), int(end) + 1), letter, passwd)


def handler(entries: FileInput) -> int:
    valid_passwd = 0

    for entry in entries:
        rng, letter, passwd = parse_entries(entry.strip())

        if passwd.count(letter) in rng:
            valid_passwd += 1

    return valid_passwd


if __name__ == "__main__":
    print(handler(fileinput.input()))
