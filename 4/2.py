import re
import sys

from cerberus import Validator  # type: ignore
from typing import Callable, TextIO


# Provide a custom field validation function for a height with units.
def compare_hgt_with_units(field: str, value: str, error: Callable[..., str]) -> None:
    if value.endswith("cm"):
        if not (150 <= int(value.rstrip("cm")) <= 193):
            error(field, "out of range")
    elif value.endswith("in"):
        if not (59 <= int(value.rstrip("in")) <= 76):
            error(field, "out of range")
    else:
        error(field, "missing units")


SCHEMA = {
    "byr": {"min": "1920", "max": "2002"},
    "iyr": {"min": "2010", "max": "2020"},
    "eyr": {"min": "2020", "max": "2030"},
    "hgt": {
        "anyof": [
            {"allof": [{"regex": "[0-9]+cm"}, {"check_with": compare_hgt_with_units}]},
            {"allof": [{"regex": "[0-9]+in"}, {"check_with": compare_hgt_with_units}]},
        ]
    },
    "hcl": {"regex": "#[0-9a-f]{6}"},
    "ecl": {"allowed": ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"]},
    "pid": {"regex": "[0-9]{9}"},
    "cid": {"required": False},
}


def handler(batch_file: TextIO) -> int:
    valid_passports = 0
    v = Validator(SCHEMA, require_all=True)

    # Split the batch file records by double newline.
    batch_file_contents = batch_file.read().split("\n\n")
    for record in batch_file_contents:
        keys = []
        values = []

        # Split the fields within a record by a space or newline.
        record_field_list = re.compile(r"\s|\n").split(record.strip())

        # Split the field name and field value and add them to distinct
        # lists.
        for field in record_field_list:
            key, value = field.split(":")
            keys.append(key)
            values.append(value)

        # Zip the field name and field value lists together, and convert
        # that into a dictionary.
        document = dict(zip(keys, values))

        # Validate the document against the SCHEMA.
        if v.validate(document):
            valid_passports += 1

    return valid_passports


if __name__ == "__main__":
    print(handler(sys.stdin))
