import fileinput
from fileinput import FileInput
from typing import Dict, List, Tuple


def neighbors(
    x: int, y: int, seat_positions: Dict[Tuple[int, int], str], rows: int, columns: int
) -> List[str]:
    adjacent_cells = []

    for direction in [
        (-1, -1),
        (-1, 0),
        (-1, 1),
        (0, -1),
        (0, 1),
        (1, -1),
        (1, 0),
        (1, 1),
    ]:
        row = x
        col = y

        while True:
            row += direction[0]
            col += direction[1]

            if row < 0 or row > rows - 1 or col < 0 or col > columns - 1:
                break

            cell = seat_positions.get((row, col), None)
            if cell and cell != ".":
                adjacent_cells.append(cell)
                break

    return adjacent_cells


def handler(raw_seat_positions: FileInput) -> int:
    layouts: List[Dict[Tuple[int, int], str]] = []
    seat_positions: Dict[Tuple[int, int], str] = {}
    rows, columns = (0, 0)

    for row, raw_seat_position in enumerate(raw_seat_positions):
        for col, status in enumerate(raw_seat_position.strip()):
            seat_positions[(row, col)] = status
        rows += 1
        columns = len(raw_seat_position.strip())

    while True:
        new_seat_positions: Dict[Tuple[int, int], str] = {}

        for x, y in seat_positions.keys():
            adjacent_cells = neighbors(x, y, seat_positions, rows, columns)
            new_seat_positions[(x, y)] = seat_positions[(x, y)]

            if seat_positions[(x, y)] == "L":
                if all(map(lambda x: x == "L", adjacent_cells)):
                    new_seat_positions[(x, y)] = "#"
            elif seat_positions[(x, y)] == "#":
                if adjacent_cells.count("#") >= 5:
                    new_seat_positions[(x, y)] = "L"

        if len(layouts) > 0 and layouts[-1] == new_seat_positions:
            return list(new_seat_positions.values()).count("#")
        else:
            layouts.append(new_seat_positions)

        seat_positions = new_seat_positions

    return 0


if __name__ == "__main__":
    print(handler(fileinput.input()))
