import fileinput
from fileinput import FileInput

import numpy as np

ROWS = 128
COLUMNS = 8
ROW_MULTIPLY = 8
SEAT_PLAN = np.zeros((ROWS, COLUMNS), dtype=np.int8)
SEAT_OCCUPIED = 1
SEAT_EMPTY = 0


def fill_seat_plan(boarding_pass: str) -> None:
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

    SEAT_PLAN[row_section[0], col_section[0]] = SEAT_OCCUPIED


def handler(boarding_passes: FileInput) -> int:
    for boarding_pass in boarding_passes:
        fill_seat_plan(boarding_pass.strip())

    open_seat_id = 0
    for x in range(len(SEAT_PLAN)):
        for y in range(len(SEAT_PLAN[x])):
            # Filter out the front and back of the seat plan.
            if x <= ROWS - 5 and x >= 5:
                if SEAT_PLAN[x][y] == SEAT_EMPTY:
                    open_seat_id = x * ROW_MULTIPLY + y

    return open_seat_id


if __name__ == "__main__":
    print(handler(fileinput.input()))
