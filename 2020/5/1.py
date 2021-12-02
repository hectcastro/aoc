import fileinput
from fileinput import FileInput
from typing import Tuple

ROWS = 128
COLUMNS = 8
ROW_MULTIPLY = 8


def seat_coords(boarding_pass: str) -> Tuple[int, int]:
    row_instructions = boarding_pass[0:7]
    col_instructions = boarding_pass[7:10]

    row_section = range(0, ROWS)

    for row_instruction in row_instructions:
        if row_instruction == "F":
            row_section = range(row_section[0], row_section[len(row_section) // 2])
        elif row_instruction == "B":
            row_section = range(
                row_section[len(row_section) // 2],
                row_section[len(row_section) - 1] + 1,
            )

    col_section = range(0, COLUMNS)

    for col_instruction in col_instructions:
        if col_instruction == "L":
            col_section = range(col_section[0], col_section[len(col_section) // 2])
        elif col_instruction == "R":
            col_section = range(
                col_section[len(col_section) // 2],
                col_section[len(col_section) - 1] + 1,
            )

    return (row_section[0], col_section[0])


def handler(boarding_passes: FileInput) -> int:
    seat_ids = []

    for boarding_pass in boarding_passes:
        row, column = seat_coords(boarding_pass.strip())
        seat_ids.append(row * ROW_MULTIPLY + column)

    return max(seat_ids)


if __name__ == "__main__":
    print(handler(fileinput.input()))
