import re
import sys

from typing import TextIO


def handler(batch_file: TextIO) -> int:
    valid_passports = 0

    # Split the batch file records by double newline.
    batch_file_contents = batch_file.read().split("\n\n")
    for record in batch_file_contents:
        # Split the fields within a record by a space or newline, but
        # also preemptively remove all CID fields.
        cid_filtered_record = filter(
            lambda x: not x.startswith("cid:"),
            re.compile(r"\s|\n").split(record.strip()),
        )

        # Naively check the length of the filtered record against the
        # valid number of fields (7).
        if len(list(cid_filtered_record)) == 7:
            valid_passports += 1

    return valid_passports


if __name__ == "__main__":
    print(handler(sys.stdin))
