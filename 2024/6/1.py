import fileinput
from enum import IntEnum
from fileinput import FileInput


class Direction(IntEnum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3


DIRECTION_VECTORS = {
    Direction.UP: (-1, 0),  # Move up: decrease row, same column
    Direction.RIGHT: (0, 1),  # Move right: same row, increase column
    Direction.DOWN: (1, 0),  # Move down: increase row, same column
    Direction.LEFT: (0, -1),  # Move left: same row, decrease column
}


def turn_right(direction_index: int) -> int:
    """Return the next direction when turning right."""
    if direction_index == Direction.LEFT:
        return Direction.UP

    return Direction(direction_index + 1)


def find_guard_start_and_direction(grid: list[str]) -> tuple[int, int, int]:
    """Find the guard's starting position and direction in the grid."""
    guard_symbol_to_direction = {"^": Direction.UP, ">": Direction.RIGHT, "v": Direction.DOWN, "<": Direction.LEFT}

    for row_index, row in enumerate(grid):
        for col_index, cell_value in enumerate(row):
            if cell_value in guard_symbol_to_direction:
                return (row_index, col_index, int(guard_symbol_to_direction[cell_value]))

    raise ValueError("No guard found in grid")


def simulate_patrol(grid: list[str]) -> int:
    grid_height = len(grid)
    grid_width = len(grid[0])

    guard_row, guard_col, direction = find_guard_start_and_direction(grid)

    visited_positions: set[tuple[int, int]] = set()
    visited_positions.add((guard_row, guard_col))

    while True:
        delta_row, delta_col = DIRECTION_VECTORS[Direction(direction)]
        next_row = guard_row + delta_row
        next_col = guard_col + delta_col

        # Check if front is within bounds.
        if 0 <= next_row < grid_height and 0 <= next_col < grid_width:
            # If there is an obstacle in front, turn right
            if grid[next_row][next_col] == "#":
                direction = turn_right(direction)
            else:
                # Move forward.
                guard_row, guard_col = next_row, next_col
                visited_positions.add((guard_row, guard_col))
        else:
            break

    return len(visited_positions)


def handler(raw_lines: FileInput) -> int:
    grid = [line.strip() for line in raw_lines]

    return simulate_patrol(grid)


if __name__ == "__main__":
    print(handler(fileinput.input()))
