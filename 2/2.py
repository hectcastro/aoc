import fileinput

from fileinput import FileInput
from typing import Tuple


def parse_entries(entry: str) -> Tuple[int, int, str, str]:
    policy, passwd = entry.split(": ")
    rng, letter = policy.split(" ")
    pos1, pos2 = rng.split("-")

    # Subtracting one helps account for the policy indexing
    # characters by one.
    return (int(pos1) - 1, int(pos2) - 1, letter, passwd)


def handler(entries: FileInput) -> int:
    valid_passwd = 0

    for entry in entries:
        pos1, pos2, letter, passwd = parse_entries(entry.strip())

        if (passwd[pos1] == letter) ^ (passwd[pos2] == letter):
            valid_passwd += 1

    return valid_passwd


if __name__ == "__main__":
    print(handler(fileinput.input()))
